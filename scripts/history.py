#!/usr/bin/env python3
"""Finite, read-only auction and buyback event accounting; standard library only.

Run with python3 -B -I. The reviewed sibling snapshot module supplies the
configurable RPC transport, strict JSON-RPC parser and descriptor-safe catalog readers.
No downloaded code, receipts, unpinned getters or saved results.
"""

import hashlib
import json
import os
from pathlib import Path
import re
import stat
import sys
import time
import types
from datetime import datetime, timezone
from fractions import Fraction


EVENTS_SHA256 = "d4aa58d40dbcc4fa87dfccf24b8255a6137c66f78a158b5902b0d89ad506ed47"
TREASURY_EVENTS_SHA256 = "edf5274602de69369b37d3e83634c2591d0b75c57a52c243c11737cd23f9f74b"
MAX_BLOCKS = 5_000_000
DEFAULT_LOOKBACK = 1_000_000
MAX_CHUNK_BLOCKS = 10_000
MAX_CHUNKS = 500
DEFAULT_MAX_CHUNKS = 100
MAX_REQUESTS = 4096
MAX_TOTAL_BYTES = 64 * 1024 * 1024
MAX_LOGS = 10_000
MAX_WINDOW_LOGS = 2000
MAX_HEADERS = 2048
MAX_ROUNDS = 1000
OVERALL_TIMEOUT = 180
MIN_REQUEST_INTERVAL = 0.5
MAX_SCRIPT_BYTES = 1024 * 1024
MAX_BLOCK_NUMBER = (1 << 64) - 1
UINT256_MAX = (1 << 256) - 1
ROLES = {"license": "licenseAuction", "charter": "charterAuction", "buybacks": "contractionVault", "pol-buybacks": "polBuyback"}
BUYBACK_KINDS = ("buybacks", "pol-buybacks")
_SNAPSHOT = None


class InputError(ValueError):
    """Invalid finite history selection."""


class HistoryError(ValueError):
    """An observation or budget cannot support the requested history."""


class ReorgError(HistoryError):
    """Previously checked observations cannot be combined safely."""


def _load_snapshot():
    """Load only the exact reviewed sibling file, without import-path search."""
    global _SNAPSHOT
    if _SNAPSHOT is not None:
        return _SNAPSHOT
    descriptors = []
    try:
        root = Path(__file__).resolve(strict=True).parent.parent
        parent = os.open(root, os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW)
        descriptors.append(parent)
        before = os.stat("scripts", dir_fd=parent, follow_symlinks=False)
        if not stat.S_ISDIR(before.st_mode):
            raise ValueError("unsafe scripts directory")
        directory = os.open("scripts", os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW, dir_fd=parent)
        descriptors.append(directory)
        opened = os.fstat(directory)
        if (before.st_dev, before.st_ino) != (opened.st_dev, opened.st_ino):
            raise ValueError("scripts directory changed")
        before = os.stat("snapshot.py", dir_fd=directory, follow_symlinks=False)
        if not stat.S_ISREG(before.st_mode) or not 0 < before.st_size <= MAX_SCRIPT_BYTES:
            raise ValueError("unsafe snapshot module")
        descriptor = os.open("snapshot.py", os.O_RDONLY | os.O_NOFOLLOW | os.O_NONBLOCK, dir_fd=directory)
        descriptors.append(descriptor)
        identity = lambda info: (info.st_dev, info.st_ino, info.st_size, info.st_mtime_ns, info.st_ctime_ns)
        opened = os.fstat(descriptor)
        if not stat.S_ISREG(opened.st_mode) or identity(before) != identity(opened):
            raise ValueError("snapshot module changed")
        chunks, size = [], 0
        while size <= MAX_SCRIPT_BYTES:
            chunk = os.read(descriptor, min(65536, MAX_SCRIPT_BYTES + 1 - size))
            if not chunk:
                break
            chunks.append(chunk)
            size += len(chunk)
        if size != opened.st_size or identity(opened) != identity(os.fstat(descriptor)):
            raise ValueError("snapshot module changed")
        module = types.ModuleType("_srstack_reviewed_snapshot")
        module.__file__ = str(root / "scripts" / "snapshot.py")
        exec(compile(b"".join(chunks), module.__file__, "exec"), module.__dict__)
        _SNAPSHOT = module
        return module
    except (OSError, ValueError, AttributeError, RuntimeError, SyntaxError, ImportError):
        raise HistoryError("fixed sibling snapshot module is missing, unsafe, or invalid") from None
    finally:
        for descriptor in reversed(descriptors):
            os.close(descriptor)


def _validate_input(config):
    required = {"schema_version", "kind"} if isinstance(config, dict) and config.get("kind") in BUYBACK_KINDS else {"schema_version", "auction"}
    optional = {"day", "anchor_block", "lookback_blocks", "from_block", "to_block", "chunk_blocks", "max_chunks", "detail"}
    if not isinstance(config, dict) or not required <= config.keys() or config.keys() - required - optional:
        raise InputError("unexpected or missing fields")
    kind = config.get("kind", config.get("auction"))
    if (type(config["schema_version"]) is not int or config["schema_version"] != 1
            or not isinstance(kind, str) or kind not in ROLES
            or ("auction" in config and kind in BUYBACK_KINDS)):
        raise InputError("expected schema_version 1 and license/charter auction or buybacks/pol-buybacks kind")
    if kind in BUYBACK_KINDS and "day" in config:
        raise InputError("day is only supported for license or charter auctions")
    value = dict(config)
    value.setdefault("detail", "summary")
    value.setdefault("chunk_blocks", MAX_CHUNK_BLOCKS)
    value.setdefault("max_chunks", DEFAULT_MAX_CHUNKS)
    if value["detail"] not in ("summary", "full"):
        raise InputError("detail must be summary or full")
    for name, maximum, minimum in (("day", UINT256_MAX, 0), ("anchor_block", MAX_BLOCK_NUMBER, 0),
                                   ("from_block", MAX_BLOCK_NUMBER, 0), ("to_block", MAX_BLOCK_NUMBER, 0),
                                   ("lookback_blocks", MAX_BLOCKS, 1), ("chunk_blocks", MAX_CHUNK_BLOCKS, 1),
                                   ("max_chunks", MAX_CHUNKS, 1)):
        if name in value and (type(value[name]) is not int or not minimum <= value[name] <= maximum):
            raise InputError(name + " is outside its integer bounds")
    explicit = "from_block" in value or "to_block" in value
    if explicit:
        if not {"from_block", "to_block"} <= value.keys() or {"anchor_block", "lookback_blocks"} & value.keys():
            raise InputError("use from_block and to_block together, without anchor_block or lookback_blocks")
        if not 1 <= value["to_block"] - value["from_block"] + 1 <= MAX_BLOCKS:
            raise InputError("explicit range must be ascending and at most 5000000 blocks")
    else:
        value.setdefault("lookback_blocks", DEFAULT_LOOKBACK)
    return value


def _load_catalog(s, kind):
    descriptors = []
    buybacks = kind in BUYBACK_KINDS
    filename = "treasury-events.json" if buybacks else "auction-events.json"
    try:
        interface, addresses, hashes = s._load_package()
        root = os.open(Path(__file__).resolve(strict=True).parent.parent, os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW)
        descriptors.append(root)
        assets = s._directory(root, "assets")
        descriptors.append(assets)
        directory = s._directory(assets, "interfaces")
        descriptors.append(directory)
        catalog, digest = s._read_file(directory, filename)
        s._keys(catalog, {"schema_version", "scope", "chain_id", "source_ids", "entity_catalog", "research_recipe", "contracts", "topic_convention", "events", "limits"})
        if (type(catalog["schema_version"]) is not int or catalog["schema_version"] != 1
                or type(catalog["chain_id"]) is not int or catalog["chain_id"] != s.CHAIN_ID
                or catalog["entity_catalog"] != "assets/entities/robinhood.json"
                or catalog["research_recipe"] != "references/auction-history.md"
                or catalog["source_ids"] != (["sr-extended-read-interface", "sr-pol-buyback-event-interface", "sr-v1-1-deployment-evidence"] if buybacks
                                              else ["sr-auction-event-interface", "sr-v1-1-read-interface", "sr-v1-1-deployment-evidence"])):
            raise ValueError("invalid event metadata")
        fingerprint = hashlib.sha256(json.dumps({k: catalog[k] for k in ("contracts", "events")}, sort_keys=True, separators=(",", ":")).encode()).hexdigest()
        if fingerprint != (TREASURY_EVENTS_SHA256 if buybacks else EVENTS_SHA256):
            raise ValueError("unreviewed event catalog")
        for role, contract in catalog["contracts"].items():
            if contract["entity_id"] != interface["contracts"][role] or contract["address"].lower() != addresses[role]:
                raise ValueError("event identity differs from fixed entity catalog")
        topics, names = set(), set()
        for event in catalog["events"]:
            abi = event["abi"]
            if (abi["type"] != "event" or abi["anonymous"] is not False or not s.WORD.fullmatch(event["topic0"])
                    or event["topic0"] in topics or any((role, abi["name"]) in names for role in event["contracts"])
                    or not event["contracts"] or any(role not in catalog["contracts"] for role in event["contracts"])
                    or event["signature"] != abi["name"] + "(" + ",".join(i["type"] for i in abi["inputs"]) + ")"
                    or sum(i["indexed"] is True for i in abi["inputs"]) > 3
                    or any(i["type"] not in ("uint256", "address") or type(i["indexed"]) is not bool for i in abi["inputs"])):
                raise ValueError("invalid reviewed event ABI")
            topics.add(event["topic0"])
            names.update((role, abi["name"]) for role in event["contracts"])
        hashes["assets/interfaces/" + filename] = digest
        return catalog, interface, addresses, hashes
    except (OSError, ValueError, TypeError, KeyError, RecursionError, RuntimeError):
        raise HistoryError("fixed event or entity catalog is missing, unsafe, or invalid") from None
    finally:
        for descriptor in reversed(descriptors):
            os.close(descriptor)


class _Budget:
    def __init__(self, s, transport, monotonic, pace=False):
        self.s, self.transport, self.monotonic = s, transport, monotonic
        self.deadline = monotonic() + OVERALL_TIMEOUT
        self.requests = self.http_requests = self.response_bytes = self.logs = 0
        self.interval = MIN_REQUEST_INTERVAL if pace else 0
        self.next_request_at = monotonic()

    def check(self):
        if self.monotonic() >= self.deadline:
            raise self.s.SnapshotError("history overall time budget exhausted")

    def __call__(self, payload, timeout, deadline, monotonic):
        self.check()
        count = len(json.loads(payload))
        if self.requests + count > MAX_REQUESTS:
            raise self.s.SnapshotError("history RPC request budget exhausted")
        # Reserve the maximum single response, including a bounded HTTP failure,
        # before sending. Never issue a request that could overrun the total cap.
        if self.response_bytes + self.s.MAX_RESPONSE_BYTES > MAX_TOTAL_BYTES:
            raise self.s.SnapshotError("history total response byte budget exhausted")
        delay = self.next_request_at - self.monotonic()
        if delay > 0:
            if self.monotonic() + delay >= min(deadline, self.deadline):
                raise self.s.SnapshotError("history time budget cannot accommodate request pacing")
            time.sleep(delay)
            self.check()
        self.next_request_at = self.monotonic() + self.interval
        self.requests += count
        self.http_requests += 1
        raw = self.transport(payload, timeout, min(deadline, self.deadline), monotonic)
        if not isinstance(raw, bytes):
            raise self.s.SnapshotError("RPC transport did not return bytes")
        self.response_bytes += len(raw)
        if len(raw) > self.s.MAX_RESPONSE_BYTES or self.response_bytes > MAX_TOTAL_BYTES:
            raise self.s.SnapshotError("history response byte budget exhausted")
        self.check()
        return raw


def _header(s, value, number, now):
    if (not isinstance(value, dict) or not isinstance(value.get("hash"), str)
            or not s.WORD.fullmatch(value["hash"]) or int(value["hash"], 16) == 0):
        raise HistoryError("invalid historical block header")
    actual, timestamp = s._quantity(value.get("number")), s._quantity(value.get("timestamp"))
    if actual > MAX_BLOCK_NUMBER or (number is not None and actual != number) or timestamp > now() + s.MAX_FUTURE_SECONDS:
        raise HistoryError("historical block number or timestamp mismatch")
    return {"number": actual, "hash": value["hash"].lower(), "timestamp": timestamp}


def _headers(s, rpc, numbers, now):
    result = {}
    ordered = sorted(numbers)
    for number, (value, error) in zip(ordered, rpc.batch([("eth_getBlockByNumber", [hex(n), False]) for n in ordered])):
        if error:
            raise HistoryError("historical block header unavailable")
        result[number] = _header(s, value, number, now)
    if len({header["hash"] for header in result.values()}) != len(result):
        raise ReorgError("one block hash names conflicting block numbers")
    if any(result[a]["timestamp"] > result[b]["timestamp"] for a, b in zip(ordered, ordered[1:])):
        raise HistoryError("historical block timestamps are not ordered")
    return result


def _decode_log(s, value, emitters, start, end):
    required = {"address", "blockNumber", "blockHash", "transactionHash", "transactionIndex", "logIndex", "topics", "data", "removed"}
    if not isinstance(value, dict) or not required <= value.keys():
        raise HistoryError("log fields are missing")
    if not isinstance(value["address"], str) or not s.ADDRESS.fullmatch(value["address"]):
        raise HistoryError("invalid log emitter")
    address = value["address"].lower()
    emitter = emitters.get(address)
    if emitter is None:
        raise HistoryError("log emitter differs from selected fixed contracts")
    number = s._quantity(value["blockNumber"])
    tx_index, index = s._quantity(value["transactionIndex"]), s._quantity(value["logIndex"])
    if not start <= number <= end or max(tx_index, index) > MAX_BLOCK_NUMBER or type(value["removed"]) is not bool:
        raise HistoryError("log range, position or removed flag is invalid")
    for key in ("blockHash", "transactionHash"):
        if not isinstance(value[key], str) or not s.WORD.fullmatch(value[key]) or int(value[key], 16) == 0:
            raise HistoryError("log hash is invalid")
    topics = value["topics"]
    if not isinstance(topics, list) or not 1 <= len(topics) <= 4 or any(not isinstance(t, str) or not s.WORD.fullmatch(t) for t in topics):
        raise HistoryError("invalid log topics")
    event = emitter["definitions"].get(topics[0].lower())
    if event is None:
        raise HistoryError("unexpected event topic for selected contract")
    inputs = event["abi"]["inputs"]
    indexed = sum(i["indexed"] for i in inputs)
    data = value["data"]
    if (len(topics) != indexed + 1 or not isinstance(data, str)
            or len(data) != 2 + 64 * (len(inputs) - indexed)
            or not re.fullmatch(r"0x[0-9a-fA-F]*", data)):
        raise HistoryError("log ABI topic or data size mismatch")
    topic_index, data_index, fields = 1, 2, {}
    for item in inputs:
        if item["indexed"]:
            word = topics[topic_index]
            topic_index += 1
        else:
            word = "0x" + data[data_index:data_index + 64]
            data_index += 64
        fields[item["name"]] = s._decode(word, item["type"])
    if event["abi"]["name"] == "LicensesPurchased" and fields["count"] == 0:
        raise HistoryError("purchase quantity is zero")
    return {"address": address, "contract_role": emitter["role"], "entity_id": emitter["entity_id"],
            "event": event["abi"]["name"], "fields": fields, "block_number": number,
            "block_hash": value["blockHash"].lower(), "transaction_hash": value["transactionHash"].lower(),
            "transaction_index": tx_index, "log_index": index, "removed": value["removed"]}


def _window(s, rpc, budget, emitters, start, end, anchor, now):
    addresses = list(emitters)
    topics = list(dict.fromkeys(topic for emitter in emitters.values() for topic in emitter["definitions"]))
    # A catalog-authenticated pre-deployment window still receives header and
    # anchor checks, but must never become an unfiltered all-contract log query.
    raw = rpc.one("eth_getLogs", [{"address": addresses[0] if len(addresses) == 1 else addresses,
                                  "fromBlock": hex(start), "toBlock": hex(end), "topics": [topics]}]) if addresses else []
    if not isinstance(raw, list):
        raise HistoryError("log result is not an array")
    budget.logs += len(raw)
    if len(raw) >= MAX_WINDOW_LOGS or budget.logs > MAX_LOGS:
        # The window cannot contribute totals, but validated removal evidence
        # still invalidates prior windows; resource exhaustion must not hide it.
        for value in raw:
            if isinstance(value, dict) and value.get("removed") is True:
                try:
                    _decode_log(s, value, emitters, start, end)
                except (ValueError, TypeError, KeyError):
                    continue
                raise ReorgError("removed log excluded; affected coverage is incomplete")
        raise HistoryError("log budget or conservative per-window saturation threshold reached")
    events, positions, transactions, by_hash = [], set(), {}, {}
    for value in raw:
        budget.check()
        event = _decode_log(s, value, emitters, start, end)
        if event["removed"]:
            raise ReorgError("removed log excluded; affected coverage is incomplete")
        position = event["block_number"], event["log_index"]
        if position in positions:
            raise HistoryError("duplicate or conflicting log position")
        positions.add(position)
        tx_position = event["block_number"], event["transaction_index"]
        tx_hash = event["transaction_hash"]
        if transactions.setdefault(tx_position, tx_hash) != tx_hash or by_hash.setdefault(tx_hash, tx_position) != tx_position:
            raise HistoryError("conflicting transaction hash or position")
        events.append(event)
    events.sort(key=lambda event: (event["block_number"], event["log_index"]))
    previous = None
    for event in events:
        if previous is not None and previous["block_number"] == event["block_number"] and previous["transaction_index"] > event["transaction_index"]:
            raise HistoryError("log and transaction positions disagree")
        previous = event
    numbers = {start, end} | {event["block_number"] for event in events}
    if len(numbers) > MAX_HEADERS:
        raise HistoryError("window block-header budget exhausted")
    headers = _headers(s, rpc, numbers, now)
    for event in events:
        header = headers[event["block_number"]]
        if header["hash"] != event["block_hash"]:
            raise ReorgError("log block hash differs from canonical block header")
        if header["timestamp"] > anchor["timestamp"]:
            raise HistoryError("log timestamp is later than the anchor")
        event["timestamp"] = header["timestamp"]
    checked = _headers(s, rpc, numbers | {anchor["number"]}, now)
    if checked[anchor["number"]] != anchor or any(checked[n] != header for n, header in headers.items()):
        raise ReorgError("anchor or used block changed during history scan")
    return events, headers


def _observation(event):
    return {"block_number": event["block_number"], "timestamp": event["timestamp"], "transaction_hash": event["transaction_hash"]}


def _rounds(s, events, auction, day, gaps):
    groups = {}
    for event in events:
        fields = event["fields"]
        if "day" not in fields or (day is not None and fields["day"] != day):
            continue
        groups.setdefault((event["address"], fields["day"]), []).append(event)
    result = []
    for (address, identifier), observed in sorted(groups.items()):
        purchases = [e for e in observed if e["event"] in ("LicensesPurchased", "CharterPurchased")]
        rolls = [e for e in observed if e["event"] == "DayRolled"]
        starts = [e for e in observed if e["event"] == "AuctionStarted"]
        quantity = sum(e["fields"]["count"] if auction == "license" else 1 for e in purchases)
        total = sum(e["fields"]["count"] * e["fields"]["unitPrice"] if auction == "license" else e["fields"]["price"] for e in purchases)
        average = Fraction(total, quantity) if quantity else None
        caps = {e["fields"]["cap"] for e in rolls}
        missing = ["scheduled_opening_unavailable", "effective_historical_configuration_unavailable", "round_extent_not_established"]
        if not caps:
            missing.append("round_cap_unavailable")
        elif len(caps) > 1:
            missing.append("conflicting_observed_round_caps")
        if gaps:
            missing.append("requested_window_has_coverage_gaps")
        result.append({"address": address, "contract_role": observed[0]["contract_role"], "entity_id": observed[0]["entity_id"],
                       "day": str(identifier), "purchase_event_count": len(purchases), "purchase_quantity": str(quantity),
                       "quantity_unit": "licenses" if auction == "license" else "charters",
                       "consideration": {"basis": "purchase_event_accounting", "asset": "STANDARD" if auction == "license" else "ETH", "decimals": 18,
                                         "total_raw": str(total), "total": s._scaled(total, 18),
                                         "quantity_weighted_average_raw": None if average is None else {"numerator": str(average.numerator), "denominator": str(average.denominator)}},
                       "observed_rolls": [{**_observation(e), "reported_cap": str(e["fields"]["cap"])} for e in rolls],
                       "observed_activations": [_observation(e) for e in starts],
                       "reported_round_cap": str(next(iter(caps))) if len(caps) == 1 else None,
                       "first_observed_purchase": _observation(purchases[0]) if purchases else None,
                       "last_observed_purchase": _observation(purchases[-1]) if purchases else None,
                       "scheduled_opening": None, "complete_round": False, "sellout": "not_established", "time_to_sellout": None,
                       "gaps": missing})
    return result


def _buyback_binding(s, rpc, interface, addresses, block):
    calls = {(call["contract"], call["signature"]): call for call in interface["calls"]
             if (call["contract"], call["signature"]) in (("contractionVault", "standard()"), ("standard", "decimals()"))}
    binding = calls[("contractionVault", "standard()")]
    decimals = calls[("standard", "decimals()")]
    if (binding["input_types"] or decimals["input_types"] or binding["output_type"] != "address"
            or decimals["output_type"] != "uint8"):
        raise HistoryError("invalid fixed buyback denomination interface")
    tag = hex(block)
    token = s._decode(rpc.one("eth_call", [{"to": addresses["contractionVault"], "data": binding["selector"]}, tag]), "address")
    if token != addresses["standard"]:
        raise HistoryError("Contraction Vault STANDARD binding differs from fixed token")
    code = rpc.one("eth_getCode", [addresses["standard"], tag])
    if not isinstance(code, str) or not re.fullmatch(r"0x(?:[0-9a-fA-F]{2})+", code) or not any(c != "0" for c in code[2:]):
        raise HistoryError("fixed STANDARD code unavailable at anchor")
    scale = s._decode(rpc.one("eth_call", [{"to": addresses["standard"], "data": decimals["selector"]}, tag]), "uint8")
    if scale != 18:
        raise HistoryError("fixed STANDARD decimals differ from reviewed denomination")
    return {"block_number": block, "standard_address": token, "standard_decimals": scale,
            "standard_code_sha256": hashlib.sha256(bytes.fromhex(code[2:])).hexdigest(),
            "scope": "anchor binding and denomination only; historical implementation continuity and asset movement not established"}


def _buybacks(s, events, completed, gaps):
    observed = [event for event in events if event["event"] == "BuybackExecuted"]
    available = bool(completed)
    def amount(field, asset):
        total = sum(event["fields"][field] for event in observed) if available else None
        return {"asset": asset, "decimals": 18, "total_raw": None if total is None else str(total),
                "total": None if total is None else s._scaled(total, 18)}
    return {"basis": "buyback_event_accounting",
            "scope": "only BuybackExecuted events in checked completed windows; not protocol-wide burns or independently reconciled asset movement",
            "observation_status": "unavailable" if not available else "observed_events" if observed else "no_matches_in_scanned_windows",
            "event_count": len(observed) if available else None,
            "eth_spent": amount("ethSpent", "ETH"), "standard_burned": amount("tokensBurned", "STANDARD"),
            "first_observed_buyback": _observation(observed[0]) if observed else None,
            "last_observed_buyback": _observation(observed[-1]) if observed else None,
            "requested_range_complete": available and not gaps}


def _pol_buybacks(s, events, completed, gaps):
    available = bool(completed)
    eth_in = sum(event["fields"]["ethIn"] for event in events) if available else None
    tokens_out = sum(event["fields"]["tokensOut"] for event in events) if available else None
    destinations = {}
    for event in events:
        row = destinations.setdefault(event["fields"]["destination"], {"event_count": 0, "tokens_out": 0})
        row["event_count"] += 1
        row["tokens_out"] += event["fields"]["tokensOut"]
    return {"basis": "pol_buyback_event_accounting",
            "scope": "event-reported ETH input, raw token output and destination only; not burns, authenticated token denomination or independently reconciled wallet flows",
            "observation_status": ("unavailable" if not available else "observed_events" if events else
                                   "no_matches_in_scanned_windows" if any(window["emitter_addresses"] for window in completed) else "no_deployed_emitters"),
            "event_count": len(events) if available else None,
            "eth_in": {"asset": "ETH", "decimals": 18, "total_raw": None if eth_in is None else str(eth_in),
                       "total": None if eth_in is None else s._scaled(eth_in, 18)},
            "tokens_out": {"asset": None, "decimals": None, "total_raw": None if tokens_out is None else str(tokens_out),
                           "total": None, "denomination_status": "unestablished; raw event field only"},
            "reported_destinations": [{"destination": destination, "event_count": row["event_count"],
                                       "tokens_out_raw": str(row["tokens_out"])} for destination, row in sorted(destinations.items())] if available else None,
            "first_observed_buyback": _observation(events[0]) if events else None,
            "last_observed_buyback": _observation(events[-1]) if events else None,
            "requested_range_complete": available and not gaps}


def _error(error):
    result = {"message": "".join(c for c in str(error)[:240] if c.isprintable())}
    diagnostics = getattr(error, "diagnostics", None)
    if isinstance(diagnostics, dict):
        result["diagnostics"] = diagnostics
    return result


def history(config, transport=None, now=None, monotonic=None):
    """Return observed event accounting and finite coverage, never persist."""
    config = _validate_input(config)
    kind = config.get("kind", config.get("auction"))
    now, monotonic = now or time.time, monotonic or time.monotonic
    completed, errors, events = [], {}, []
    start, end = config.get("from_block"), config.get("to_block", config.get("anchor_block"))
    if start is None and end is not None:
        start = max(0, end - config["lookback_blocks"] + 1)
    cursor, anchor, budget, s = start, None, None, None
    evidence = {"chain_id": 4663, "accounting": ("BuybackExecuted ethSpent and tokensBurned; event accounting, not proof of actual ERC20 movement or protocol-wide burns"
                                               if kind == "buybacks" else "BuybackExecuted ethIn, raw tokensOut and reported destination; no established token denomination, burns or wallet flows"
                                               if kind == "pol-buybacks" else "purchase events; receipts and payment flows not independently reconciled"),
                "reorg_policy": "canonical-number headers and fixed anchor rechecked before each committed window; observed reorg invalidates all windows; no finality claim"}
    stage = "setup"
    invalidated = False
    try:
        s = _load_snapshot()
        catalog, interface, addresses, hashes = _load_catalog(s, kind)
        roles = ("licenseAuctionLegacy", "licenseAuction") if kind == "license" else (ROLES[kind],)
        emitters = {addresses[role]: {"role": role, "entity_id": catalog["contracts"][role]["entity_id"],
                                     "deployment_block": catalog["contracts"][role].get("deployment_block", 0),
                                     "definitions": {e["topic0"]: e for e in catalog["events"] if role in e["contracts"]}}
                    for role in roles}
        evidence.update({"rpc_url": s._rpc_endpoint()["label"], "source_ids": catalog["source_ids"], "package_sha256": hashes})
        evidence["deployment_boundaries"] = {address: emitter["deployment_block"] for address, emitter in emitters.items()
                                             if emitter["deployment_block"]}
        if kind == "license":
            evidence["license_generations"] = {role: catalog["contracts"][role] for role in roles}
        else:
            evidence[{"charter": "auction_address", "buybacks": "contraction_vault_address", "pol-buybacks": "pol_buyback_address"}[kind]] = addresses[ROLES[kind]]
        budget = _Budget(s, transport or s._https, monotonic, pace=transport is None)
        rpc = s._RPC(budget, monotonic, False)
        rpc.deadline = budget.deadline
        if s._quantity(rpc.one("eth_chainId", [])) != s.CHAIN_ID:
            raise HistoryError("RPC chain mismatch")
        fresh = end is None
        anchor = _header(s, rpc.one("eth_getBlockByNumber", ["latest" if fresh else hex(end), False]), end, now)
        if fresh and now() - anchor["timestamp"] > s.MAX_BLOCK_AGE:
            raise HistoryError("latest anchor is stale")
        if end is None:
            end = anchor["number"]
            start = max(0, end - config["lookback_blocks"] + 1)
        cursor = start
        evidence["anchor"] = anchor
        evidence["scan_emitters"] = [{"address": address, "contract_role": emitter["role"], "entity_id": emitter["entity_id"],
                                      "from_block": max(start, emitter["deployment_block"]), "to_block": end}
                                     for address, emitter in emitters.items() if emitter["deployment_block"] <= end]
        evidence["anchor_contracts"] = []
        for target in evidence["scan_emitters"]:
            code = rpc.one("eth_getCode", [target["address"], hex(end)])
            if not isinstance(code, str) or not re.fullmatch(r"0x(?:[0-9a-fA-F]{2})+", code) or not any(c != "0" for c in code[2:]):
                raise HistoryError("selected contract code unavailable at anchor")
            evidence["anchor_contracts"].append({"address": target["address"], "code_sha256": hashlib.sha256(bytes.fromhex(code[2:])).hexdigest()})
        if kind == "buybacks":
            evidence["anchor_standard_binding"] = _buyback_binding(s, rpc, interface, addresses, end)
        seen_days = set()
        seen_transactions, seen_block_hashes = {}, {anchor["hash"]: anchor["number"]}
        previous_timestamp = None
        while cursor <= end:
            stage = "window_" + str(cursor)
            budget.check()
            if len(completed) >= config["max_chunks"]:
                raise HistoryError("history chunk budget exhausted")
            stop = min(end, cursor + config["chunk_blocks"] - 1)
            # Split at deployment, not cutover: include initialization and never
            # infer that the legacy address stopped emitting at registry change.
            for emitter in emitters.values():
                if cursor < emitter["deployment_block"] <= stop:
                    stop = emitter["deployment_block"] - 1
            selected = {address: emitter for address, emitter in emitters.items() if emitter["deployment_block"] <= cursor}
            observed, headers = _window(s, rpc, budget, selected, cursor, stop, anchor, now)
            for event in observed:
                position = event["block_number"], event["transaction_index"]
                if seen_transactions.setdefault(event["transaction_hash"], position) != position:
                    raise ReorgError("transaction hash occurs at conflicting positions across windows")
            for number, header in headers.items():
                if seen_block_hashes.setdefault(header["hash"], number) != number:
                    raise ReorgError("block hash occurs at conflicting numbers across windows")
            if previous_timestamp is not None and previous_timestamp > headers[cursor]["timestamp"]:
                raise ReorgError("block timestamps conflict across windows")
            previous_timestamp = headers[stop]["timestamp"]
            days = {(e["address"], e["fields"]["day"]) for e in observed if "day" in e["fields"] and ("day" not in config or e["fields"]["day"] == config["day"])}
            if len(seen_days | days) > MAX_ROUNDS:
                raise HistoryError("history observed-round budget exhausted")
            seen_days.update(days)
            events.extend(observed)
            digest = hashlib.sha256(json.dumps(list(headers.values()), sort_keys=True, separators=(",", ":")).encode()).hexdigest()
            completed.append({"from_block": cursor, "to_block": stop, "emitter_addresses": list(selected),
                              "scan_status": "logs_checked" if selected else "no_deployed_emitters",
                              "matched_events": len(observed), "checked_headers_sha256": digest})
            cursor = stop + 1
        stage = "final_anchor"
        final = _header(s, rpc.one("eth_getBlockByNumber", [hex(end), False]), end, now)
        if final != anchor:
            raise ReorgError("anchor changed after completed windows")
        evidence["final_anchor_check"] = "matched"
    except (OSError, ValueError, TypeError, KeyError, RecursionError, RuntimeError) as error:
        errors[stage] = _error(error)
        if isinstance(error, ReorgError):
            evidence["invalidated_windows"] = completed[:]
            completed.clear()
            events.clear()
            cursor = start
            invalidated = True
        evidence["final_anchor_check"] = "changed" if invalidated else "unavailable; committed windows retain their own anchor checks"
    missing = []
    if start is None or end is None:
        missing.append({"from_block": start, "to_block": end, "reason": "anchor or requested range unavailable"})
    elif cursor is None or cursor <= end:
        missing.append({"from_block": start if cursor is None else cursor, "to_block": end, "reason": next(reversed(errors.values()))["message"] if errors else "not scanned"})
    evidence["retrieved_at"] = datetime.fromtimestamp(now(), timezone.utc).isoformat().replace("+00:00", "Z")
    evidence["budgets"] = {"max_blocks": MAX_BLOCKS, "chunk_blocks": config["chunk_blocks"], "max_chunks": config["max_chunks"],
                           "max_rpc_requests": MAX_REQUESTS, "max_total_response_bytes": MAX_TOTAL_BYTES,
                           "max_response_bytes": 1048576, "max_logs": MAX_LOGS, "window_log_saturation": MAX_WINDOW_LOGS,
                           "max_headers_per_window": MAX_HEADERS, "max_rounds": MAX_ROUNDS, "overall_seconds": OVERALL_TIMEOUT,
                           "minimum_live_http_interval_seconds": MIN_REQUEST_INTERVAL}
    if budget is not None:
        evidence["usage"] = {"rpc_requests": budget.requests, "http_requests": budget.http_requests, "response_bytes": budget.response_bytes, "returned_logs": budget.logs}
    if config["detail"] == "full":
        evidence["decoded_events"] = events
    result = {"schema_version": 1, "status": "partial" if errors or missing else "ok",
              "coverage": {"selection": config, "requested": {"from_block": start, "to_block": end}, "completed": completed, "missing": missing,
                           "scope": ("selected ContractionVault BuybackExecuted events over checked scanned windows, not all-history absence or protocol-wide burns; silent provider omissions cannot be independently excluded"
                                     if kind == "buybacks" else "selected POL Buyback raw event accounting, not burned-token accounting or proven wallet flows; silent provider omissions cannot be independently excluded"
                                     if kind == "pol-buybacks" else "catalog emitters over checked windows: legacy license throughout the requested interval and v1.1 from deployment, with no emission cutoff at registry cutover; not complete rounds or independently proven provider completeness"
                                     if kind == "license" else "selected-address catalog topics over scanned windows, not complete rounds; silent provider omissions cannot be independently excluded")},
              "errors": errors, "evidence": evidence}
    if kind == "buybacks":
        result.update({"kind": kind, "buybacks": _buybacks(s, events, completed, bool(errors or missing))})
    elif kind == "pol-buybacks":
        result.update({"kind": kind, "pol_buybacks": _pol_buybacks(s, events, completed, bool(errors or missing))})
    else:
        result.update({"auction": kind, "rounds": _rounds(s, events, kind, config.get("day"), bool(errors or missing)) if s is not None else []})
        result["coverage"]["day_filter"] = str(config["day"]) if "day" in config else None
    return result


def _cli_config(arguments):
    if not arguments or len(arguments) > 17 or any(len(a) > 80 for a in arguments) or arguments[0] not in ROLES:
        raise InputError("expected license, charter, buybacks or pol-buybacks and at most eight bounded flag/value pairs")
    config = {"schema_version": 1, "kind" if arguments[0] in BUYBACK_KINDS else "auction": arguments[0]}
    flags = {"--day", "--anchor-block", "--lookback-blocks", "--from-block", "--to-block", "--chunk-blocks", "--max-chunks", "--detail"}
    for index in range(1, len(arguments), 2):
        flag = arguments[index]
        name = flag[2:].replace("-", "_")
        if flag not in flags or name in config or index + 1 == len(arguments):
            raise InputError("unknown, repeated or valueless history flag")
        value = arguments[index + 1]
        if flag != "--detail":
            if not re.fullmatch(r"[0-9]{1,78}", value):
                raise InputError(flag + " requires ASCII decimal digits")
            value = int(value)
        config[name] = value
    return _validate_input(config)


def main():
    if sys.argv[1:] == ["--help"]:
        print("usage: history.py license|charter [--day N] [--anchor-block B] [--lookback-blocks N]\n"
              "       history.py license|charter [--day N] --from-block A --to-block B\n"
              "       history.py buybacks|pol-buybacks [--anchor-block B] [--lookback-blocks N]\n"
              "       history.py buybacks|pol-buybacks --from-block A --to-block B\n"
              "       any form: [--chunk-blocks N] [--max-chunks N] [--detail summary|full]\n"
              "Defaults: fresh head, 1000000-block lookback, 10000-block chunks, 100 chunks.\n"
              "Day is auction-only: an emitted round ID, not UTC or 24 hours. JSON stdout only; no saved results.")
        return 0
    try:
        result = history(_cli_config(sys.argv[1:]))
    except InputError as error:
        print(json.dumps({"schema_version": 1, "status": "error", "error": {"kind": "input", **_error(error)}}, separators=(",", ":")))
        return 2
    print(json.dumps(result, separators=(",", ":")))
    return 0 if result["status"] == "ok" else 4


if __name__ == "__main__":
    sys.exit(main())
