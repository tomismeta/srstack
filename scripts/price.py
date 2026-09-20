#!/usr/bin/env python3
"""Read indicative STANDARD prices from the fixed canonical Robinhood pool.

With no arguments, supply one JSON object on stdin: {"schema_version": 1}, optionally with
"standard_amount": "12.5" for a gross indicative mark using the same quotes.
Optional "source": "auto" (default), "dexscreener", or "geckoterminal";
"cross_check": true compares the other provider without blending quotes.
Auto uses DEX Screener, falling back to GeckoTerminal only on availability failure.
CLI: [--quote | --amount-standard DECIMAL] [--source auto|dexscreener|geckoterminal]
     [--cross-check]
Any CLI flag selects explicit CLI mode, which never reads stdin; --quote requests
quotes without an amount. DECIMAL has at most 78 digits, at most 18 fractional,
and no sign or exponent. Flags must be exact, unrepeated, separate tokens.
--quote conflicts with --amount-standard; --help must stand alone.
No wallet, endpoint, address, or file inputs.
Python standard library only; no observations are saved.
"""

import hashlib
import http.client
import json
import math
import os
from pathlib import Path
import re
import socket
import ssl
import stat
import sys
import threading
import time
from datetime import datetime, timezone
from decimal import Decimal, localcontext


PROVIDERS = {
    "dexscreener": {"label": "DEX Screener", "host": "api.dexscreener.com",
                    "path": "/latest/dex/pairs/robinhood/", "source_id": "dexscreener-api",
                    "market": "https://dexscreener.com/robinhood/", "accept": "application/json",
                    "fields": ("priceUsd", "priceNative")},
    "geckoterminal": {"label": "GeckoTerminal", "host": "api.geckoterminal.com",
                     "path": "/api/v2/networks/robinhood/pools/", "source_id": "geckoterminal-api",
                     "market": "https://www.geckoterminal.com/robinhood/pools/",
                     "accept": "application/json;version=20230203",
                     "fields": ("base_token_price_usd", "base_token_price_native_currency")},
}
CHAIN_ID = 4663
ZERO_ADDRESS = "0x" + "0" * 40
MAX_INPUT_BYTES = 4096
MAX_FILE_BYTES = 65536
MAX_RESPONSE_BYTES = 65536
REQUEST_TIMEOUT = 10
NOTE = "Provider-reported indicative price; not an executable quote or net proceeds."
BASIS = "Gross indicative value before withdrawal and trading costs; not net proceeds or charter value."
ADDRESS = re.compile(r"0x[0-9a-fA-F]{40}\Z")
POOL_ID = re.compile(r"0x[0-9a-fA-F]{64}\Z")
IDENTIFIER = re.compile(r"[a-zA-Z][a-zA-Z0-9_-]{0,79}\Z")
PLAIN_DECIMAL = re.compile(r"[0-9]+(?:\.[0-9]+)?\Z")


class InputError(ValueError):
    """Invalid bounded stdin or CLI configuration."""


class PackageDataError(ValueError):
    """Fixed packaged identity data is unsafe or invalid."""


class PriceError(ValueError):
    """Provider transport, identity, or usable quotes could not be established."""

    def __init__(self, message, category="invalid"):
        super().__init__(message)
        self.category = category


def _pairs(pairs):
    result = {}
    for key, value in pairs:
        if key in result:
            raise ValueError("duplicate JSON object key")
        result[key] = value
    return result


def _constant(_value):
    raise ValueError("nonfinite JSON number")


def _json_integer(text):
    if len(text) > 80:
        raise ValueError("JSON number exceeds digit limit")
    return int(text)


def _json_float(text):
    if len(text) > 80:
        raise ValueError("JSON number exceeds digit limit")
    value = float(text)
    if not math.isfinite(value):
        raise ValueError("nonfinite JSON number")
    return value


def _json(raw, limit):
    if not isinstance(raw, bytes) or len(raw) > limit:
        raise ValueError("JSON exceeds byte limit or is not bytes")
    text = raw.decode("utf-8")
    depth, quoted, escaped = 0, False, False
    for character in text:
        if quoted:
            if escaped:
                escaped = False
            elif character == "\\":
                escaped = True
            elif character == '"':
                quoted = False
        elif character == '"':
            quoted = True
        elif character in "[{":
            depth += 1
            if depth > 12:
                raise ValueError("JSON nesting exceeds limit")
        elif character in "]}":
            depth -= 1
    return json.loads(text, object_pairs_hook=_pairs, parse_constant=_constant,
                      parse_int=_json_integer, parse_float=_json_float)


def _decimal(value, fractional_digits, positive=False):
    if not isinstance(value, str) or len(value) > 79 or not PLAIN_DECIMAL.fullmatch(value):
        raise ValueError("expected bounded unsigned plain decimal string")
    whole, _, fraction = value.partition(".")
    if len(whole) + len(fraction) > 78 or len(fraction) > fractional_digits:
        raise ValueError("decimal exceeds digit limit")
    whole, fraction = whole.lstrip("0") or "0", fraction.rstrip("0")
    normalized = whole + ("." + fraction if fraction else "")
    if positive and normalized == "0":
        raise ValueError("price must be positive")
    return normalized


def _validate_input(config):
    try:
        if (not isinstance(config, dict) or "schema_version" not in config
                or config.keys() - {"schema_version", "standard_amount", "source", "cross_check"}):
            raise ValueError("unexpected or missing fields")
        if type(config["schema_version"]) is not int or config["schema_version"] != 1:
            raise ValueError("unsupported schema_version")
        source, cross_check = config.get("source", "auto"), config.get("cross_check", False)
        if not isinstance(source, str) or source not in ("auto", "dexscreener", "geckoterminal"):
            raise ValueError("unsupported source")
        if type(cross_check) is not bool:
            raise ValueError("cross_check must be boolean")
        result = {"schema_version": 1, "source": source, "cross_check": cross_check}
        if "standard_amount" in config:
            result["standard_amount"] = _decimal(config["standard_amount"], 18)
        return result
    except (ValueError, TypeError):
        raise InputError("expected schema_version 1, optional unsigned plain decimal standard_amount (78 digits, at most 18 fractional), source auto|dexscreener|geckoterminal, and boolean cross_check") from None


def _read_file(directory, filename):
    before = os.stat(filename, dir_fd=directory, follow_symlinks=False)
    if not stat.S_ISREG(before.st_mode) or before.st_size > MAX_FILE_BYTES:
        raise ValueError("unsafe package file")
    descriptor = os.open(filename, os.O_RDONLY | os.O_NOFOLLOW | os.O_NONBLOCK, dir_fd=directory)
    try:
        opened = os.fstat(descriptor)
        if (not stat.S_ISREG(opened.st_mode) or opened.st_size > MAX_FILE_BYTES
                or (before.st_dev, before.st_ino) != (opened.st_dev, opened.st_ino)):
            raise ValueError("unsafe package file")
        chunks, size = [], 0
        while size <= MAX_FILE_BYTES:
            chunk = os.read(descriptor, MAX_FILE_BYTES + 1 - size)
            if not chunk:
                break
            chunks.append(chunk)
            size += len(chunk)
        raw = b"".join(chunks)
        return _json(raw, MAX_FILE_BYTES), hashlib.sha256(raw).hexdigest()
    finally:
        os.close(descriptor)


def _directory(parent, name):
    before = os.stat(name, dir_fd=parent, follow_symlinks=False)
    if not stat.S_ISDIR(before.st_mode):
        raise ValueError("unsafe package directory")
    descriptor = os.open(name, os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW, dir_fd=parent)
    opened = os.fstat(descriptor)
    if (before.st_dev, before.st_ino) != (opened.st_dev, opened.st_ino):
        os.close(descriptor)
        raise ValueError("package directory changed")
    return descriptor


def _validate_catalog(catalog):
    if (not isinstance(catalog, dict) or type(catalog.get("schema_version")) is not int or catalog["schema_version"] != 1
            or not isinstance(catalog.get("chain"), dict) or type(catalog["chain"].get("id")) is not int or catalog["chain"]["id"] != CHAIN_ID
            or not isinstance(catalog.get("records"), list) or not 1 <= len(catalog["records"]) <= 100):
        raise ValueError("invalid entity catalog")
    entities, addresses = {}, set()
    for record in catalog["records"]:
        if (not isinstance(record, dict) or not isinstance(record.get("id"), str)
                or not IDENTIFIER.fullmatch(record["id"]) or record["id"] in entities
                or type(record.get("chain_id")) is not int or record["chain_id"] != CHAIN_ID
                or not isinstance(record.get("address"), str) or not ADDRESS.fullmatch(record["address"])
                or record["address"].lower() == ZERO_ADDRESS or record["address"].lower() in addresses):
            raise ValueError("invalid or duplicate entity")
        entities[record["id"]] = record["address"].lower()
        addresses.add(record["address"].lower())
    market = catalog.get("market")
    if ("sr-robinhood-standard" not in entities or not isinstance(market, dict)
            or type(market.get("chain_id")) is not int or market["chain_id"] != CHAIN_ID
            or not isinstance(market.get("pool_id"), str) or not POOL_ID.fullmatch(market["pool_id"])
            or int(market["pool_id"], 16) == 0):
        raise ValueError("missing or invalid canonical market identity")
    return {"token_address": entities["sr-robinhood-standard"], "pool_id": market["pool_id"].lower()}


def _load_package():
    descriptors = []
    try:
        if (not all(hasattr(os, flag) for flag in ("O_DIRECTORY", "O_NOFOLLOW", "O_NONBLOCK"))
                or os.open not in os.supports_dir_fd or os.stat not in os.supports_dir_fd
                or os.stat not in os.supports_follow_symlinks):
            raise ValueError("host lacks safe descriptor reads")
        root = os.open(Path(__file__).resolve(strict=True).parent.parent, os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW)
        descriptors.append(root)
        assets = _directory(root, "assets")
        descriptors.append(assets)
        entities = _directory(assets, "entities")
        descriptors.append(entities)
        catalog, digest = _read_file(entities, "robinhood.json")
        return _validate_catalog(catalog), {"assets/entities/robinhood.json": digest}
    except (OSError, ValueError, TypeError, KeyError, RecursionError, RuntimeError):
        raise PackageDataError("fixed bundled identity data is missing, unsafe, or invalid") from None
    finally:
        for descriptor in reversed(descriptors):
            os.close(descriptor)


def _https_request(connection, source, path, deadline, monotonic):
    """Read one bounded response; never follow redirects or expose its body on error."""
    try:
        connection.connect()
        if monotonic() >= deadline:
            raise PriceError("price request deadline exceeded before sending", "unavailable")
        connection.request("GET", path, headers={"Accept": PROVIDERS[source]["accept"],
                           "User-Agent": "srstack/0.2.0 (+https://github.com/tomismeta/srstack)"})
        response = connection.getresponse()
        if response.status != 200:
            category = ("access" if response.status in (401, 403) else "unavailable"
                        if response.status in (404, 429) or 500 <= response.status <= 599 else "invalid")
            raise PriceError("price HTTP request failed (status " + str(response.status) + "); redirects are not followed", category)
        length = response.getheader("Content-Length")
        if length is not None and (not re.fullmatch(r"[0-9]{1,10}", length) or int(length) > MAX_RESPONSE_BYTES):
            raise PriceError("invalid or oversized price response length")
        chunks, size = [], 0
        while size <= MAX_RESPONSE_BYTES:
            remaining = deadline - monotonic()
            if remaining <= 0:
                raise PriceError("price request deadline exceeded", "unavailable")
            if connection.sock is not None:
                connection.sock.settimeout(min(REQUEST_TIMEOUT, remaining))
            chunk = response.read1(min(65536, MAX_RESPONSE_BYTES + 1 - size))
            if not chunk:
                break
            chunks.append(chunk)
            size += len(chunk)
        if size > MAX_RESPONSE_BYTES:
            raise PriceError("price response exceeds byte limit")
        if length is not None and size != int(length):
            raise PriceError("incomplete price response", "unavailable")
        return b"".join(chunks)
    except PermissionError:
        raise PriceError("price transport access denied", "access") from None
    except ssl.SSLCertVerificationError:
        raise PriceError("price transport certificate verification failed", "access") from None
    except (OSError, http.client.HTTPException):
        raise PriceError("price transport failed", "unavailable") from None
    finally:
        connection.close()


def _https(source, path, timeout, deadline, monotonic):
    """Bound DNS, TLS, headers and body without environment proxy handling."""
    timeout = min(timeout, deadline - monotonic())
    if timeout <= 0:
        raise PriceError("price request deadline exceeded", "unavailable")
    connection = http.client.HTTPSConnection(PROVIDERS[source]["host"], timeout=timeout)
    request_deadline = min(deadline, monotonic() + timeout)
    finished, outcome = threading.Event(), []

    def request():
        try:
            outcome.append(_https_request(connection, source, path, request_deadline, monotonic))
        except Exception as error:
            outcome.append(error)
        finally:
            finished.set()

    # Socket timeouts do not reliably bound DNS. A daemon allows the CLI to
    # terminate even if resolution stalls; a late connection cannot send.
    worker = threading.Thread(target=request, daemon=True)
    worker.start()
    if not finished.wait(timeout):
        if connection.sock is not None:
            try:
                connection.sock.shutdown(socket.SHUT_RDWR)
            except OSError:
                pass
        connection.close()
        raise PriceError("price request deadline exceeded", "unavailable")
    if isinstance(outcome[0], Exception):
        if isinstance(outcome[0], PriceError):
            raise outcome[0]
        raise PriceError("price transport failed") from None
    return outcome[0]


def _matching_pair(body, target):
    if body is None or (isinstance(body, dict) and "pairs" in body and body["pairs"] in (None, [])):
        raise PriceError("provider pair data unavailable", "unavailable")
    if not isinstance(body, dict) or not isinstance(body.get("pairs"), list):
        raise PriceError("provider pair schema invalid")
    matches = []
    for pair in body["pairs"]:
        if not isinstance(pair, dict):
            continue
        base, quote = pair.get("baseToken"), pair.get("quoteToken")
        if (pair.get("chainId") == "robinhood" and pair.get("dexId") == "uniswap"
                and isinstance(pair.get("labels"), list) and "v4" in pair["labels"]
                and isinstance(pair.get("pairAddress"), str) and pair["pairAddress"].lower() == target["pool_id"]
                and isinstance(base, dict) and isinstance(base.get("address"), str)
                and base["address"].lower() == target["token_address"]
                and isinstance(quote, dict) and isinstance(quote.get("address"), str)
                and quote["address"].lower() == ZERO_ADDRESS):
            matches.append(pair)
    if len(matches) != 1:
        raise PriceError("provider must return exactly one matching canonical pair", "identity")
    return matches[0]


def _matching_pool(body, target):
    if body is None or (isinstance(body, dict) and "data" in body and body["data"] in (None, [])):
        raise PriceError("provider pool data unavailable", "unavailable")
    if not isinstance(body, dict) or not isinstance(body.get("data"), dict):
        raise PriceError("provider pool schema invalid")
    pool = body["data"]
    attributes, relationships = pool.get("attributes"), pool.get("relationships")
    if not isinstance(attributes, dict) or not isinstance(relationships, dict):
        raise PriceError("provider pool schema invalid")
    expected = {"base_token": "robinhood_" + target["token_address"],
                "quote_token": "robinhood_" + ZERO_ADDRESS, "dex": "uniswap-v4-robinhood"}
    if (pool.get("type") != "pool" or pool.get("id") != "robinhood_" + target["pool_id"]
            or not isinstance(attributes.get("address"), str)
            or attributes["address"].lower() != target["pool_id"]):
        raise PriceError("provider canonical pool identity mismatch", "identity")
    for name, identifier in expected.items():
        relation = relationships.get(name)
        data = relation.get("data") if isinstance(relation, dict) else None
        if not isinstance(data, dict) or data.get("id") != identifier:
            raise PriceError("provider canonical pool relationship mismatch", "identity")
    return attributes


def _multiply(amount, quote):
    # Each operand has at most 78 decimal digits; 156 retains the exact product.
    with localcontext() as context:
        context.prec = 156
        value = format(Decimal(amount) * Decimal(quote), "f")
    return value.rstrip("0").rstrip(".") if "." in value else value


def _evidence(source, target, hashes):
    provider = PROVIDERS[source]
    return {"provider": provider["label"], "source_ids": [provider["source_id"]],
            "source_url": "https://" + provider["host"] + provider["path"] + target["pool_id"],
            "market_url": provider["market"] + target["pool_id"],
            "chain_id": CHAIN_ID, "pool_id": target["pool_id"],
            "token_address": target["token_address"], "quote_token_address": ZERO_ADDRESS,
            "price_observed_at": None, "price_observation_time_status": "not_supplied_by_provider",
            "package_sha256": hashes}


def _observe(source, target, hashes, transport, now, monotonic, deadline):
    request_deadline = min(deadline, monotonic() + REQUEST_TIMEOUT)
    timeout = request_deadline - monotonic()
    if timeout <= 0:
        raise PriceError("price request deadline exceeded", "unavailable")
    try:
        raw = transport(source, PROVIDERS[source]["path"] + target["pool_id"], timeout, request_deadline, monotonic)
    except PriceError:
        raise
    except (PermissionError, ssl.SSLCertVerificationError):
        raise PriceError("price transport access denied", "access") from None
    except (OSError, http.client.HTTPException):
        raise PriceError("price transport failed", "unavailable") from None
    except Exception:
        raise PriceError("price transport failed") from None
    if monotonic() >= request_deadline:
        raise PriceError("price request deadline exceeded", "unavailable")
    try:
        body = _json(raw, MAX_RESPONSE_BYTES)
    except (ValueError, TypeError, RecursionError):
        raise PriceError("bounded provider JSON invalid") from None
    pair = _matching_pair(body, target) if source == "dexscreener" else _matching_pool(body, target)
    values, errors = {}, {}
    fields = PROVIDERS[source]["fields"]
    for field, identifier, unit in zip(fields, ("standard_usd", "standard_eth"), ("USD/STANDARD", "ETH/STANDARD")):
        try:
            values[identifier] = {"value": _decimal(pair.get(field), 36, positive=True), "unit": unit}
        except ValueError:
            errors[identifier] = "provider denomination missing or invalid positive plain decimal string"
    if not values:
        category = "unavailable" if all(pair.get(field) is None for field in fields) else "invalid"
        raise PriceError("provider has no valid canonical price denomination", category)
    evidence = _evidence(source, target, hashes)
    evidence["retrieved_at"] = datetime.fromtimestamp(now(), timezone.utc).isoformat().replace("+00:00", "Z")
    return {"schema_version": 1, "status": "partial" if errors else "ok", "values": values,
            "errors": errors, "evidence": evidence, "note": PROVIDERS[source]["label"] + ": " + NOTE}


def _failure(error):
    # Never publish exception text supplied by an injected transport or upstream body.
    return {"unavailable": "provider temporarily unavailable or has no quotes",
            "access": "provider access denied; permission controls are not bypassed",
            "identity": "provider canonical market identity could not be established",
            "invalid": "provider transport, schema, or bounded price data invalid"}.get(error.category, "provider request failed")


def _disagreement(selected, other):
    result = {}
    # Prices have at most 78 digits and 36 fractional digits. This also retains
    # tiny differences between large coefficients before rounding percentages.
    with localcontext() as context:
        context.prec = 240
        for identifier in selected.keys() & other.keys():
            primary, secondary = Decimal(selected[identifier]["value"]), Decimal(other[identifier]["value"])
            result[identifier] = format((abs(secondary - primary) / primary * 100).quantize(Decimal("0.0001")), "f")
    return result


def price(config, transport=None, now=None, monotonic=None):
    """Select one provider's quotes and gross mark; at most two bounded requests.

    Injectable transport(source, path, timeout, deadline, monotonic) returns bytes.
    Clocks return Unix seconds and monotonic seconds respectively.
    """
    config = _validate_input(config)
    target, hashes = _load_package()
    now, monotonic, transport = now or time.time, monotonic or time.monotonic, transport or _https
    deadline = monotonic() + 2 * REQUEST_TIMEOUT
    selected = "dexscreener" if config["source"] == "auto" else config["source"]
    primary_failure = None
    try:
        result = _observe(selected, target, hashes, transport, now, monotonic, deadline)
    except PriceError as error:
        if config["source"] != "auto" or error.category != "unavailable":
            raise PriceError(PROVIDERS[selected]["label"] + ": " + _failure(error), error.category) from None
        primary_failure = error
        selected = "geckoterminal"
        try:
            result = _observe(selected, target, hashes, transport, now, monotonic, deadline)
        except PriceError as fallback_error:
            raise PriceError("DEX Screener unavailable; GeckoTerminal fallback failed: " + _failure(fallback_error),
                             fallback_error.category) from None
        result["fallback"] = {"from": "DEX Screener", "to": "GeckoTerminal", "reason": _failure(error)}
        result["errors"]["primary_source"] = _failure(error)
        result["status"] = "partial"
        result["note"] = "GeckoTerminal fallback after DEX Screener was unavailable. " + NOTE
    if "standard_amount" in config:
        amount = config["standard_amount"]
        valuation = {"standard_amount": amount, "basis": BASIS}
        for identifier, field, unit in (("standard_usd", "gross_usd", "USD"), ("standard_eth", "gross_eth", "ETH")):
            if identifier in result["values"]:
                valuation[field] = {"value": _multiply(amount, result["values"][identifier]["value"]), "unit": unit}
        result["valuation"] = valuation
    if config["cross_check"]:
        other = "geckoterminal" if selected == "dexscreener" else "dexscreener"
        try:
            if primary_failure is not None:
                raise primary_failure
            secondary = _observe(other, target, hashes, transport, now, monotonic, deadline)
            comparison = {key: secondary[key] for key in ("status", "values", "evidence", "errors")}
            comparison["disagreement_percent"] = _disagreement(result["values"], secondary["values"])
        except PriceError as error:
            comparison = {"status": "unavailable", "values": {}, "evidence": _evidence(other, target, hashes),
                          "errors": {"request": _failure(error)}, "disagreement_percent": {}}
        comparison["provider"] = PROVIDERS[other]["label"]
        result["cross_check"] = comparison
        if comparison["status"] != "ok":
            result["status"] = "partial"
            result["errors"]["cross_check"] = "secondary provider unavailable or incomplete; selected quotes retained"
        result["note"] += (" Cross-check observations are not atomic or a guarantee of independent truth;"
                           " GeckoTerminal and CoinGecko are the same provider family. No quotes are blended.")
    return result


def _cli_config(arguments):
    if len(arguments) > 6 or any(len(value) > 80 for value in arguments):
        raise InputError("CLI accepts at most 6 arguments of at most 80 characters")
    config = {"schema_version": 1}
    seen = set()
    index = 0
    while index < len(arguments):
        flag = arguments[index]
        if flag not in ("--quote", "--amount-standard", "--source", "--cross-check") or flag in seen:
            raise InputError("unknown or repeated CLI flag")
        seen.add(flag)
        index += 1
        if flag in ("--amount-standard", "--source"):
            if index == len(arguments):
                raise InputError("CLI flag requires a value")
            config["standard_amount" if flag == "--amount-standard" else "source"] = arguments[index]
            index += 1
        elif flag == "--cross-check":
            config["cross_check"] = True
    if "--quote" in seen and "--amount-standard" in seen:
        raise InputError("--quote and --amount-standard are mutually exclusive")
    return config


def main():
    if sys.argv[1:] == ["--help"]:
        sys.stdout.write(__doc__ + "\n" + NOTE + "\n")
        return 0
    try:
        if len(sys.argv) > 1:
            config = _cli_config(sys.argv[1:])
        else:
            try:
                config = _json(sys.stdin.buffer.read(MAX_INPUT_BYTES + 1), MAX_INPUT_BYTES)
            except (ValueError, RecursionError):
                raise InputError("stdin must be bounded UTF-8 JSON without duplicate keys") from None
        result = price(config)
    except (InputError, PackageDataError, PriceError) as error:
        code, kind = (2, "invalid_input") if isinstance(error, InputError) else (4, "package_data_error") if isinstance(error, PackageDataError) else (5, "price_error")
        sys.stderr.write(json.dumps({"schema_version": 1, "error": {"type": kind, "message": str(error)}, "note": NOTE}) + "\n")
        return code
    sys.stdout.write(json.dumps(result, ensure_ascii=True, allow_nan=False, indent=2) + "\n")
    return 0


if __name__ == "__main__":
    sys.exit(main())
