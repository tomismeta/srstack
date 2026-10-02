"""Validate reviewed ABI evidence as data; no network, routing, or execution client."""
import hashlib
import json
import re
from collections import Counter
from datetime import date
from functools import lru_cache

KINDS = {"function", "event", "error", "constructor", "receive", "fallback"}
MASK = (1 << 64) - 1
ROTATIONS = (0, 1, 62, 28, 27, 36, 44, 6, 55, 20, 3, 10, 43, 25, 39, 41, 45, 15, 21, 8, 18, 2, 61, 56, 14)
ROUND_CONSTANTS = (0x1, 0x8082, 0x800000000000808A, 0x8000000080008000,
                   0x808B, 0x80000001, 0x8000000080008081, 0x8000000000008009,
                   0x8A, 0x88, 0x80008009, 0x8000000A, 0x8000808B,
                   0x800000000000008B, 0x8000000000008089, 0x8000000000008003,
                   0x8000000000008002, 0x8000000000000080, 0x800A,
                   0x800000008000000A, 0x8000000080008081, 0x8000000000008080,
                   0x80000001, 0x8000000080008008)


@lru_cache(maxsize=4096)
def keccak256(data):
    """Ethereum Keccak-256, deliberately not hashlib.sha3_256."""
    def rotate(value, count):
        return ((value << count) | (value >> ((64 - count) % 64))) & MASK

    padded = bytearray(data)
    padded.append(1)
    padded.extend(bytes((-len(padded)) % 136))
    padded[-1] |= 0x80
    state = [0] * 25
    for offset in range(0, len(padded), 136):
        for lane in range(17):
            start = offset + lane * 8
            state[lane] ^= int.from_bytes(padded[start:start + 8], "little")
        for constant in ROUND_CONSTANTS:
            columns = [state[x] ^ state[x + 5] ^ state[x + 10] ^ state[x + 15] ^ state[x + 20] for x in range(5)]
            delta = [columns[(x - 1) % 5] ^ rotate(columns[(x + 1) % 5], 1) for x in range(5)]
            lanes = [0] * 25
            for x in range(5):
                for y in range(5):
                    index = x + 5 * y
                    lanes[y + 5 * ((2 * x + 3 * y) % 5)] = rotate(state[index] ^ delta[x], ROTATIONS[index])
            for x in range(5):
                for y in range(5):
                    state[x + 5 * y] = lanes[x + 5 * y] ^ ((~lanes[(x + 1) % 5 + 5 * y]) & lanes[(x + 2) % 5 + 5 * y])
            state[0] ^= constant
    return b"".join(lane.to_bytes(8, "little") for lane in state)[:32]


def canonical_type(parameter):
    value = parameter["type"]
    match = re.fullmatch(r"([^\[]+)((?:\[(?:[1-9][0-9]*)?\])*)", value)
    if not match:
        raise ValueError(f"Invalid ABI type: {value}")
    base, suffix = match.groups()
    if base == "tuple":
        components = parameter.get("components")
        if not isinstance(components, list):
            raise ValueError("Tuple requires ordered components")
        base = "(" + ",".join(canonical_type(item) for item in components) + ")"
    else:
        if "components" in parameter:
            raise ValueError("Non-tuple has components")
        base = {"uint": "uint256", "int": "int256", "fixed": "fixed128x18", "ufixed": "ufixed128x18"}.get(base, base)
        integer = re.fullmatch(r"u?int([0-9]+)", base)
        fixed_bytes = re.fullmatch(r"bytes([0-9]+)", base)
        fixed = re.fullmatch(r"u?fixed([0-9]+)x([0-9]+)", base)
        valid = base in {"address", "bool", "bytes", "string", "function"}
        valid |= bool(integer and 8 <= int(integer[1]) <= 256 and int(integer[1]) % 8 == 0)
        valid |= bool(fixed_bytes and 1 <= int(fixed_bytes[1]) <= 32)
        valid |= bool(fixed and 8 <= int(fixed[1]) <= 256 and int(fixed[1]) % 8 == 0 and 1 <= int(fixed[2]) <= 80)
        if not valid:
            raise ValueError(f"Invalid ABI base type: {base}")
    return base + suffix


def signature(abi):
    kind = abi["type"]
    if kind not in KINDS:
        raise ValueError(f"Invalid ABI entry kind: {kind}")
    name = abi.get("name") if kind in {"function", "event", "error"} else kind
    if not isinstance(name, str) or not re.fullmatch(r"[A-Za-z_$][A-Za-z0-9_$]*", name):
        raise ValueError("Invalid or missing ABI name")
    return name + "(" + ",".join(canonical_type(item) for item in abi.get("inputs", [])) + ")"


def declaration(abi):
    def parameter(item):
        value = canonical_type(item)
        if abi["type"] == "event" and item["indexed"]:
            value += " indexed"
        return value + (" " + item["name"] if item.get("name") else "")

    kind = abi["type"]
    prefix = kind + " " + abi["name"] if kind in {"function", "event", "error"} else kind
    result = prefix + "(" + ", ".join(parameter(item) for item in abi.get("inputs", [])) + ")"
    if kind == "event":
        return result + (" anonymous" if abi["anonymous"] else "")
    if kind in {"function", "constructor", "receive", "fallback"}:
        result += " " + abi["stateMutability"]
    if kind == "function":
        result += " returns (" + ", ".join(parameter(item) for item in abi["outputs"]) + ")"
    return result


def event_layout(abi):
    """Positions are parameters, not guessed words: tuple/dynamic data needs ABI decoding."""
    topic = 0 if abi["anonymous"] else 1
    data_index = 0
    fields = []
    for index, parameter in enumerate(abi["inputs"]):
        field = {"abi_index": index, "name": parameter.get("name", ""), "canonical_type": canonical_type(parameter), "indexed": parameter["indexed"]}
        if parameter["indexed"]:
            hashed = parameter["type"].startswith("tuple") or "[" in parameter["type"] or parameter["type"] in {"string", "bytes"}
            field.update({"location": "topic", "topic_index": topic, "encoding": "keccak256_indexed_value" if hashed else "abi_word"})
            topic += 1
        else:
            field.update({"location": "data", "data_parameter_index": data_index, "encoding": "abi_parameter"})
            data_index += 1
        fields.append(field)
    return {"anonymous": abi["anonymous"], "topic_count": topic, "data_parameter_count": data_index, "fields": fields}


def abi_digest(entries):
    """Canonical JSON preserves every ABI name, type, tuple component, and indexed bit."""
    return hashlib.sha256(json.dumps(entries, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode()).hexdigest()


def entry_counts(entries):
    counts = Counter(item["type"] for item in entries)
    return {kind: counts[kind] for kind in sorted(KINDS)}


def _validate_inventory(files):
    """Implementation; public wrapper normalizes malformed data to ValueError."""
    def require(condition, message):
        if not condition:
            raise ValueError(message)

    def load(path):
        require(path in files, f"Missing inventory file: {path}")
        try:
            return json.loads(files[path])
        except (ValueError, TypeError) as error:
            raise ValueError(f"Invalid inventory JSON: {path}") from error

    reviews_doc = load("assets/interfaces/reviews.json")
    contracts_doc = load("assets/entities/contracts.json")
    require(reviews_doc.get("schema_version") == 1 and contracts_doc.get("schema_version") == 1, "Unsupported inventory schema")
    reviews = {item["id"]: item for item in reviews_doc["reviews"]}
    require(len(reviews) == len(reviews_doc["reviews"]), "Duplicate review ID")
    source_records = {record["id"]: record for path in files if path.startswith("assets/sources/") and path.endswith(".json") for record in load(path)["records"]}
    interfaces = {}
    for path in files:
        if not path.startswith("assets/interfaces/") or path in {"assets/interfaces/reviews.json", "assets/interfaces/capabilities.json"}:
            continue
        item = load(path)
        identity = item["id"]
        require(item.get("schema_version") == 1, f"Unsupported interface schema: {identity}")
        require(path == f"assets/interfaces/{identity}.json" and identity not in interfaces, "Interface path/identity mismatch")
        require(item["review_id"] in reviews, f"Unknown interface review: {identity}")
        require(item.get("role") and item.get("generation"), f"Missing role/generation: {identity}")
        review = reviews[item["review_id"]]
        require(identity in review["interfaces"], f"Interface not covered by review: {identity}")
        coverage = item["coverage"]
        require(type(coverage["source_definition_complete"]) is bool, f"Missing completeness flag: {identity}")
        require(coverage["kind"] in {"complete_literal", "complete_adaptation", "selective_fragment"}, f"Unknown coverage kind: {identity}")
        require(coverage["source_definition_complete"] == (coverage["kind"] != "selective_fragment"), f"Inconsistent completeness: {identity}")
        require(type(coverage.get("deployed_implementation_complete")) is bool, f"Missing deployed completeness flag: {identity}")
        require(coverage["source_definition_complete"] or not coverage["deployed_implementation_complete"], f"Partial interface claims deployed completeness: {identity}")
        fragment = coverage["source_fragment"]
        require(coverage.get("source_locator") and re.fullmatch(r"[0-9a-f]{64}", fragment.get("sha256", "")), f"Missing source fragment provenance: {identity}")
        require(type(fragment.get("bytes")) is int and fragment["bytes"] > 0 and type(fragment.get("start_utf8_byte")) is int and type(fragment.get("end_utf8_byte")) is int and fragment["start_utf8_byte"] >= 0 and fragment["end_utf8_byte"] - fragment["start_utf8_byte"] == fragment["bytes"], f"Invalid source fragment byte range: {identity}")
        if "artifact_url" in fragment or "artifact_sha256" in fragment:
            parents = [artifact for artifact in review.get("source_chain", [])
                       if artifact.get("url") == fragment.get("artifact_url")
                       and artifact.get("sha256") == fragment.get("artifact_sha256")]
            require(len(parents) == 1, f"Unknown or ambiguous fragment parent: {identity}")
            require(fragment["end_utf8_byte"] <= parents[0]["bytes"], f"Source fragment exceeds parent artifact: {identity}")
        abis = [entry["abi"] for entry in item["entries"]]
        require(bool(abis), f"Empty reviewed interface: {identity}")
        digest, counts = abi_digest(abis), entry_counts(abis)
        require(coverage["abi_sha256"] == digest and coverage["entry_counts"] == counts, f"Incomplete/stale interface digest/counts: {identity}")
        require(review["interfaces"][identity] == coverage, f"Review coverage mismatch: {identity}")
        seen = set()
        for entry in item["entries"]:
            abi = entry["abi"]
            kind = abi["type"]
            canonical = signature(abi)
            key = (kind, canonical)
            require(key not in seen, f"Duplicate signature: {identity}: {key}")
            seen.add(key)
            require(entry["signature"] == canonical and entry["declaration"] == declaration(abi), f"Stale signature/declaration: {identity}: {canonical}")
            require(entry["review_id"] == item["review_id"], f"Wrong entry review: {identity}: {canonical}")
            require(entry["generation"] == item["generation"], f"Wrong entry generation: {identity}: {canonical}")
            require(isinstance(entry.get("explanation"), str) and bool(entry["explanation"].strip()), f"Missing explanation: {identity}: {canonical}")
            require(isinstance(entry.get("units"), str) and bool(entry["units"].strip()), f"Missing unit qualification: {identity}: {canonical}")
            require(isinstance(entry.get("limitations"), list) and entry["limitations"], f"Missing semantic limits: {identity}: {canonical}")
            for parameter in abi.get("inputs", []) + abi.get("outputs", []):
                canonical_type(parameter)
                require(isinstance(parameter.get("name"), str), f"Missing parameter name: {canonical}")
            if kind in {"function", "constructor", "receive", "fallback"}:
                require(abi.get("stateMutability") in {"view", "pure", "nonpayable", "payable"}, f"Invalid mutability: {canonical}")
            if kind == "function":
                require(isinstance(abi.get("outputs"), list), f"Missing return layout: {canonical}")
            if kind in {"function", "error"}:
                require(entry.get("selector") == "0x" + keccak256(canonical.encode())[:4].hex(), f"Wrong selector: {canonical}")
            else:
                require("selector" not in entry, f"Selector on noncallable entry: {canonical}")
            if kind == "event":
                require(type(abi.get("anonymous")) is bool and all(type(p.get("indexed")) is bool for p in abi["inputs"]), f"Missing explicit indexed/anonymous bits: {canonical}")
                require(sum(p["indexed"] for p in abi["inputs"]) <= (4 if abi["anonymous"] else 3), f"Too many indexed event fields: {canonical}")
                require(entry.get("topic0") == (None if abi["anonymous"] else "0x" + keccak256(canonical.encode()).hex()), f"Wrong event topic: {canonical}")
                require(entry.get("event_layout") == event_layout(abi), f"Wrong indexed event layout: {identity}: {canonical}")
            else:
                require("topic0" not in entry and "event_layout" not in entry, f"Event layout on non-event: {canonical}")
        interfaces[identity] = item
    for identity, item in interfaces.items():
        if item["coverage"]["kind"] != "complete_adaptation":
            continue
        adaptation = item["coverage"]["adaptation"]
        require(adaptation["base_interface_id"] in interfaces, f"Missing adaptation base: {identity}")
        base = interfaces[adaptation["base_interface_id"]]
        require(base["coverage"]["source_definition_complete"], f"Incomplete adaptation base: {identity}")
        retained = [entry["abi"] for entry in base["entries"] if not (adaptation["constructor_removed"] and entry["abi"]["type"] == "constructor") and entry["abi"].get("name") not in adaptation["removed_names"]]
        actual = [entry["abi"] for entry in item["entries"]]
        require(actual[:len(retained)] == retained and [signature(abi) for abi in actual[len(retained):]] == adaptation["added_signatures"], f"Adaptation diverges from reviewed removals/additions: {identity}")
    reviewed_ids = set()
    for review in reviews.values():
        require(review.get("reviewed_at") and review.get("source_ids"), f"Missing review provenance: {review['id']}")
        require(date.fromisoformat(review["reviewed_at"]).isoformat() == review["reviewed_at"], f"Invalid ISO review date: {review['id']}")
        require(set(review["source_ids"]) <= source_records.keys(), f"Unknown review source: {review['id']}")
        artifacts = review.get("source_chain", [])
        require(artifacts, f"Missing fingerprinted review artifacts: {review['id']}")
        for artifact in artifacts:
            require(artifact.get("url") and re.fullmatch(r"[0-9a-f]{64}", artifact.get("sha256", "")) and type(artifact.get("bytes")) is int and artifact["bytes"] > 0, "Invalid source artifact fingerprint")
        recorded = []
        for source_id in review["source_ids"]:
            record = source_records[source_id]
            recorded.extend(record.get("artifacts", []))
            if "complete_asset_sha256" in record:
                recorded.append({"sha256": record["complete_asset_sha256"], "bytes": record.get("complete_asset_bytes")})
        require(any(artifact["sha256"] == record.get("sha256") and artifact["bytes"] == record.get("bytes") for artifact in artifacts for record in recorded), "Review artifact does not match source record")
        if any("artifact_url" in coverage["source_fragment"] for coverage in review["interfaces"].values()):
            require(all(any(artifact["url"] == record.get("url")
                            and artifact["sha256"] == record.get("sha256")
                            and artifact["bytes"] == record.get("bytes")
                            for record in recorded) for artifact in artifacts),
                    f"Review artifact does not match source record: {review['id']}")
        for identity in review["interfaces"]:
            require(identity in interfaces and interfaces[identity]["review_id"] == review["id"], f"Dangling review interface: {identity}")
            reviewed_ids.add(identity)
    require(reviewed_ids == interfaces.keys(), "Unreviewed interface file")
    bindings = contracts_doc["bindings"]
    require(len({binding["id"] for binding in bindings}) == len(bindings), "Duplicate contract binding")
    used_interfaces = set()
    for binding in bindings:
        require(binding["review_id"] in reviews and binding["as_of"] == reviews[binding["review_id"]]["reviewed_at"], "Invalid dated binding review")
        require(type(binding["chain_id"]) is int and binding["chain_id"] > 0, "Invalid binding chain")
        require(re.fullmatch(r"0x[0-9a-fA-F]{40}", binding["address"]), "Invalid binding address")
        require(binding.get("generation") and binding.get("role") and binding.get("source_locator"), "Unqualified dated binding")
        require(set(binding["interface_ids"]) <= interfaces.keys(), "Unknown contract interface")
        require(binding.get("interface_status") in {"complete_publisher_definition", "selective_fragment", "unknown"}, "Missing binding coverage status")
        status = binding["interface_status"]
        complete = [interfaces[i]["coverage"]["source_definition_complete"] for i in binding["interface_ids"]]
        require((status == "unknown" and not complete) or (status == "complete_publisher_definition" and complete and all(complete)) or (status == "selective_fragment" and complete and not any(complete)), "Binding coverage status contradicts referenced definitions")
        require(all(interfaces[i]["review_id"] == binding["review_id"] for i in binding["interface_ids"]), "Binding interface review mismatch")
        require(not any(key in binding for key in {"active", "current", "default", "alias"}), "Runtime routing alias in dated binding")
        for interface_id, signatures in binding.get("selected_functions", {}).items():
            require(interface_id in binding["interface_ids"], "Selected function lacks interface")
            available = {entry["signature"] for entry in interfaces[interface_id]["entries"] if entry["abi"]["type"] == "function"}
            require(set(signatures) <= available, "Unknown selected binding function")
        used_interfaces.update(binding["interface_ids"])
    require(used_interfaces == interfaces.keys(), "Reviewed interface lacks dated role binding")
    capability_count = 0
    if "assets/interfaces/capabilities.json" in files:
        capability_doc = load("assets/interfaces/capabilities.json")
        require(capability_doc.get("schema_version") == 1, "Unsupported capability schema")
        capabilities = capability_doc["capabilities"]
        require(len({row["id"] for row in capabilities}) == len(capabilities), "Duplicate capability ID")
        for row in capabilities:
            capability_count += 1
            ids = row["interface_ids"]
            require(ids and set(ids) <= interfaces.keys(), f"Unknown capability interface: {row['id']}")
            require(row["review_ids"] and set(row["review_ids"]) <= reviews.keys(), f"Unknown capability review: {row['id']}")
            require({interfaces[i]["review_id"] for i in ids} <= set(row["review_ids"]), f"Capability review scope mismatch: {row['id']}")
            require(row["status"] in {"available", "not_exposed", "unknown"}, "Invalid capability status")
            require(row["status"] != "available" or bool(row.get("functions")), f"Available capability lacks function evidence: {row['id']}")
            for function in row.get("functions", []):
                require(function["interface_id"] in ids, "Capability function outside scope")
                available = {entry["signature"] for entry in interfaces[function["interface_id"]]["entries"] if entry["abi"]["type"] == "function"}
                require(function["signature"] in available, f"Missing capability function: {function['signature']}")
            for event in row.get("events", []):
                require(event["interface_id"] in ids, "Capability event outside scope")
                available = {entry["signature"] for entry in interfaces[event["interface_id"]]["entries"] if entry["abi"]["type"] == "event"}
                require(event["signature"] in available, f"Missing capability event: {event['signature']}")
            absent = row.get("absent_signatures", [])
            if row["status"] == "not_exposed" or absent:
                require(all(interfaces[i]["coverage"]["source_definition_complete"] for i in ids), f"Incomplete negative capability claim: {row['id']}")
                require(bool(absent), f"Negative capability lacks precise absence claim: {row['id']}")
                present = {entry["signature"] for i in ids for entry in interfaces[i]["entries"]}
                require(not set(absent) & present, f"False negative capability: {row['id']}")
            require(row.get("explanation") and row.get("question") and row.get("alternative_evidence"), "Unexplained capability or missing alternative evidence")
    return {"interfaces": len(interfaces), "entries": sum(len(item["entries"]) for item in interfaces.values()), "reviews": len(reviews), "contract_bindings": len(bindings), "capabilities": capability_count}


def validate_inventory(files):
    """Validate package bytes; malformed or inconsistent evidence raises ValueError."""
    try:
        return _validate_inventory(files)
    except (KeyError, TypeError, IndexError, AttributeError) as error:
        raise ValueError(f"Malformed inventory data: {error}") from error
