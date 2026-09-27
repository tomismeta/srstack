"""Optional, offline arithmetic for Python 3.10+; no transport or execution API.

Callers may use, adapt or ignore this module. It is not a required analysis
workflow or an evidence validator. Financial accounting uses integers/Fraction;
no helper accepts binary floats. Results contain Python Fraction/Decimal values,
not a prescribed JSON output format. Evidence v1 is an optional interchange.

Observed summaries never prove canonicality, receipt coverage, a round close or
complete history. Conflicting event variants are retained and excluded from
uncontested totals. Pending deltas are signed ledger changes, not earned income.
The exponential helper is an explicitly supplied mathematical scenario, NOT a
protocol equation or reproduction of deployed integer rounding.
"""

from copy import deepcopy
from decimal import Context, Decimal, ROUND_CEILING, ROUND_FLOOR, ROUND_HALF_EVEN
from fractions import Fraction
import json
import re


_DECIMAL_INTEGER = re.compile(r"0|[1-9][0-9]*")


def _integer(value, name):
    if type(value) is int:
        result = value
    elif isinstance(value, str) and _DECIMAL_INTEGER.fullmatch(value):
        result = int(value)
    else:
        raise ValueError(f"{name} must be a nonnegative integer or canonical decimal string")
    if result < 0:
        raise ValueError(f"{name} must be nonnegative")
    return result


def weighted_price(rows):
    """Exact totals for compatible (quantity, raw unit price) pairs.

    Caller establishes asset/scale compatibility. Quantity and raw price must be
    nonnegative integers (or decimal integer strings). Average stays in raw price
    units; quotient and remainder satisfy consideration = quotient*quantity +
    remainder. Empty or zero-quantity observations have no average, not zero.
    """
    quantity = consideration = 0
    for count, price in rows:
        count = _integer(count, "quantity")
        price = _integer(price, "unit_price_raw")
        quantity += count
        consideration += count * price
    quotient, remainder = divmod(consideration, quantity) if quantity else (None, None)
    return {"quantity": quantity, "consideration_raw": consideration,
            "average_raw": Fraction(consideration, quantity) if quantity else None,
            "quotient_raw": quotient, "remainder": remainder}


def _serialized(value):
    return json.dumps(value, sort_keys=True, separators=(",", ":"), allow_nan=False)


def _group_key(event):
    decoded = event["decoded"]
    denomination = event["denomination"]
    if denomination == "unknown":
        asset, decimals = "unknown", None
    else:
        asset = denomination["asset"]
        if not isinstance(asset, str) or not asset or asset == "unknown":
            raise ValueError("known denomination requires an asset identity")
        decimals = _integer(denomination["decimals"], "decimals")
    return (_integer(event["chain_id"], "chain_id"), event["emitter"],
            _integer(decoded["round_id"], "round_id"), asset, decimals)


def _position(event):
    return tuple(_integer(event[name], name) for name in
                 ("block_number", "transaction_index", "log_index"))


def _observations_at_position(events, headers, position):
    observations = []
    for event in events:
        if _position(event) != position:
            continue
        header_key = f"{event['chain_id']}:{event['block_hash']}"
        header = headers.get(header_key)
        timestamp = "unknown"
        if header is not None:
            variants = [header] + header.get("alternatives", [])
            timestamps = {item.get("timestamp", "unknown") for item in variants}
            matching = all(item.get("chain_id") == event["chain_id"] and
                           item.get("block_hash") == event["block_hash"] and
                           item.get("block_number") == event["block_number"] for item in variants)
            if matching and len(timestamps) == 1 and header.get("canonicality") != "conflicting":
                candidate = next(iter(timestamps))
                if candidate != "unknown":
                    try:
                        _integer(candidate, "timestamp")
                    except ValueError:
                        candidate = "unknown"
                timestamp = candidate
        observations.append({"event": event, "timestamp": timestamp, "header_ref": header_key})
    return observations


def summarize_rounds(document):
    """Summarize supplied v1 sale observations, without fetching anything.

    Requires full event identity, ordering, decoded quantity/raw price/round and
    denomination; incomplete records are deferred with scoped diagnostics.
    Log identity is (chain, transaction hash, log index), so changed block hashes
    or emitters are conflicts, not extra sales. Identical records are deduplicated;
    provenance/check variants are retained but identical economic content counts
    once. Removed logs are retained separately, never counted. Excluding them is
    not evidence of canonicality. Round keys include emitter and denomination.

    `uncontested_totals` is partial: conflicts, known-invalid receipt/header
    evidence, unknown denominations and deferred identities are excluded.
    First/last observed retain all equal-position ties, including disputed rows;
    neither is a closing sale. Conflicting block-global log slots, competing
    block hashes at one height and active/removed variants are disputed. Headers
    are reused by chain/hash; unknown/conflicting timestamps remain unknown.
    Provenance and coverage pass through without promoting verification status.
    """
    if document.get("schema_version") != "1":
        raise ValueError("expected evidence schema_version '1'")
    try:
        identities, removed, deferred = {}, {}, []
        for original in document["events"]:
            event = deepcopy(original)
            try:
                if type(event["removed"]) is not bool:
                    raise ValueError("removed must be boolean")
                _group_key(event)
                _position(event)
                for name in ("emitter", "block_hash", "transaction_hash"):
                    if not isinstance(event[name], str) or not event[name] or event[name] == "unknown":
                        raise ValueError(f"full {name} required")
                weighted_price([(event["decoded"]["quantity"], event["decoded"]["unit_price_raw"])])
                encoded = _serialized(event)
            except (KeyError, TypeError, ValueError) as error:
                deferred.append({"event": event, "reason": str(error)})
                continue
            if event["removed"]:
                removed[encoded] = event
                continue
            identity = (_integer(event["chain_id"], "chain_id"),
                        event["transaction_hash"], _integer(event["log_index"], "log_index"))
            identities.setdefault(identity, {})[encoded] = event
        groups, conflicts, disputed = {}, [], []
        deferred_identities = set()
        for item in deferred:
            event = item["event"]
            try:
                deferred_identities.add((_integer(event["chain_id"], "chain_id"),
                                         event["transaction_hash"], _integer(event["log_index"], "log_index")))
            except (KeyError, TypeError, ValueError):
                pass
        economic_fields = ("chain_id", "emitter", "block_number", "block_hash",
                           "transaction_hash", "transaction_index", "log_index", "decoded", "denomination")
        slots, heights = {}, {}
        removed_locations = {
            (_integer(event["chain_id"], "chain_id"), event["transaction_hash"],
             _integer(event["log_index"], "log_index"), event["block_hash"])
            for event in removed.values()
        }
        for identity, records in identities.items():
            for event in records.values():
                header = document["headers"].get(f"{event['chain_id']}:{event['block_hash']}", {})
                if any(item.get("canonicality") in ("noncanonical", "conflicting")
                       for item in [header] + header.get("alternatives", [])):
                    continue
                slots.setdefault((identity[0], event["block_hash"], identity[2]), set()).add(identity)
                heights.setdefault((identity[0], _position(event)[0]), set()).add(event["block_hash"])
        for identity, records in sorted(identities.items()):
            variants = [records[key] for key in sorted(records)]
            contents = {_serialized({name: event[name] for name in economic_fields}) for event in variants}
            raw_conflict = any(len({_serialized(event[name]) for event in variants if name in event}) > 1
                               for name in ("topics", "data"))
            conflicting = len(contents) > 1 or raw_conflict
            if conflicting:
                conflicts.append({"identity": identity, "variants": variants})
            reasons = set()
            if identity in deferred_identities:
                reasons.add("incomplete competing observation")
            for event in variants:
                if (*identity, event["block_hash"]) in removed_locations:
                    reasons.add("active and removed observations at the same location")
                if len(slots.get((identity[0], event["block_hash"], identity[2]), ())) > 1:
                    reasons.add("competing transactions at one block-global log index")
                if len(heights.get((identity[0], _position(event)[0]), ())) > 1:
                    reasons.add("competing block hashes at one height")
                if event["denomination"] == "unknown":
                    reasons.add("unknown denomination does not establish compatible units")
                header = document["headers"].get(f"{event['chain_id']}:{event['block_hash']}", {})
                if any(item.get("canonicality") in ("noncanonical", "conflicting")
                       for item in [header] + header.get("alternatives", [])):
                    reasons.add("noncanonical or conflicting header evidence")
                if any(check.get("status") == "mismatched" or check.get("transaction_status") == "reverted"
                       for check in event.get("receipt_checks", [])):
                    reasons.add("mismatched receipt or reverted transaction evidence")
                group = groups.setdefault(_group_key(event), {"events": [], "uncontested": []})
                group["events"].append(event)
            if reasons:
                disputed.append({"identity": identity, "variants": variants, "reasons": sorted(reasons)})
            if not conflicting and not reasons:
                groups[_group_key(variants[0])]["uncontested"].append(variants[0])
        summaries = []
        for key in sorted(groups, key=lambda item: (item[:4], -1 if item[4] is None else item[4])):
            group = groups[key]
            events = sorted(group["events"], key=lambda event: (_position(event), _serialized(event)))
            first = _observations_at_position(events, document["headers"], _position(events[0]))
            last = _observations_at_position(events, document["headers"], _position(events[-1]))
            first_times = {item["timestamp"] for item in first}
            last_times = {item["timestamp"] for item in last}
            span = None
            if len(first_times) == len(last_times) == 1 and "unknown" not in first_times | last_times:
                difference = int(next(iter(last_times))) - int(next(iter(first_times)))
                if difference >= 0:
                    span = difference
            summaries.append({"key": key, "events": events, "first_observed": first,
                              "last_observed": last, "observed_span_seconds": span,
                              "totals_scope": "partial supplied observations; conflicting, disputed and deferred identities excluded",
                              "uncontested_minimum_unit_price_raw": min(
                                  (_integer(event["decoded"]["unit_price_raw"], "unit_price_raw")
                                   for event in group["uncontested"]), default=None),
                              "uncontested_totals": weighted_price(
                                  (event["decoded"]["quantity"], event["decoded"]["unit_price_raw"])
                                  for event in group["uncontested"])})
        return {"rounds": summaries, "conflicts": conflicts,
                "deferred_events": sorted(deferred, key=_serialized),
                "disputed_events": disputed,
                "removed_events": [removed[key] for key in sorted(removed)],
                "sources": deepcopy(document["sources"]), "headers": deepcopy(document["headers"]),
                "coverage": deepcopy(document["coverage"])}
    except (KeyError, TypeError) as error:
        raise ValueError(f"incomplete or malformed evidence needed by summary: {error}") from error


def pending_delta_pace(opening_raw, closing_raw, opening_timestamp, closing_timestamp, *,
                       opening_asset, closing_asset, opening_scale, closing_scale, period_seconds):
    """Signed observed ledger change, using actual header times and explicit units.

    Scales are raw units per whole asset unit and must agree. Caller establishes
    compatible deployment/position and timestamps; equal endpoint units alone
    do not establish this. period_seconds is an explicit rescaling, not a claim
    of continuation or earnings. No default daily conversion is supplied.
    """
    opening = _integer(opening_raw, "opening_raw")
    closing = _integer(closing_raw, "closing_raw")
    elapsed = _integer(closing_timestamp, "closing_timestamp") - _integer(opening_timestamp, "opening_timestamp")
    scale = _integer(opening_scale, "opening_scale")
    if not scale or scale != _integer(closing_scale, "closing_scale"):
        raise ValueError("positive compatible raw scales required")
    if not isinstance(opening_asset, str) or not opening_asset or opening_asset == "unknown" or opening_asset != closing_asset:
        raise ValueError("compatible known asset identities required")
    period = _integer(period_seconds, "period_seconds")
    if elapsed <= 0 or period <= 0:
        raise ValueError("timestamps must increase and period_seconds must be positive")
    raw_pace = Fraction(closing - opening, elapsed)
    return {"label": "unattributed observed ledger-change pace", "asset": opening_asset,
            "raw_delta": closing - opening, "elapsed_seconds": elapsed,
            "raw_per_second": raw_pace, "amount_per_second": raw_pace / scale,
            "amount_per_period": raw_pace * period / scale, "period_seconds": period}


def estimate_workload(ranges, max_blocks_per_request, *, overlaps="reject"):
    """Arithmetic request estimate for inclusive block ranges; never scans.

    reject: overlapping endpoints are errors, adjacent ranges remain separate.
    normalize: union overlapping/adjacent ranges before chunking. This estimates
    range requests only, not pagination, receipts, provider retries or timing.
    """
    chunk = _integer(max_blocks_per_request, "max_blocks_per_request")
    if chunk == 0 or overlaps not in ("reject", "normalize"):
        raise ValueError("positive request span and reject/normalize overlap policy required")
    ordered = []
    for bounds in ranges:
        if not isinstance(bounds, (tuple, list)) or len(bounds) != 2:
            raise ValueError("each range requires exactly two endpoints")
        start, end = (_integer(value, "range endpoint") for value in bounds)
        if start > end:
            raise ValueError("range start exceeds end")
        ordered.append((start, end))
    normalized = []
    for start, end in sorted(ordered):
        if normalized and start <= normalized[-1][1]:
            if overlaps == "reject":
                raise ValueError("inclusive ranges overlap")
            normalized[-1] = (normalized[-1][0], max(end, normalized[-1][1]))
        elif normalized and overlaps == "normalize" and start == normalized[-1][1] + 1:
            normalized[-1] = (normalized[-1][0], end)
        else:
            normalized.append((start, end))
    return {"ranges": normalized, "blocks": sum(end - start + 1 for start, end in normalized),
            "range_requests": sum((end - start + chunk) // chunk for start, end in normalized),
            "overlaps": overlaps}


def _rational(value, name):
    if isinstance(value, bool) or not isinstance(value, (int, str, Decimal, Fraction)):
        raise ValueError(f"{name} requires an exact integer, Fraction or finite decimal")
    try:
        result = Fraction(value)
    except (ValueError, OverflowError, ZeroDivisionError) as error:
        raise ValueError(f"{name} requires a finite exact value") from error
    if abs(result) > 10 ** 1000 or (result and abs(result) < Fraction(1, 10 ** 1000)):
        raise ValueError(f"{name} magnitude outside supported [1e-1000, 1e1000]")
    return result


def gap_to_floor_scenario(opening, floor, half_life, elapsed, *, precision):
    """Bounded Decimal evaluation of floor + (opening-floor)*2**(-elapsed/half_life).

    Explicit mathematical scenario only. Times use the same caller-chosen unit;
    0 <= floor <= opening, half_life > 0, elapsed >= 0. No protocol defaults.
    precision is 16..200 significant decimal digits. Nonzero input magnitudes
    are limited to [1e-1000, 1e1000], elapsed/half_life to 10000. Beyond these
    computational limits raises ValueError, never silently clips the horizon.

    Work precision is precision+12 in an isolated deterministic Decimal context.
    Directed arithmetic and adjacent representable bounds around correctly
    rounded Decimal ln/exp enclose numerical error. Returned bounds and absolute
    error bound apply ONLY to this exact-input mathematical expression, not
    model uncertainty, input evidence, or deployed contract rounding.
    """
    if type(precision) is not int or not 16 <= precision <= 200:
        raise ValueError("precision must be an integer in [16, 200]")
    opening, floor, half_life, elapsed = (
        _rational(value, name) for value, name in
        ((opening, "opening"), (floor, "floor"), (half_life, "half_life"), (elapsed, "elapsed")))
    if not 0 <= floor <= opening or half_life <= 0 or elapsed < 0:
        raise ValueError("require 0 <= floor <= opening, half_life > 0, elapsed >= 0")
    ratio = elapsed / half_life
    if ratio > 10000:
        raise ValueError("elapsed/half_life exceeds computational limit 10000")
    work = precision + 12
    down = Context(prec=work, rounding=ROUND_FLOOR)
    up = Context(prec=work, rounding=ROUND_CEILING)
    nearest = Context(prec=work, rounding=ROUND_HALF_EVEN)

    def bound(value, context):
        return context.divide(Decimal(value.numerator), Decimal(value.denominator))

    if ratio.denominator == 1 or opening == floor:
        exact = floor + (opening - floor) / (2 ** ratio.numerator) if opening != floor else floor
        low, high = bound(exact, down), bound(exact, up)
    else:
        logarithm = nearest.ln(Decimal(2))
        log_low, log_high = nearest.next_minus(logarithm), nearest.next_plus(logarithm)
        exponent_low = down.multiply(bound(ratio, up).copy_negate(), log_high)
        exponent_high = up.multiply(bound(ratio, down).copy_negate(), log_low)
        exp_low = nearest.next_minus(nearest.exp(exponent_low))
        exp_high = nearest.next_plus(nearest.exp(exponent_high))
        low = down.add(bound(floor, down), down.multiply(bound(opening - floor, down), exp_low))
        high = up.add(bound(floor, up), up.multiply(bound(opening - floor, up), exp_high))
    lower = Context(prec=precision, rounding=ROUND_FLOOR).plus(low)
    upper = Context(prec=precision, rounding=ROUND_CEILING).plus(high)
    value = Context(prec=precision, rounding=ROUND_HALF_EVEN).plus(nearest.divide(nearest.add(low, high), Decimal(2)))
    error = up.max(up.subtract(value, lower), up.subtract(upper, value))
    return {"model": "gap-to-floor exponential mathematical scenario", "value": value,
            "lower_bound": lower, "upper_bound": upper, "absolute_error_bound": error,
            "precision": precision, "working_precision": work}
