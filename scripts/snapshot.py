#!/usr/bin/env python3
"""Read a fixed Robinhood RPC snapshot; Python standard library only.

With no arguments, supply JSON on stdin: {"schema_version":1,"view":"protocol"}.
Views: protocol, charter (requires integer charter_id), auctions, treasury, orderbook.
CLI: protocol|auctions [--detail summary|full]
     charter --id UINT256 [--detail summary|full|activity]
     treasury [--asset ADDRESS] [--detail summary|full]
     orderbook --start UINT256 --count 1..100 [--charter-ids CSV] [--detail summary|full]
Orderbook JSON requires start/count; optional charter_ids: at most 10 unique uint256s.
One page only. Returned IDs have unestablished semantics; never joined to charter IDs.
Selected charter bids/fillable are independent observations; bid prices retain raw units.
Treasury JSON accepts optional reserve_asset: one nonzero public asset address.
It is getter argument data only, never an eth_call target. Holdings use raw units.
CLI mode never reads stdin. UINT256 is 1..78 ASCII decimal digits in uint256 range.
Optional detail: summary (default) or full (raw RPC evidence and call mapping).
Activity detail is charter-only: owner, raw activity/transfer clocks and dormancy period.
No inferred dormancy deadline, eligibility or last-check-in time.
Flags must be exact, unrepeated, separate tokens; --help must stand alone.
RPC: SRSTACK_RPC_URL, otherwise ALCHEMY_API_KEY, otherwise free public RPC.
No wallet, signing, simulation, or filesystem writes.
Owner getters are observations, not a privilege audit.
"""

import base64
import hashlib
import http.client
import json
import math
import os
from pathlib import Path
import re
import socket
import stat
import sys
import threading
import time
from datetime import datetime, timezone
import unicodedata
from urllib.parse import parse_qsl, quote, unquote, urlsplit
import urllib.error
import urllib.request


RPC_URL = "https://rpc.mainnet.chain.robinhood.com/"
CHAIN_ID = 4663
NOTE = "RPC snapshot; publisher ABI."
MAX_INPUT_BYTES = 4096
MAX_FILE_BYTES = 65536
MAX_RESPONSE_BYTES = 1048576
MAX_DIAGNOSTIC_BYTES = 2048
DIAGNOSTIC_HEADERS = ("content-type", "server", "date", "via", "cf-ray", "retry-after",
                      "x-request-id", "x-correlation-id", "request-id", "x-amzn-requestid")
BATCH_SIZE = 20
REQUEST_TIMEOUT = 10
OVERALL_TIMEOUT = 40
MAX_BLOCK_AGE = 300
MAX_FUTURE_SECONDS = 30
UINT256_MAX = (1 << 256) - 1
PROFILES = {"protocol", "charter", "auctions", "treasury", "orderbook"}
MAX_ORDERBOOK_PAGE = 100
MAX_ORDERBOOK_CHARTERS = 10
ADDRESS = re.compile(r"0x[0-9a-fA-F]{40}\Z")
WORD = re.compile(r"0x[0-9a-fA-F]{64}\Z")
QUANTITY = re.compile(r"0x(?:0|[1-9a-fA-F][0-9a-fA-F]*)\Z")
IDENTIFIER = re.compile(r"[a-zA-Z][a-zA-Z0-9_]{0,79}\Z")
ZERO_ADDRESS = "0x" + "0" * 40
CHARTER_VALUES = frozenset(("charter_owner", "charter_branches", "charter_pending"))
CHARTER_RATE_CALLS = frozenset((
    "token_decimals", "emissions_started", "stream_rate_per_second", "total_branches"))
CHARTER_SUMMARY_CALLS = CHARTER_VALUES | CHARTER_RATE_CALLS
SCALAR_TYPES = frozenset(("uint256", "uint8", "uint24", "int24", "bool", "address"))
ASSET_GETTERS = frozenset(("isReserveAsset", "holdingsOf", "reservePool"))
ASSET_APPROVAL = "expansion_is_reserve_asset"
ASSET_DETAILS = frozenset(("expansion_holdings", "expansion_reserve_pool"))
INCENTIVES_BALANCE = "incentives_vault_standard_balance"
# Reviewed execution metadata, not a source/bytecode equivalence assertion.
# Changing the callable surface requires deliberate review and a new fingerprint.
CALLS_SHA256 = "bb3bbf086d799a02bdcb7c99288a701ada290bcfb9c04a204aac5bbb8af697e8"
ORDERBOOK_SHA256 = "5f959244f3e8f50c077c3e4f81e4c733a838e300c3b7b9abe281ba992875d0d4"
ACTIVITY_SHA256 = "96f08e8fee853ecefdaf117ece3813c9059169e59ca67f3ed19b89117afcc4a2"
RPC_CONFIGURATION_HINT = (
    "RPC configuration: SRSTACK_RPC_URL or ALCHEMY_API_KEY via host-managed environment only. "
    "No retry or failover was attempted.")


class InputError(ValueError):
    """Invalid bounded stdin or CLI configuration."""


class PackageDataError(ValueError):
    """Fixed packaged interface or entity data is unsafe or invalid."""


class SnapshotError(ValueError):
    """Transport, chain, or snapshot integrity could not be established."""

    def __init__(self, message, diagnostics=None):
        super().__init__(message)
        self.diagnostics = diagnostics


def _rpc_endpoint():
    """Select user infrastructure without exposing URL credentials in evidence."""
    key = os.environ.get("ALCHEMY_API_KEY", "")
    url = os.environ.get("SRSTACK_RPC_URL") or (
        "https://robinhood-mainnet.g.alchemy.com/v2/" + quote(key, safe="") if key else RPC_URL)
    try:
        parsed = urlsplit(url)
        if (parsed.scheme not in ("http", "https") or not parsed.hostname
                or parsed.fragment or any(character.isspace() or ord(character) < 32 or ord(character) == 127 for character in url)):
            raise ValueError
        port = parsed.port
    except ValueError:
        raise SnapshotError("invalid SRSTACK_RPC_URL; use an HTTP or HTTPS RPC URL") from None
    path = parsed.path or "/"
    target = path + ("?" + parsed.query if parsed.query else "")
    host = parsed.hostname
    authority = ("[" + host + "]") if ":" in host else host
    if port is not None:
        authority += ":" + str(port)
    label = RPC_URL if url == RPC_URL else parsed.scheme + "://" + authority + "/[REDACTED]"
    headers = {"Content-Type": "application/json", "Accept": "application/json"}
    secrets = {key, url if url != RPC_URL else ""}
    if url != RPC_URL:
        secrets.update(part for part in parsed.path.split("/") if part)
        secrets.update(value for _, value in parse_qsl(parsed.query, keep_blank_values=False))
        secrets.update(part.partition("=")[2] for part in parsed.query.split("&") if "=" in part)
    if parsed.username is not None:
        user, password = unquote(parsed.username), unquote(parsed.password or "")
        authorization = base64.b64encode((user + ":" + password).encode()).decode()
        headers["Authorization"] = "Basic " + authorization
        secrets.update((user, password, authorization))
    # Proxy authentication is host configuration, never output evidence.
    for proxy in urllib.request.getproxies().values():
        try:
            parsed_proxy = urlsplit(proxy if "://" in proxy else "http://" + proxy)
            if parsed_proxy.username is not None:
                user = unquote(parsed_proxy.username)
                password = unquote(parsed_proxy.password or "")
                authorization = base64.b64encode((user + ":" + password).encode()).decode()
                secrets.update((proxy, user, password, authorization))
        except ValueError:
            pass
    secrets.update(unquote(value) for value in tuple(secrets))
    secrets.update(quote(value, safe="") for value in tuple(secrets))
    secrets.update(json.dumps(value, ensure_ascii=True)[1:-1] for value in tuple(secrets))
    return {"url": parsed.scheme + "://" + authority + target,
            "headers": headers, "label": label, "secrets": tuple(sorted(secrets - {""}, key=len, reverse=True))}


def _redact_rpc(value, *, truncated=False):
    secrets = _rpc_endpoint()["secrets"]
    if not secrets:
        return value
    pattern = re.compile("|".join(re.escape(secret) for secret in secrets))

    def redact(item):
        if isinstance(item, str):
            cutoff = len(item)
            if truncated:
                # A bounded header/body may end partway through an echoed key.
                for secret in secrets:
                    for length in range(min(len(secret) - 1, len(item)), 0, -1):
                        if item.endswith(secret[:length]):
                            cutoff = min(cutoff, len(item) - length)
                            break
            clean = pattern.sub("[REDACTED]", item[:cutoff])
            return clean + ("[REDACTED]" if cutoff < len(item) else "")
        if isinstance(item, list):
            return [redact(child) for child in item]
        if isinstance(item, dict):
            return {redact(key): redact(child) for key, child in item.items()}
        return item

    return redact(value)


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
    if len(raw) > limit:
        raise ValueError("JSON exceeds byte limit")
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


def _keys(value, required, optional=()):
    if not isinstance(value, dict) or not set(required) <= value.keys() or value.keys() - set(required) - set(optional):
        raise ValueError("unexpected or missing fields")


def _integer(value, maximum=UINT256_MAX):
    return type(value) is int and 0 <= value <= maximum


def _validate_input(config):
    try:
        _keys(config, {"schema_version", "view"}, {"detail", "charter_id", "reserve_asset",
                                                 "start", "count", "charter_ids"})
        if type(config["schema_version"]) is not int or config["schema_version"] != 1:
            raise ValueError("unsupported schema_version")
        if not isinstance(config["view"], str) or config["view"] not in PROFILES:
            raise ValueError("unsupported view")
        if config.get("detail", "summary") not in ("summary", "full", "activity"):
            raise ValueError("unsupported detail")
        if config.get("detail") == "activity" and config["view"] != "charter":
            raise ValueError("activity detail is only accepted for charter view")
        if config["view"] == "charter":
            if not _integer(config.get("charter_id")):
                raise ValueError("charter requires a uint256 integer charter_id")
        elif "charter_id" in config:
            raise ValueError("charter_id is only accepted for charter view")
        if "reserve_asset" in config:
            asset = config["reserve_asset"]
            if config["view"] != "treasury":
                raise ValueError("reserve_asset is only accepted for treasury view")
            if not isinstance(asset, str) or not ADDRESS.fullmatch(asset) or asset.lower() == ZERO_ADDRESS:
                raise ValueError("reserve_asset requires one nonzero public asset address")
        order_fields = {"start", "count", "charter_ids"}
        if config["view"] == "orderbook":
            if not _integer(config.get("start")) or not _integer(config.get("count"), MAX_ORDERBOOK_PAGE) or config["count"] == 0:
                raise ValueError("orderbook requires uint256 start and count from 1 to 100")
            if config["start"] > UINT256_MAX - config["count"]:
                raise ValueError("orderbook start plus count exceeds uint256")
            identifiers = config.get("charter_ids", [])
            if (not isinstance(identifiers, list) or len(identifiers) > MAX_ORDERBOOK_CHARTERS
                    or not all(_integer(identifier) for identifier in identifiers)
                    or len(set(identifiers)) != len(identifiers)):
                raise ValueError("charter_ids requires at most 10 unique uint256 integers")
        elif order_fields & config.keys():
            raise ValueError("start, count and charter_ids are only accepted for orderbook view")
    except (ValueError, TypeError) as error:
        raise InputError(str(error)) from None
    result = dict(config, detail=config.get("detail", "summary"))
    if "reserve_asset" in result:
        result["reserve_asset"] = result["reserve_asset"].lower()
    return result


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


def _validate_output(field):
    if field["output_type"] not in SCALAR_TYPES or not _integer(field["decimals"], 18):
        raise ValueError("unsupported output")
    if field["output_type"] in ("bool", "address", "uint8", "uint24", "int24") and field["decimals"] != 0:
        raise ValueError("invalid scalar scaling")
    if not isinstance(field["unit"], str) or not re.fullmatch(r"[A-Za-z/-]{1,40}", field["unit"]):
        raise ValueError("invalid unit")


def _validate_package(interface, catalog):
    _keys(interface, {"schema_version", "chain_id", "rpc_url", "entity_catalog", "source_ids", "contracts", "calls", "limits", "publisher_bundle"})
    if (type(interface["schema_version"]) is not int or interface["schema_version"] != 2
            or type(interface["chain_id"]) is not int or interface["chain_id"] != CHAIN_ID
            or interface["rpc_url"] != RPC_URL or interface["entity_catalog"] != "assets/entities/robinhood.json"):
        raise ValueError("unsupported interface metadata")
    if not isinstance(interface["source_ids"], list) or not interface["source_ids"] or not all(isinstance(x, str) and IDENTIFIER.fullmatch(x.replace("-", "_")) for x in interface["source_ids"]):
        raise ValueError("invalid interface sources")
    if not isinstance(interface["limits"], list) or not all(isinstance(x, str) and 0 < len(x) <= 1024 for x in interface["limits"]):
        raise ValueError("invalid interface limits")
    bundle = interface["publisher_bundle"]
    _keys(bundle, {"url", "sha256", "retrieved_at"})
    if (not isinstance(bundle["url"], str) or not bundle["url"].startswith("https://www.standardreserve.xyz/assets/")
            or not isinstance(bundle["sha256"], str) or not re.fullmatch(r"[0-9a-f]{64}", bundle["sha256"])
            or not isinstance(bundle["retrieved_at"], str) or len(bundle["retrieved_at"]) > 40):
        raise ValueError("invalid publisher metadata")
    contracts = interface["contracts"]
    if not isinstance(contracts, dict) or len(contracts) != 16 or not all(isinstance(k, str) and IDENTIFIER.fullmatch(k) and isinstance(v, str) for k, v in contracts.items()):
        raise ValueError("invalid contracts")
    calls = interface["calls"]
    if not isinstance(calls, list) or not 1 <= len(calls) <= 144:
        raise ValueError("invalid call count")
    seen = set()
    required = {"id", "contract", "function", "signature", "mutability", "input_types", "args", "output_type", "decimals", "unit", "profiles", "selector"}
    for call in calls:
        _keys(call, required, {"binds_to", "components", "binding_profiles"})
        identifier = call["id"]
        if not isinstance(identifier, str) or not IDENTIFIER.fullmatch(identifier) or identifier in seen:
            raise ValueError("invalid or duplicate call id")
        seen.add(identifier)
        if call["contract"] not in contracts or call["mutability"] not in ("view", "pure"):
            raise ValueError("unsupported contract or mutability")
        types, args = call["input_types"], call["args"]
        if not isinstance(types, list) or not isinstance(args, list) or len(types) != len(args) or len(types) > 1:
            raise ValueError("invalid call arguments")
        for kind, argument in zip(types, args):
            if kind == "bool":
                valid = type(argument) is bool
            elif kind in ("uint256", "uint8"):
                valid = _integer(argument, 255 if kind == "uint8" else UINT256_MAX) or (kind == "uint256" and argument == "$charter_id")
            elif kind == "address":
                valid = types == ["address"] and call["profiles"] == ["treasury"] and (
                    (argument == "$reserve_asset" and call["contract"] == "expansionVault"
                     and call["function"] in ASSET_GETTERS)
                    or (identifier == INCENTIVES_BALANCE and call["contract"] == "standard"
                        and call["function"] == "balanceOf" and isinstance(argument, str)
                        and ADDRESS.fullmatch(argument)))
            else:
                valid = False
            if not valid:
                raise ValueError("unsupported argument")
        if (not isinstance(call["function"], str) or not IDENTIFIER.fullmatch(call["function"])
                or call["signature"] != call["function"] + "(" + ",".join(types) + ")"
                or not isinstance(call["selector"], str) or not re.fullmatch(r"0x[0-9a-f]{8}", call["selector"])):
            raise ValueError("invalid function or selector")
        if call["output_type"] == "tuple":
            components = call.get("components")
            if (call["decimals"] != 0 or call["unit"] not in ("queued-policy", "pool-key")
                    or not isinstance(components, list) or not 2 <= len(components) <= 5):
                raise ValueError("invalid static tuple")
            names = set()
            for component in components:
                _keys(component, {"name", "output_type", "decimals", "unit"})
                name = component["name"]
                if not isinstance(name, str) or not IDENTIFIER.fullmatch(name) or name in names:
                    raise ValueError("invalid tuple component name")
                names.add(name)
                _validate_output(component)
        else:
            if "components" in call:
                raise ValueError("scalar cannot have tuple components")
            _validate_output(call)
        profiles = call["profiles"]
        if not isinstance(profiles, list) or not all(isinstance(x, str) and x in PROFILES for x in profiles) or len(set(profiles)) != len(profiles):
            raise ValueError("invalid profiles")
        if "$charter_id" in args and profiles != ["charter"]:
            raise ValueError("charter input outside charter profile")
        if "binds_to" in call:
            if call["binds_to"] not in contracts or profiles or types or call["output_type"] != "address":
                raise ValueError("invalid binding")
            scoped = call.get("binding_profiles")
            if scoped is not None and (not isinstance(scoped, list) or not scoped
                    or not all(isinstance(x, str) and x in PROFILES for x in scoped)
                    or len(set(scoped)) != len(scoped)):
                raise ValueError("invalid binding profiles")
        elif not profiles:
            raise ValueError("call lacks profile")
        if "binding_profiles" in call and "binds_to" not in call:
            raise ValueError("binding profiles require a binding")
    fingerprint = hashlib.sha256(json.dumps({k: interface[k] for k in ("contracts", "calls")}, sort_keys=True, separators=(",", ":")).encode()).hexdigest()
    if fingerprint != CALLS_SHA256:
        raise ValueError("unreviewed callable metadata")
    if (not isinstance(catalog, dict) or type(catalog.get("schema_version")) is not int or catalog["schema_version"] != 1
            or not isinstance(catalog.get("chain"), dict) or type(catalog["chain"].get("id")) is not int or catalog["chain"]["id"] != CHAIN_ID
            or not isinstance(catalog.get("records"), list) or not 1 <= len(catalog["records"]) <= 100):
        raise ValueError("invalid entity catalog")
    entities, addresses = {}, set()
    for record in catalog["records"]:
        if (not isinstance(record, dict) or not isinstance(record.get("id"), str) or record["id"] in entities
                or type(record.get("chain_id")) is not int or record["chain_id"] != CHAIN_ID
                or not isinstance(record.get("address"), str) or not ADDRESS.fullmatch(record["address"])
                or record["address"].lower() == ZERO_ADDRESS or record["address"].lower() in addresses):
            raise ValueError("invalid or duplicate entity")
        entities[record["id"]] = record["address"].lower()
        addresses.add(record["address"].lower())
    if not set(contracts.values()) <= entities.keys():
        raise ValueError("missing contract entity")
    if any(call["args"][0].lower() != entities[contracts["incentivesVault"]]
           for call in calls if call["id"] == INCENTIVES_BALANCE):
        raise ValueError("incentives balance argument does not match fixed catalog")
    return {role: entities[identifier] for role, identifier in contracts.items()}


def _load_package(orderbook=False, activity=False):
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
        loaded, hashes = [], {}
        for folder, filename in (("interfaces", "robinhood-reads.json"), ("entities", "robinhood.json")):
            directory = _directory(assets, folder)
            descriptors.append(directory)
            data, digest = _read_file(directory, filename)
            loaded.append(data)
            hashes["assets/" + folder + "/" + filename] = digest
        interface, catalog = loaded
        if activity:
            directory = _directory(assets, "interfaces")
            descriptors.append(directory)
            data, digest = _read_file(directory, "charter-activity-reads.json")
            fingerprint = hashlib.sha256(json.dumps(data, sort_keys=True, separators=(",", ":")).encode()).hexdigest()
            if fingerprint != ACTIVITY_SHA256:
                raise ValueError("unreviewed charter activity interface")
            addresses = _validate_package(interface, catalog)
            for role, record in data["contracts"].items():
                if (record["entity_id"] != interface["contracts"][role]
                        or record["address"].lower() != addresses[role]):
                    raise ValueError("activity target does not match fixed catalog")
            interface["activity"] = data
            hashes["assets/interfaces/charter-activity-reads.json"] = digest
            return interface, addresses, hashes
        if orderbook:
            directory = _directory(assets, "interfaces")
            descriptors.append(directory)
            data, digest = _read_file(directory, "v1-2-orderbook-reads.json")
            keys = ("schema_version", "chain_id", "entity_id", "address", "source_ids",
                    "publisher_evidence", "selectors", "reads")
            fingerprint = hashlib.sha256(json.dumps({key: data[key] for key in keys},
                                                    sort_keys=True, separators=(",", ":")).encode()).hexdigest()
            if fingerprint != ORDERBOOK_SHA256 or data["entity_id"] != interface["contracts"]["licenseAuction"]:
                raise ValueError("unreviewed orderbook interface")
            # Main metadata is validated before adding a separate, reviewed surface.
            addresses = _validate_package(interface, catalog)
            if addresses["licenseAuction"] != data["address"].lower():
                raise ValueError("orderbook target does not match fixed catalog")
            interface["orderbook"] = data
            hashes["assets/interfaces/v1-2-orderbook-reads.json"] = digest
            return interface, addresses, hashes
        return interface, _validate_package(interface, catalog), hashes
    except (OSError, ValueError, TypeError, KeyError, RecursionError, RuntimeError):
        raise PackageDataError("fixed bundled interface or entity data is missing, unsafe, or invalid") from None
    finally:
        for descriptor in reversed(descriptors):
            os.close(descriptor)



def _orderbook_calls(data, config):
    calls = []

    def add(function, identifier, arguments):
        abi = next(item for item in data["reads"] if item["name"] == function)
        types = [item["type"] for item in abi["inputs"]]
        signature = function + "(" + ",".join(types) + ")"
        outputs = abi["outputs"]
        call = {"id": identifier, "contract": "licenseAuction", "function": function,
                "signature": signature, "input_types": types, "args": arguments,
                "selector": data["selectors"][signature], "decimals": 0,
                "unit": "orders" if function == "openBidCount" else "boolean" if function == "fillable" else "raw",
                "output_type": "tuple" if len(outputs) > 1 else outputs[0]["type"]}
        if call["output_type"] == "tuple":
            call["components"] = [{"name": field["name"], "output_type": field["type"],
                                   "decimals": 0, "unit": "address" if field["type"] == "address" else "raw"}
                                  for field in outputs]
        if function == "openBids":
            call["max_items"] = config["count"]
        calls.append(call)

    add("openBidCount", "license_open_bid_count", [])
    add("openBids", "orderbook_page", [config["start"], config["count"]])
    for index, charter_id in enumerate(config.get("charter_ids", [])):
        add("bids", "orderbook_bid_" + str(index), [charter_id])
        add("fillable", "orderbook_fillable_" + str(index), [charter_id])
    return calls

def _diagnostic_text(text, limit):
    """Bound untrusted response text; never expose common credential material."""
    text = _redact_rpc(text, truncated=True)
    text = re.sub(r"\x1b(?:\[[0-?]*[ -/]*[@-~]|\][^\x07\x1b]*(?:\x07|\x1b\\))", "", text)
    text = "".join(character for character in text if not unicodedata.category(character).startswith("C"))
    text = re.sub(r"(?i)\b(?:bearer|basic)\s+[^\s\"'<>;,]+", "[REDACTED]", text)
    text = re.sub(
        r"""(?i)\b(?:authorization|cookie|set-cookie|(?:access[_-]?|refresh[_-]?)?token|api[_-]?key|password|secret|private[_-]?key)\b["']?\s*[:=]\s*(?:"[^"]*(?:"|$)|'[^']*(?:'|$)|[^\s<>,;]+)""",
        "[REDACTED]", text)
    text = re.sub(r"\beyJ[A-Za-z0-9_-]+\.[A-Za-z0-9_-]+(?:\.[A-Za-z0-9_-]*)?", "[REDACTED]", text)
    text = re.sub(r"\b(?:0x)?[0-9a-fA-F]{64}\b", "[REDACTED]", text)
    return text.encode("utf-8")[:limit].decode("utf-8", errors="ignore")


class _NoRedirect(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, request, response, code, message, headers, new_url):
        return None


def _response_socket(response):
    # urllib HTTPError wraps an HTTPResponse; success exposes it directly.
    stream = response.fp if isinstance(response, urllib.error.HTTPError) else response
    return getattr(getattr(getattr(stream, "fp", None), "raw", None), "_sock", None)


def _read_timeout(response, remaining):
    connection = _response_socket(response)
    if connection is not None:
        connection.settimeout(min(REQUEST_TIMEOUT, remaining))


def _http_failure(response, deadline, monotonic, failure):
    diagnostics = {"http_status": response.status, "endpoint": _rpc_endpoint()["label"], "headers": {},
                   "response_excerpt": "", "excerpt_bytes": 0, "truncated": True,
                   "read_error": None, "untrusted_response": True, "cause": "unconfirmed"}
    if response.status in (401, 403):
        diagnostics["configuration_hint"] = RPC_CONFIGURATION_HINT
    message = ("endpoint denied this request" if response.status in (401, 403)
               else "RPC HTTP request failed; redirects are not followed")
    error = SnapshotError(message, diagnostics)
    # Publish status before reading diagnostic headers/body, so the outer hard
    # deadline can still report the original response if its body stalls.
    if failure is not None:
        failure.append(error)
    chunks, size = [], 0
    try:
        header_bytes = 0
        for name in DIAGNOSTIC_HEADERS:
            value = response.headers.get(name)
            remaining_header = MAX_DIAGNOSTIC_BYTES - header_bytes - len(name)
            if remaining_header <= 0:
                break
            if value is not None:
                value = _diagnostic_text(value, min(256, remaining_header))
                diagnostics["headers"][name] = value
                header_bytes += len(name) + len(value.encode("utf-8"))
        length = response.headers.get("Content-Length")
        expected = int(length) if length is not None and len(length) <= 20 and length.isascii() and length.isdecimal() else None
        while size <= MAX_DIAGNOSTIC_BYTES:
            remaining = deadline - monotonic()
            if remaining <= 0:
                diagnostics["read_error"] = "request deadline exceeded"
                break
            _read_timeout(response, remaining)
            chunk = response.read1(MAX_DIAGNOSTIC_BYTES + 1 - size)
            if not chunk:
                diagnostics["truncated"] = expected is not None and size < expected
                if diagnostics["truncated"]:
                    diagnostics["read_error"] = "response body unavailable or incomplete"
                break
            chunks.append(chunk)
            size += len(chunk)
            excerpt = _diagnostic_text(b"".join(chunks)[:MAX_DIAGNOSTIC_BYTES].decode("utf-8", errors="replace"),
                                       MAX_DIAGNOSTIC_BYTES)
            diagnostics.update(response_excerpt=excerpt, excerpt_bytes=len(excerpt.encode("utf-8")))
    except (OSError, http.client.HTTPException):
        diagnostics["read_error"] = "response body unavailable or incomplete"
    raise error


def _https_request(opener, payload, deadline, monotonic, failure=None, endpoint=None, active=None):
    """Read one bounded response using the host's normal urllib proxy handling."""
    endpoint = endpoint or _rpc_endpoint()
    response = None
    try:
        remaining = deadline - monotonic()
        if remaining <= 0:
            raise SnapshotError("RPC request deadline exceeded before sending")
        request = urllib.request.Request(endpoint["url"], data=payload,
                                         headers=endpoint["headers"], method="POST")
        try:
            response = opener.open(request, timeout=min(REQUEST_TIMEOUT, remaining))
        except urllib.error.HTTPError as error:
            response = error
        if active is not None:
            active.append(response)
        if response.status != 200:
            _http_failure(response, deadline, monotonic, failure)
        length = response.headers.get("Content-Length")
        if length is not None and (len(length) > 20 or not length.isascii()
                                   or not length.isdecimal() or int(length) > MAX_RESPONSE_BYTES):
            raise SnapshotError("RPC response exceeds byte limit")
        chunks, size = [], 0
        while size <= MAX_RESPONSE_BYTES:
            remaining = deadline - monotonic()
            if remaining <= 0:
                raise SnapshotError("snapshot deadline exceeded")
            _read_timeout(response, remaining)
            chunk = response.read1(min(65536, MAX_RESPONSE_BYTES + 1 - size))
            if not chunk:
                break
            chunks.append(chunk)
            size += len(chunk)
        if size > MAX_RESPONSE_BYTES:
            raise SnapshotError("RPC response exceeds byte limit")
        if length is not None and size != int(length):
            raise SnapshotError("incomplete RPC response")
        return b"".join(chunks)
    except (OSError, http.client.HTTPException):
        raise SnapshotError("RPC transport failed") from None
    finally:
        if response is not None:
            response.close()


def _https(payload, timeout, deadline, monotonic):
    """Bound proxy-aware DNS, TLS, headers and body without redirects or retries."""
    timeout = min(timeout, deadline - monotonic())
    if timeout <= 0:
        raise SnapshotError("snapshot deadline exceeded")
    endpoint = _rpc_endpoint()
    opener = urllib.request.build_opener(_NoRedirect())
    request_deadline = min(deadline, monotonic() + timeout)
    finished = threading.Event()
    outcome, failure, active = [], [], []

    def request():
        try:
            outcome.append(_https_request(opener, payload, request_deadline, monotonic, failure, endpoint, active))
        except Exception as error:
            outcome.append(error)
        finally:
            finished.set()

    # DNS is not reliably bounded by socket timeouts. A daemon worker lets the
    # CLI terminate on deadline even if the host resolver does not return.
    worker = threading.Thread(target=request, daemon=True)
    worker.start()
    if not finished.wait(timeout):
        connection = _response_socket(active[0]) if active else None
        if connection is not None:
            try:
                connection.shutdown(socket.SHUT_RDWR)
            except OSError:
                pass
        if failure:
            diagnostics = dict(failure[0].diagnostics)
            diagnostics["headers"] = dict(diagnostics["headers"])
            diagnostics.update(truncated=True, read_error="request deadline exceeded")
            raise SnapshotError(str(failure[0]), diagnostics)
        raise SnapshotError("RPC request deadline exceeded")
    if isinstance(outcome[0], Exception):
        if isinstance(outcome[0], SnapshotError):
            raise outcome[0]
        raise SnapshotError("RPC transport failed") from None
    return outcome[0]


class _RPC:
    def __init__(self, transport, monotonic, full):
        self.transport = transport
        self.monotonic = monotonic
        self.deadline = monotonic() + OVERALL_TIMEOUT
        self.next_id = 1
        self.full = full
        self.exchanges = []

    def batch(self, requests):
        results = []
        for offset in range(0, len(requests), BATCH_SIZE):
            batch = []
            for method, params in requests[offset:offset + BATCH_SIZE]:
                batch.append({"jsonrpc": "2.0", "id": self.next_id, "method": method, "params": params})
                self.next_id += 1
            remaining = self.deadline - self.monotonic()
            if remaining <= 0:
                raise SnapshotError("snapshot deadline exceeded")
            try:
                raw = self.transport(json.dumps(batch, separators=(",", ":")).encode(), min(REQUEST_TIMEOUT, remaining), self.deadline, self.monotonic)
                if self.monotonic() > self.deadline:
                    raise SnapshotError("snapshot deadline exceeded")
                response = _json(raw, MAX_RESPONSE_BYTES)
                if not isinstance(response, list) or len(response) > len(batch):
                    raise ValueError("invalid batch response")
                expected = {request["id"] for request in batch}
                by_id = {}
                for item in response:
                    if (not isinstance(item, dict) or item.get("jsonrpc") != "2.0" or type(item.get("id")) is not int
                            or item["id"] not in expected or item["id"] in by_id
                            or ("result" in item) == ("error" in item)):
                        raise ValueError("invalid RPC envelope")
                    by_id[item["id"]] = item
                for request in batch:
                    item = by_id.get(request["id"])
                    results.append((item["result"], None) if item is not None and "result" in item else (None, "RPC field unavailable"))
                if self.full:
                    self.exchanges.append({"requests": batch, "responses": _redact_rpc(response)})
            except (OSError, ValueError, TypeError, RecursionError) as error:
                if isinstance(error, SnapshotError):
                    raise
                raise SnapshotError("invalid or unavailable RPC response") from None
        return results

    def one(self, method, params):
        value, error = self.batch([(method, params)])[0]
        if error:
            raise SnapshotError("required RPC metadata unavailable")
        return value


def _quantity(value):
    if not isinstance(value, str) or len(value) > 66 or not QUANTITY.fullmatch(value):
        raise SnapshotError("invalid RPC quantity")
    return int(value, 16)


def _block(value, now):
    if not isinstance(value, dict) or not isinstance(value.get("hash"), str) or not WORD.fullmatch(value["hash"]):
        raise SnapshotError("invalid block metadata")
    number = _quantity(value.get("number"))
    timestamp = _quantity(value.get("timestamp"))
    age = now() - timestamp
    if age > MAX_BLOCK_AGE or age < -MAX_FUTURE_SECONDS:
        raise SnapshotError("RPC block is stale or future-dated")
    return number, value["hash"].lower(), timestamp


def _decode(value, kind):
    if not isinstance(value, str) or not WORD.fullmatch(value):
        raise ValueError("invalid scalar ABI word")
    number = int(value, 16)
    if kind == "bool":
        if number not in (0, 1):
            raise ValueError("invalid ABI boolean")
        return bool(number)
    if kind == "address":
        if number >= 1 << 160:
            raise ValueError("invalid ABI address padding")
        return "0x" + value[-40:].lower()
    if kind in ("uint8", "uint24"):
        if number >= 1 << (8 if kind == "uint8" else 24):
            raise ValueError("invalid unsigned ABI padding")
    elif kind == "int24":
        signed = number if number < 1 << 255 else number - (1 << 256)
        if not -(1 << 23) <= signed < 1 << 23:
            raise ValueError("invalid ABI int24 sign extension")
        return signed
    elif kind != "uint256":
        raise ValueError("unsupported scalar ABI type")
    return number


def _decode_result(value, call):
    if call["output_type"] == "uint256[]":
        maximum = call["max_items"]
        if (not isinstance(value, str) or not 130 <= len(value) <= 130 + 64 * maximum
                or not re.fullmatch(r"0x[0-9a-fA-F]+", value) or (len(value) - 2) % 64):
            raise ValueError("invalid dynamic array ABI size")
        if int(value[2:66], 16) != 32:
            raise ValueError("invalid dynamic array ABI offset")
        count = int(value[66:130], 16)
        if count > maximum or len(value) != 130 + 64 * count:
            raise ValueError("invalid dynamic array ABI count")
        return [int(value[offset:offset + 64], 16) for offset in range(130, len(value), 64)]
    if call["output_type"] != "tuple":
        return _decode(value, call["output_type"])
    components = call["components"]
    if (not isinstance(value, str) or len(value) != 2 + 64 * len(components)
            or not re.fullmatch(r"0x[0-9a-fA-F]+", value)):
        raise ValueError("invalid static tuple ABI result")
    return {component["name"]: _decode("0x" + value[2 + index * 64:2 + (index + 1) * 64],
                                       component["output_type"])
            for index, component in enumerate(components)}


def _normalized(value, call):
    if call["output_type"] != "tuple":
        return {"value": _scaled(value, call["decimals"]), "unit": call["unit"]}
    return {"type": "tuple", "unit": call["unit"],
            "value": {component["name"]: dict(_normalized(value[component["name"]], component),
                                              type=component["output_type"])
                      for component in call["components"]}}


def _scaled(value, decimals):
    if not decimals:
        return value
    whole, fraction = divmod(value, 10 ** decimals)
    return str(whole) + (("." + str(fraction).zfill(decimals).rstrip("0")) if fraction else "")


def _calldata(call, config):
    result = call["selector"]
    for kind, argument in zip(call["input_types"], call["args"]):
        if argument == "$charter_id":
            argument = config["charter_id"]
        elif argument == "$charter_owner":
            argument = config["charter_owner"]
        elif argument == "$reserve_asset":
            argument = config["reserve_asset"]
        result += format(int(argument, 16) if kind == "address" else int(argument), "064x")
    return result


def _license_opening_preview(raw, values, context, status):
    """A documented-policy calculation, not a next-round quote or enforcement proof."""
    identifiers = ("license_current_round", "license_sold", "license_last_sale_round",
                   "license_last_sale_price", "license_round_floor", "license_start_multiplier")
    preview = {
        "status": "unknown", "basis": "documented_policy_not_contract_enforcement",
        "auction_status": status,
        "policy": {
            "multiplier": 2,
            "with_sales": "2 * final_sale_price, subject to the next round floor; exact clamp unverified",
            "without_sales": "2 * next_round_floor",
            "source_urls": [
                "https://www.standardreserve.xyz/app/protocol/whitepaper/#branches",
                "https://www.standardreserve.xyz/app/protocol/whitepaper/#auctions",
            ],
        },
        "round_context": context, "target_round": None, "sale_basis": "unknown",
        "candidate": None,
        "inputs": {identifier: {"raw": str(raw[identifier]), "value": values[identifier]["value"],
                                "unit": values[identifier]["unit"]}
                   for identifier in identifiers if identifier in values},
        "multiplier_comparison": "unavailable",
        "assumptions": [],
        "unknown_reasons": ["next_round_floor_unavailable", "contract_policy_enforcement_unverified",
                            "start_multiplier_consumption_unverified"],
    }
    reasons = preview["unknown_reasons"]
    multiplier = raw["license_start_multiplier"] if "license_start_multiplier" in values else None
    if multiplier is not None:
        preview["multiplier_comparison"] = "matches_published" if multiplier == 2 else "differs_from_published"
    if multiplier != 2:
        reasons.append("start_multiplier_unavailable" if multiplier is None
                       else "start_multiplier_differs_from_published_policy")
    if context != "aligned":
        reasons.append("round_context_" + context)
        return preview
    preview["target_round"] = str(raw["license_current_round"] + 1)
    if status == "unknown":
        reasons.append("auction_availability_unavailable")
        return preview
    if "license_sold" not in values:
        reasons.append("sold_count_unavailable")
        return preview
    if raw["license_sold"] == 0:
        # A stale lastSaleDay alone cannot establish a no-sale round. Even this
        # aligned soldToday observation is not a log-authenticated round recap.
        preview["sale_basis"] = "getter_reported_no_sales"
        reasons.append("final_round_sales_unknown")
        return preview
    missing = [identifier for identifier in ("license_last_sale_round", "license_last_sale_price")
               if identifier not in values]
    if missing:
        reasons.extend(identifier + "_unavailable" for identifier in missing)
        return preview
    if raw["license_last_sale_round"] != raw["license_current_round"]:
        reasons.append("last_sale_round_mismatch")
        return preview
    if raw["license_last_sale_price"] == 0:
        reasons.append("last_sale_price_not_positive")
        return preview
    sold_out = status == "sold_out"
    preview["sale_basis"] = "getter_reported_sold_out_last_sale" if sold_out else "provisional_latest_sale"
    reasons.append("closing_sale_finality_not_independently_verified" if sold_out else "final_closing_sale_unknown")
    if multiplier != 2:
        return preview
    candidate = 2 * raw["license_last_sale_price"]
    preview["status"] = "conditional"
    preview["candidate"] = {
        "raw": str(candidate), "value": _scaled(candidate, 18), "unit": "STANDARD",
        "basis": "twice_last_sale_before_unknown_next_floor",
    }
    preview["assumptions"] = ["published_policy_applies_to_next_round"]
    if sold_out:
        preview["assumptions"].append("sold_out_getter_and_matching_sale_round_identify_final_sale")
    else:
        preview["assumptions"].append("latest_observed_sale_remains_final_sale_for_stored_round")
    return preview


def _derive(config, raw, values, errors, timestamp):
    derived = {}

    def amount(identifier, value, unit="STANDARD"):
        derived[identifier] = {"value": _scaled(value, 18), "unit": unit}

    def available(*identifiers):
        return all(identifier in values for identifier in identifiers)

    active_stream = available("stream_rate_per_second", "emissions_started") and raw["emissions_started"] is True
    if active_stream and not (config["view"] == "charter" and config["detail"] == "summary"):
        amount("global_gross_daily", raw["stream_rate_per_second"] * 86400, "STANDARD/day")
    for result, high, low in (("remaining_gross_budget", "issuance_budget", "cumulative_issued"), ("permanent_removed", "token_hard_cap", "token_max_supply")):
        if available(high, low):
            if raw[high] >= raw[low]:
                amount(result, raw[high] - raw[low])
            else:
                errors[result] = "inconsistent supply or issuance bounds"
    if available("token_hard_cap", "token_max_supply", "token_burned_forever", "token_ledger_retired"):
        if raw["token_hard_cap"] != raw["token_max_supply"] + raw["token_burned_forever"] + raw["token_ledger_retired"]:
            # Keep observed fields; do not substitute a sum for the existing cap difference.
            derived.pop("permanent_removed", None)
            errors["permanent_removed"] = "permanent burn and retirement totals do not reconcile with supply cap"
    if config["view"] == "charter":
        if not available("charter_owner") or raw["charter_owner"] == ZERO_ADDRESS:
            errors.setdefault("charter_owner", "charter ownership unavailable")
            values.pop("charter_owner", None)
            dependent_values = ("owner_last_active", "charter_last_transferred") if config["detail"] == "activity" else ("charter_branches", "charter_pending")
            for identifier in dependent_values:
                values.pop(identifier, None)
                errors[identifier] = "valid charter owner required"
        elif active_stream and available("charter_branches", "total_branches"):
            total, branches = raw["total_branches"], raw["charter_branches"]
            if total > 0 and branches <= total:
                amount("charter_gross_daily", (raw["stream_rate_per_second"] * branches * 86400) // total, "STANDARD/day")
            else:
                errors["charter_gross_daily"] = "positive total branches and consistent charter branches required"
        if config["detail"] == "activity":
            derived["charter_activity"] = {
                "basis": "publisher_abi_raw_observations",
                "owner_wallet": raw["charter_owner"] if available("charter_owner") else None,
                "dormancy_status": "unknown", "deadline": None, "last_check_in": None,
                "unknown_reasons": [
                    "timestamp_and_period_units_unverified",
                    "deployed_reset_and_transfer_grace_semantics_unverified",
                    "lastActive_is_not_a_checkIn_specific_timestamp",
                ],
            }
    if config["view"] == "auctions":
        for prefix in ("license", "charter_auction"):
            started, paused, remaining = (prefix + suffix for suffix in ("_started", "_paused", "_remaining"))
            is_license = prefix == "license"
            current = prefix + "_current_round"
            last = prefix + "_last_sale_round"
            period = prefix + "_round_seconds"
            anchor = "license_auction_anchor" if is_license else "charter_auction_anchor"
            context_id = prefix + "_round_context"
            context = "unknown"
            if available(started):
                if not raw[started]:
                    context = "not_started"
                elif available(current, period, anchor):
                    if raw[period] == 0 or raw[anchor] == 0 or raw[anchor] > timestamp:
                        errors[context_id] = "positive period and nonzero anchor at or before the snapshot block required"
                    else:
                        elapsed = (timestamp - raw[anchor]) // raw[period]
                        derived[prefix + "_elapsed_round"] = {"value": str(elapsed), "unit": "auction-round"}
                        stored = raw[current]
                        context = "aligned" if stored == elapsed else "rollover_pending" if stored < elapsed else "stored_ahead"
                        derived[prefix + "_stored_round_stale"] = {"value": stored != elapsed, "unit": "boolean"}
                        derived[prefix + "_rollover_pending"] = {"value": stored < elapsed, "unit": "boolean"}
                        round_start = raw[anchor] + elapsed * raw[period]
                        stored_end = raw[anchor] + (stored + 1) * raw[period]
                        pending = stored < elapsed
                        derived[prefix + "_schedule"] = {
                            "basis": "anchor_period_block_timestamp", "round_context": context,
                            "unit": "unix-seconds",
                            "anchor_timestamp": raw[anchor], "period_seconds": raw[period],
                            "block_timestamp": timestamp, "stored_round": str(stored),
                            "elapsed_round": str(elapsed), "elapsed_round_start_timestamp": round_start,
                            "next_boundary_timestamp": round_start + raw[period],
                            "seconds_until_next_boundary": round_start + raw[period] - timestamp,
                            "stored_round_end_timestamp": stored_end,
                            "due_boundary_timestamp": stored_end if pending else None,
                            "latest_due_boundary_timestamp": round_start if pending else None,
                            "seconds_since_due_boundary": timestamp - stored_end if pending else None,
                            "pending_rounds": str(elapsed - stored) if pending else "0",
                            "keeper_execution_timestamp": None,
                            "note": "Scheduled boundaries assume unchanged anchor and period; not keeper transaction times.",
                        }
                        if stored > elapsed:
                            errors[context_id] = "stored round exceeds elapsed round at the snapshot block"
            derived[context_id] = {"value": context, "unit": "status"}
            status = "unknown"
            if available(started, paused, remaining):
                status = "not_started" if not raw[started] else "paused" if raw[paused] else "sold_out" if raw[remaining] == 0 else "open"
                derived[prefix + "_status"] = {"value": status, "unit": "status",
                                               "basis": "contract_availability_getters", "round_context": context}
            price = prefix + "_current_price"
            if status != "open":
                # Raw getter results remain inspectable in full RPC evidence only.
                values.pop(price, None)
            # Availability getters may already use the elapsed round while stored
            # counters lag. Keep the live price observation, never an old closing recap.
            for identifier in (current, prefix + "_sold", prefix + "_round_cap", prefix + "_round_floor"):
                if identifier in values:
                    values[identifier]["round_context"] = context
            for identifier in (remaining, price):
                if identifier in values:
                    values[identifier]["basis"] = "contract_availability_getter"
                    values[identifier]["round_context"] = context
            if is_license or config["detail"] == "full":
                for identifier in (prefix + "_last_sale_price", last):
                    if identifier in values:
                        values[identifier]["not_historical"] = True
                        values[identifier]["round_context"] = context
                if config["detail"] == "full" and context == "aligned" and status == "sold_out" and available(prefix + "_last_sale_price", last, current):
                    if raw[last] == raw[current]:
                        derived[prefix + "_closing_price"] = dict(values[prefix + "_last_sale_price"])
            if is_license:
                derived["license_next_opening_preview"] = _license_opening_preview(raw, values, context, status)
    return derived


def snapshot(config, transport=None, now=None, monotonic=None):
    """Read a snapshot; injectable clocks/byte transport support offline checks."""
    config = _validate_input(config)
    interface, addresses, hashes = _load_package(orderbook=config["view"] == "orderbook",
                                                activity=config["detail"] == "activity")
    now = now or time.time
    rpc = _RPC(transport or _https, monotonic or time.monotonic, config["detail"] == "full")
    if _quantity(rpc.one("eth_chainId", [])) != CHAIN_ID:
        raise SnapshotError("RPC chain mismatch")
    number, block_hash, timestamp = _block(rpc.one("eth_getBlockByNumber", ["latest", False]), now)
    tag = hex(number)
    selected = [call for call in interface["calls"] if config["view"] in call["profiles"]
                and ("$reserve_asset" not in call["args"] or "reserve_asset" in config)]
    if config["view"] == "orderbook":
        selected = _orderbook_calls(interface["orderbook"], config)
    if config["detail"] == "activity":
        selected = [call for call in selected if call["id"] == "charter_owner"] + interface["activity"]["calls"]
    if config["detail"] == "summary":
        if config["view"] == "charter":
            selected = [call for call in selected if call["id"] in CHARTER_SUMMARY_CALLS]
        elif config["view"] == "auctions":
            selected = [call for call in selected if not call["id"].startswith("charter_auction_last_sale_")]
    roles = {call["contract"] for call in selected}
    all_bindings = [call for call in interface["calls"] if "binds_to" in call
                    and config["view"] in call.get("binding_profiles", PROFILES)]
    # Expand dependencies, not all modules: compact charter retains its fixed read set.
    while True:
        expanded = roles | {call["binds_to"] for call in all_bindings if call["contract"] in roles}
        if expanded == roles:
            break
        roles = expanded
    bindings = [call for call in all_bindings if call["contract"] in roles]
    code_roles = sorted(roles)
    bad_roles, errors = set(), {}
    for role, (code, error) in zip(code_roles, rpc.batch([("eth_getCode", [addresses[role], tag]) for role in code_roles])):
        if error or not isinstance(code, str) or not re.fullmatch(r"0x(?:[0-9a-fA-F]{2})+", code) or not any(x != "0" for x in code[2:]):
            bad_roles.add(role)
            errors["code_" + role] = "contract code unavailable at snapshot block"

    def reject_dependents():
        while True:
            rejected = bad_roles | {call["contract"] for call in bindings if call["binds_to"] in bad_roles}
            if rejected == bad_roles:
                return
            bad_roles.update(rejected)

    mapping, raw = [], {}

    def fetch(calls, arguments=None):
        callable_calls = [call for call in calls if call["contract"] not in bad_roles
                          and not (call["id"] == INCENTIVES_BALANCE and "incentivesVault" in bad_roles)]
        items = [{"id": call["id"], "contract": call["contract"], "address": addresses[call["contract"]],
                  "signature": call["signature"], "data": _calldata(call, arguments or config)} for call in callable_calls]
        mapping.extend(items)
        responses = rpc.batch([("eth_call", [{"to": item["address"], "data": item["data"]}, tag]) for item in items])
        for call, (result, error) in zip(callable_calls, responses):
            try:
                if error:
                    raise ValueError(error)
                raw[call["id"]] = _decode_result(result, call)
            except ValueError:
                errors[call["id"]] = "RPC field unavailable or invalid ABI result"

    reject_dependents()
    fetch(bindings)
    for call in bindings:
        if raw.get(call["id"]) != addresses[call["binds_to"]]:
            bad_roles.add(call["contract"])
            errors[call["id"]] = "contract binding unavailable or does not match fixed catalog"
    reject_dependents()
    owner_calls = [call for call in selected if "$charter_owner" in call["args"]]
    fetch([call for call in selected if call["id"] not in ASSET_DETAILS and call not in owner_calls])
    if owner_calls:
        if "charterNFT" not in bad_roles and raw.get("charter_owner", ZERO_ADDRESS) != ZERO_ADDRESS:
            fetch(owner_calls, dict(config, charter_owner=raw["charter_owner"]))
        else:
            for call in owner_calls:
                errors[call["id"]] = "valid charter owner required"
    asset_details = [call for call in selected if call["id"] in ASSET_DETAILS]
    if raw.get(ASSET_APPROVAL) is True and "expansionVault" not in bad_roles:
        fetch(asset_details)
    else:
        for call in asset_details:
            errors[call["id"]] = "reserve asset approval not confirmed at snapshot block"
    values = {}
    for call in selected:
        identifier = call["id"]
        if call["contract"] in bad_roles or (identifier == INCENTIVES_BALANCE and "incentivesVault" in bad_roles):
            errors[identifier] = "contract code or binding check failed"
        elif identifier in raw:
            values[identifier] = _normalized(raw[identifier], call)
    standard_calls = [call for call in selected
                      if any(field["unit"].startswith("STANDARD")
                             for field in call.get("components", [call]))]
    if standard_calls and ("token_decimals" not in values or raw.get("token_decimals") != 18):
        errors["token_decimals"] = "STANDARD decimals must be confirmed as 18"
        for call in standard_calls:
            values.pop(call["id"], None)
            errors[call["id"]] = "STANDARD decimals not confirmed as 18"
    derived = _derive(config, raw, values, errors, timestamp)
    if config["view"] == "charter" and config["detail"] == "summary":
        values = {identifier: value for identifier, value in values.items() if identifier in CHARTER_VALUES}
        if "charter_owner" in values and not CHARTER_RATE_CALLS.isdisjoint(errors) and "charter_gross_daily" not in derived:
            errors["charter_gross_daily"] = "Current-rate equivalent unavailable; rate or scale prerequisites failed"
        errors = {identifier: message for identifier, message in errors.items()
                  if identifier in CHARTER_VALUES or identifier == "charter_gross_daily"}
    final_number, final_hash, final_timestamp = _block(rpc.one("eth_getBlockByNumber", [tag, False]), now)
    if (final_number, final_hash, final_timestamp) != (number, block_hash, timestamp):
        raise SnapshotError("snapshot block changed during read")
    evidence = {"chain_id": CHAIN_ID, "block_number": number, "block_hash": block_hash, "block_timestamp": timestamp,
                "retrieved_at": datetime.fromtimestamp(now(), timezone.utc).isoformat().replace("+00:00", "Z"),
                "interface_source_ids": interface["source_ids"], "package_sha256": hashes,
                "rpc_url": _rpc_endpoint()["label"]}
    if config["detail"] == "activity":
        evidence["interface_source_ids"] = interface["source_ids"] + interface["activity"]["source_ids"]
        evidence["activity_publisher_evidence"] = interface["activity"]["publisher_evidence"]
    if config["detail"] == "full":
        evidence.update({"call_mapping": mapping, "rpc_exchanges": rpc.exchanges,
                         "publisher_bundle": interface["publisher_bundle"]})
    result = {"schema_version": 1, "status": "partial" if errors else "ok", "view": config["view"],
              "values": values, "derived": derived, "errors": errors, "evidence": evidence, "note": NOTE}
    if config["view"] == "charter":
        result["charter_id"] = config["charter_id"]
        if config["detail"] != "activity" and "charter_pending" not in values:
            result["message"] = "Charter pending unavailable; no accrued-balance valuation."
    if "reserve_asset" in config:
        result["reserve_asset"] = config["reserve_asset"]
    if config["view"] == "orderbook":
        page_value = values.pop("orderbook_page", None)
        page = {"start": str(config["start"]), "count": config["count"],
                "raw_ids": [str(value) for value in page_value["value"]] if page_value is not None else None,
                "type": "uint256[]", "identifier_semantics": "unestablished",
                "coverage": "single_bounded_page", "complete_orderbook": False}
        if "orderbook_page" in errors:
            page["error"] = errors["orderbook_page"]
        charters = []
        for index, charter_id in enumerate(config.get("charter_ids", [])):
            bid_id, fillable_id = "orderbook_bid_" + str(index), "orderbook_fillable_" + str(index)
            charters.append({"charter_id": str(charter_id),
                             "bids": values.pop(bid_id, None), "fillable": values.pop(fillable_id, None),
                             "errors": {getter: errors[key] for getter, key in (("bids", bid_id), ("fillable", fillable_id))
                                        if key in errors}})
        result["orderbook"] = {"page": page, "selected_charters": charters,
                               "selection_basis": "explicit_charter_ids_not_page_ids",
                               "bid_price_units": "raw_unestablished_denomination",
                               "fillable_basis": "pinned_block_getter_not_execution_guarantee"}
        if config["detail"] == "full":
            evidence["orderbook_publisher_evidence"] = interface["orderbook"]["publisher_evidence"]
    return result


def _cli_config(arguments):
    if len(arguments) > 9 or any(len(value) > 789 for value in arguments):
        raise InputError("CLI accepts at most 9 arguments of at most 789 characters")
    if not arguments or arguments[0] not in PROFILES:
        raise InputError("expected protocol, auctions, charter, treasury, or orderbook as the first argument")
    config = {"schema_version": 1, "view": arguments[0]}
    seen = set()
    index = 1
    while index < len(arguments):
        flag = arguments[index]
        if flag not in ("--id", "--detail", "--asset", "--start", "--count", "--charter-ids") or flag in seen:
            raise InputError("unknown or repeated CLI flag")
        seen.add(flag)
        if index + 1 == len(arguments):
            raise InputError("CLI flag requires a value")
        value = arguments[index + 1]
        if flag in ("--id", "--start", "--count"):
            if not re.fullmatch(r"[0-9]{1,78}", value):
                raise InputError(flag + " requires 1..78 ASCII decimal digits")
            config["charter_id" if flag == "--id" else flag[2:]] = int(value)
        elif flag == "--charter-ids":
            if not re.fullmatch(r"[0-9]{1,78}(?:,[0-9]{1,78}){0,9}", value):
                raise InputError("--charter-ids requires 1..10 comma-separated uint256 integers")
            config["charter_ids"] = [int(identifier) for identifier in value.split(",")]
        elif flag == "--asset":
            config["reserve_asset"] = value
        else:
            config["detail"] = value
        index += 2
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
        result = snapshot(config)
    except (InputError, PackageDataError, SnapshotError) as error:
        code, kind = (2, "invalid_input") if isinstance(error, InputError) else (4, "package_data_error") if isinstance(error, PackageDataError) else (5, "snapshot_error")
        failure = {"type": kind, "message": str(error)}
        if isinstance(error, SnapshotError) and error.diagnostics is not None:
            failure["diagnostics"] = error.diagnostics
        sys.stderr.write(json.dumps({"schema_version": 1, "error": failure, "note": NOTE}) + "\n")
        return code
    formatting = {"indent": 2} if config.get("detail", "summary") == "full" else {"separators": (",", ":")}
    sys.stdout.write(json.dumps(result, ensure_ascii=True, allow_nan=False, **formatting) + "\n")
    return 0


if __name__ == "__main__":
    sys.exit(main())
