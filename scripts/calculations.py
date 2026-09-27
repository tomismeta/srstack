"""Optional, offline arithmetic for Python 3.10+; no network or wallet API.

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


def _projection_contexts(precision):
    if type(precision) is not int or not 16 <= precision <= 200:
        raise ValueError("precision must be an integer in [16, 200]")
    return (Context(prec=precision + 12, rounding=ROUND_FLOOR),
            Context(prec=precision + 12, rounding=ROUND_CEILING),
            Context(prec=precision + 12, rounding=ROUND_HALF_EVEN))


def _decimal_fraction(value, context):
    return context.divide(Decimal(value.numerator), Decimal(value.denominator))


def _bounded_decimal(low, high, precision):
    """Round an enclosing interval outward, keeping numerical error separate."""
    _, up, nearest = _projection_contexts(precision)
    lower = Context(prec=precision, rounding=ROUND_FLOOR).plus(low)
    upper = Context(prec=precision, rounding=ROUND_CEILING).plus(high)
    value = Context(prec=precision, rounding=ROUND_HALF_EVEN).plus(
        nearest.divide(nearest.add(low, high), Decimal(2)))
    return {"value": value, "lower_bound": lower, "upper_bound": upper,
            "absolute_error_bound": up.max(up.subtract(value, lower),
                                           up.subtract(upper, value)),
            "precision": precision, "working_precision": precision + 12}


def _bounded_sqrt(value, precision):
    down, up, nearest = _projection_contexts(precision)
    if not value:
        return _bounded_decimal(Decimal(0), Decimal(0), precision)
    # Decimal sqrt is correctly rounded to nearest. Adjacent representable
    # values enclose each result even when the input division was inexact.
    low = nearest.next_minus(nearest.sqrt(_decimal_fraction(value, down)))
    high = nearest.next_plus(nearest.sqrt(_decimal_fraction(value, up)))
    return _bounded_decimal(low, high, precision)


def _round_identity(record):
    generation, contract = record["generation"], record["contract"]
    if not isinstance(generation, str) or not generation:
        raise ValueError("round generation must be a nonempty string")
    if not isinstance(contract, str) or not re.fullmatch(r"0x[0-9a-fA-F]{40}", contract):
        raise ValueError("round contract must be a 20-byte hex address")
    return {"generation": generation, "contract": contract.lower(),
            "day": _integer(record["day"], "day")}


def _round_order(record):
    window = record.get("scheduled_window") or {}
    start = window.get("start_unix")
    if start is not None:
        return _integer(start, "start_unix")
    for name in ("first_sale", "last_sale"):
        anchor = record.get(name)
        if anchor is not None and anchor.get("ts") is not None:
            return _integer(anchor["ts"], f"{name}.ts")
    return None


def _ordered_rounds(rounds, trailing):
    trailing = _integer(trailing, "trailing")
    if not trailing:
        raise ValueError("trailing must be positive")
    ordered, excluded, seen = [], [], set()
    for record in rounds:
        identity = _round_identity(record)
        key = tuple(identity.values())
        if key in seen:
            raise ValueError("duplicate generation/contract/day round identity")
        seen.add(key)
        order = _round_order(record)
        if order is None:
            excluded.append({"identity": identity, "reasons": ["chronology unavailable"]})
        else:
            ordered.append((order, key, record, identity))
    ordered.sort(key=lambda item: (item[0], item[1]))
    return [(item[2], item[3]) for item in ordered], excluded, trailing


def _sale_reasons(record, *, sellout):
    reasons = []
    if record.get("last_sale_price_raw") is None:
        reasons.append("no observed last sale price")
    else:
        _integer(record["last_sale_price_raw"], "last_sale_price_raw")
    provenance = record.get("provenance") or {}
    if provenance.get("timestamp_basis") != "block_headers":
        reasons.append("node-header sale timestamps unavailable")
    anchors = []
    for name in ("first_sale", "last_sale"):
        anchor = record.get(name)
        if anchor is None:
            if sellout or name == "last_sale":
                reasons.append(f"{name} anchor unavailable")
        else:
            anchors.append((_integer(anchor["block"], f"{name}.block"),
                            _integer(anchor["ts"], f"{name}.ts")))
    if len(anchors) == 2 and (anchors[0][0] > anchors[1][0] or anchors[0][1] > anchors[1][1]):
        reasons.append("sale anchors out of order")
    for field, position in (("head_block", 0), ("head_timestamp", 1)):
        head = provenance.get(field)
        if head is None:
            if sellout:
                reasons.append(f"{field} unavailable")
        elif any(anchor[position] > _integer(head, field) for anchor in anchors):
            reasons.append(f"sale anchor exceeds {field}")
    if sellout:
        if record.get("sellout") is not True:
            reasons.append("sellout not evidenced")
        if provenance.get("coverage") != "complete":
            reasons.append("coverage not complete")
        basis = provenance.get("sellout_basis")
        if not isinstance(basis, str) or not basis.strip():
            reasons.append("sellout basis unavailable")
        opening = record.get("start_price_raw")
        if opening is None or _integer(opening, "start_price_raw") == 0:
            reasons.append("positive opening unavailable")
        sold, cap = record.get("sold"), record.get("round_cap")
        if sold is None or cap is None:
            reasons.append("sold or round cap unavailable")
        elif not _integer(cap, "round_cap") or _integer(sold, "sold") != _integer(cap, "round_cap"):
            reasons.append("positive fully sold allocation not evidenced")
    return reasons


def _sale_sample(rounds, trailing, *, sellout):
    ordered, excluded, trailing = _ordered_rounds(rounds, trailing)
    qualified = []
    for record, identity in ordered:
        reasons = _sale_reasons(record, sellout=sellout)
        if reasons:
            excluded.append({"identity": identity, "reasons": reasons})
        else:
            qualified.append((record, identity))
    selected = qualified[-trailing:]
    if len(selected) < 2:
        raise ValueError("at least two qualified chronological round observations required")
    return selected, excluded, len(qualified)


def _ols(values):
    """Exact OLS for explicit (ordinal, raw value) observations."""
    count = len(values)
    x_mean = Fraction(sum(x for x, _ in values), count)
    y_mean = Fraction(sum(y for _, y in values), count)
    slope = sum((x - x_mean) * (y - y_mean) for x, y in values) / sum(
        (x - x_mean) ** 2 for x, _ in values)
    return slope, y_mean - slope * x_mean


def sellout_ratio_summary(rounds, *, trailing, precision):
    """Recent evidenced sellout close/open ratios; no live/default sample.

    Requires complete supplied coverage, a sellout basis, header sale anchors,
    positive opening/cap, and sold == cap > 0. These are evidence assertions,
    not independent verification of the chain or all historical rounds.
    """
    _projection_contexts(precision)
    selected, excluded, qualified_count = _sale_sample(rounds, trailing, sellout=True)
    ratios = [Fraction(_integer(record["last_sale_price_raw"], "last_sale_price_raw"),
                       _integer(record["start_price_raw"], "start_price_raw"))
              for record, _ in selected]
    mean = sum(ratios, Fraction()) / len(ratios)
    variance = sum((ratio - mean) ** 2 for ratio in ratios) / (len(ratios) - 1)
    return {"count": len(ratios), "selected_rounds": [identity for _, identity in selected],
            "ratios": ratios, "mean": mean, "sample_variance": variance,
            "sample_variance_ddof": 1,
            "sample_sd": _bounded_sqrt(variance, precision), "excluded": excluded,
            "qualified_count": qualified_count,
            "scope": "selected supplied evidenced sellouts only; not all history"}


def close_trend_projection(rounds, *, trailing):
    """Exact OLS of comparable observed last-sold prices, not policy openings.

    Caller establishes compatible units, generations and market regime.
    x=0..N-1 indexes selected observations, not elapsed time or resettable day
    IDs. Partial observations can be fitted, but are not promoted to closes.
    A negative extrapolation is retained, never clipped to a plausible price.
    """
    selected, excluded, qualified_count = _sale_sample(rounds, trailing, sellout=False)
    prices = [_integer(record["last_sale_price_raw"], "last_sale_price_raw")
              for record, _ in selected]
    slope, intercept = _ols(list(enumerate(prices)))
    return {"count": len(prices), "selected_rounds": [identity for _, identity in selected],
            "values_raw": prices, "slope_raw_per_round": slope,
            "intercept_raw": intercept, "next_raw": intercept + slope * len(prices),
            "axis": "ordinal_selected_round", "excluded": excluded,
            "qualified_count": qualified_count,
            "scope": "observed last-sold prices; not independently proved exhausted closes"}


def structural_close_projection(policy_open_raw, ratio_summary, *, precision):
    """Policy opening times exact mean ratio, with a descriptive ±1 sample SD.

    The band is empirical dispersion, not a confidence/prediction interval.
    Each band's endpoint has separate numerical bounds; negative lower
    endpoints are retained. The supplied opening is not a transaction quote.
    """
    opening = _rational(policy_open_raw, "policy_open_raw")
    mean = _rational(ratio_summary["mean"], "mean")
    variance = _rational(ratio_summary["sample_variance"], "sample_variance")
    if opening < 0 or mean < 0 or variance < 0:
        raise ValueError("opening, mean and sample variance must be nonnegative")
    if _integer(ratio_summary["count"], "count") < 2:
        raise ValueError("sample dispersion requires at least two observations")
    down, up, _ = _projection_contexts(precision)
    sd = _bounded_sqrt(variance, precision)
    central = opening * mean
    center_low, center_high = _decimal_fraction(central, down), _decimal_fraction(central, up)
    spread_low = down.multiply(_decimal_fraction(opening, down), sd["lower_bound"])
    spread_high = up.multiply(_decimal_fraction(opening, up), sd["upper_bound"])
    lower = _bounded_decimal(down.subtract(center_low, spread_high),
                             up.subtract(center_high, spread_low), precision)
    upper = _bounded_decimal(down.add(center_low, spread_low),
                             up.add(center_high, spread_high), precision)
    return {"central_raw": central, "mean": mean, "sample_variance": variance,
            "sample_sd": sd, "band_raw": {"lower": lower, "upper": upper},
            "band_kind": "mean plus/minus one sample standard deviation; descriptive only",
            "band_standard_deviations": 1, "is_confidence_interval": False,
            "is_executable_quote": False}


def floor_trend_context(rounds, *, trailing):
    """Historical floor context; never extrapolate a future policy floor.

    Missing observations stay in the series as None. Known-floor OLS uses
    original selected-round ordinals, preserving gaps, and needs two values.
    """
    ordered, excluded, trailing = _ordered_rounds(rounds, trailing)
    selected = ordered[-trailing:]
    series, known = [], []
    for ordinal, (record, identity) in enumerate(selected):
        floor = record.get("floor_price_raw")
        if floor is not None:
            floor = _integer(floor, "floor_price_raw")
            known.append((ordinal, floor))
        series.append({"identity": identity, "floor_price_raw": floor})
    slope, intercept = _ols(known) if len(known) >= 2 else (None, None)
    return {"series": series, "count": len(series), "known_count": len(known),
            "slope_raw_per_round": slope, "intercept_raw": intercept,
            "axis": "ordinal_selected_round", "excluded": excluded,
            "future_floor_raw": None, "scope": "historical context only"}


def project_next_close(dataset, *, trailing, policy_multiplier, precision):
    """Compose two conditional close estimates from an explicit curated dataset.

    Caller must consult the latest relevant dataset, verify freshness/coverage,
    comparable units/regime and applicability of the supplied policy multiplier.
    This function fetches nothing, has no wall clock and certifies none of those
    premises. Excluded records and the latest observed print remain visible.
    """
    if dataset.get("schema_version") != "1":
        raise ValueError("expected round dataset schema_version '1'")
    multiplier = _rational(policy_multiplier, "policy_multiplier")
    if multiplier <= 0:
        raise ValueError("policy_multiplier must be positive")
    rounds = dataset["rounds"]
    ratios = sellout_ratio_summary(rounds, trailing=trailing, precision=precision)
    selected, _, _ = _sale_sample(rounds, trailing, sellout=True)
    trend = close_trend_projection([record for record, _ in selected], trailing=trailing)
    last, identity = selected[-1]
    last_close = _integer(last["last_sale_price_raw"], "last_sale_price_raw")
    opening = last_close * multiplier
    ordered, unordered, _ = _ordered_rounds(rounds, trailing)
    if unordered or ordered[-1][1] != identity:
        raise ValueError("latest supplied round must be a qualified sellout close; stale target unavailable")
    observations = [(record, ident) for record, ident in ordered
                    if record.get("last_sale_price_raw") is not None and record.get("last_sale") is not None]
    observed = None
    if observations:
        record, ident = max(observations, key=lambda item: (
            _integer(item[0]["last_sale"]["ts"], "last_sale.ts"),
            _integer(item[0]["last_sale"]["block"], "last_sale.block")))
        observed = {"identity": ident,
                    "price_raw": _integer(record["last_sale_price_raw"], "last_sale_price_raw"),
                    "anchor": deepcopy(record["last_sale"]),
                    "is_qualified_sellout_close": not _sale_reasons(record, sellout=True)}
    return {"policy_open": {"value_raw": opening, "multiplier": multiplier,
                            "source_round": identity, "is_expected_transaction_price": False},
            "target": {"after_round": identity, "kind": "next_round_after_latest_qualified_close",
                       "day": None, "scheduled_window": None},
            "trend": trend, "structural": structural_close_projection(opening, ratios, precision=precision),
            "ratio_summary": ratios, "last_observed": observed,
            "last_qualified_close": {"identity": identity, "price_raw": last_close,
                                     "anchor": deepcopy(last["last_sale"])},
            "floor_context": floor_trend_context(rounds, trailing=trailing),
            "future_floor_raw": None, "excluded": ratios["excluded"],
            "dataset_context": {key: deepcopy(dataset.get(key)) for key in
                                ("chain_id", "auction_family", "price_unit", "curated_at", "synthetic")},
            "assumptions": {
                "conditional_on_sellout_continuing": True,
                "latest_relevant_dataset_and_freshness_verified_by_helper": False,
                "comparable_units_and_regime_required": True,
                "policy_multiplier_is_explicit_scenario": True,
                "all_history_proved_soldout": False,
                "is_executable_quote": False,
                "scope": "next round after latest supplied qualified close; missing history remains unknown"}}


def auction_curve_quote(opening, floor, half_life, elapsed, *, remaining_today, precision):
    """Inventory-gated diagnostic curve, not a deployed quote or fill guarantee.

    Zero remaining inventory is the only sold-out tripwire here. Unknown
    inventory (None) yields no buyable price. Positive remaining inventory
    does not establish authorization, timing or any other purchase constraint.
    """
    remaining = None if remaining_today is None else _integer(remaining_today, "remaining_today")
    curve = gap_to_floor_scenario(opening, floor, half_life, elapsed, precision=precision)
    opening, floor, half_life, elapsed = (
        _rational(value, name) for value, name in
        ((opening, "opening"), (floor, "floor"), (half_life, "half_life"), (elapsed, "elapsed")))
    ratio = elapsed / half_life
    exact = None
    if opening == floor:
        exact = floor
    elif ratio.denominator == 1:
        exact = floor + (opening - floor) / (2 ** ratio.numerator)
    status = ("availability_unknown" if remaining is None else
              "phantom_not_buyable" if remaining == 0 else "inventory_conditional")
    return {"status": status, "remaining_today": remaining,
            "buyable_price_raw": curve["value"] if remaining is not None and remaining > 0 else None,
            "diagnostic_curve": curve, "exact_curve_raw": exact,
            "is_guaranteed_fill": False,
            "scope": "mathematical curve only; inventory is necessary, not sufficient, for purchase"}
