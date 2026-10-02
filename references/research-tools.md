# Optional offline research tools and evidence

These are optional aids, not a dependency, required workflow, answer gate or prescribed tool budget. Use, adapt or ignore them; an independent exact calculator, host-native code or another suitable evidence format is equally valid. Missing helpers do not block an answer whose arithmetic and evidence can be established another way. The [research guidance](research-workflow.md) and [history guidance](auction-history.md) describe the underlying distinctions, not a required sequence of calls.

## Installed optional library, CLI and schema

The installed skill includes `scripts/calculations.py`, the thin `scripts/research.py` CLI, `assets/schemas/research-evidence-v1.json` and the fictional replay input `assets/examples/research-evidence-v1.json`. The [worked example](research-example.md) shows its replay and exact table/duration display without introducing another CLI mode. The library and CLI use Python 3.10+ and only its standard library; there are no dependencies or install hooks. A source checkout is not needed to use them. Regression tests and their fixtures remain source-only under `research/`; the installed example is separately maintained teaching input, not live evidence. Loading or installing the skill does not automatically execute anything. No provider, RPC transport, fixed address, live price, live rate or fixed allocation is supplied by these helpers.

Choose to run the reviewed installed code only under existing [host permissions](safety.md#public-retrieval-and-calls), or use another language, host tool or independent calculation. Bundling code grants no execution, retrieval or storage permission. Nothing here permits signing, transactions, wallet-secret access or a change to the existing wallet boundary. These tools calculate supplied inputs; they neither collect evidence nor execute protocol actions.

For next-close forecasts, consult the latest relevant [curated round dataset](round-datasets.md) before policy derivation. Six additional direct-library [calculation recipes](calculations.md) provide exact close/open statistics and ordinal trends, bounded descriptive dispersion, historical floor context with unknown future floor, a composed conditional forecast, and an inventory-gated curve quote. `assets/schemas/round-dataset-v1.json` and the explicitly fictional `assets/examples/projection-evidence-v1.json` support those recipes. They add no CLI command; the existing bare `curve` command remains a mathematical diagnostic, not an inventory-aware executable quote.

For S-Bill scheduled maturities, the direct-library [`sbill_maturity_cohort` recipe](calculations.md#s-bill-maturity-cohort) counts supplied pinned bill records in an explicit timezone-resolved `[start,end)` interval and sums active principal/booked premium exactly. Active and settled remain independent; duplicate IDs cannot double count. It does not discover bills, establish historical activity or redemption eligibility, calculate bonuses/actual payouts, or add a CLI mode or schema. See [S-Bill evidence boundaries](sbills.md).

`weighted-price` rows must each be a two-element list/tuple pair; strings or dictionaries are not pairs. Direct-library callers may still supply an outer iterator of valid pairs.

### CLI inputs and exact JSON output

Use `python3 -I -B /absolute/path/to/installed/srstack/scripts/research.py COMMAND`. Supply one JSON object on stdin, or select a UTF-8 file with `COMMAND --input /absolute/path/to/input.json`; the file replaces stdin. Resolve the script path from the actual loaded installation, not the working directory. `-I -B` is supported: isolated Python execution does not require a source checkout, `PYTHONPATH` or bytecode writes.

| Command | Input object | Calculation |
| --- | --- | --- |
| `weighted-price` | `{"rows":[[quantity,raw_price],...]}` | `weighted_price(rows)`: compatible nonnegative quantity/raw-unit-price pairs; the caller establishes units. |
| `rounds` | Full evidence-v1 document: `schema_version: "1"`, `sources`, `headers`, `events`, `coverage`, with optional extensions described below | `summarize_rounds(document)`: observed groups, exact uncontested totals, conflicts, removed/deferred records and supplied coverage. Not a schema validator. |
| `pace` | `opening_raw`, `closing_raw`, `opening_timestamp`, `closing_timestamp`, `opening_asset`, `closing_asset`, `opening_scale`, `closing_scale`, `period_seconds` | `pending_delta_pace(...)`: equal known asset identities and positive scales, increasing timestamps, explicit positive display period. Scales mean raw units per whole asset; times are integer seconds. |
| `workload` | `ranges: [[from_block,to_block],...]`, `max_blocks_per_request`, optional `overlaps: "reject"` or `"normalize"` | `estimate_workload(...)`: inclusive nonnegative bounds and positive maximum range length. Default overlap rejection is arithmetic behavior, not a provider limit. Normalization unions overlapping/adjacent ranges before estimating. No scan is started. |
| `curve` | `opening`, `floor`, `half_life`, `elapsed`, `precision` | `gap_to_floor_scenario(...)`: the explicitly assumed mathematical curve below, not a protocol price oracle. Times share a caller-chosen unit; precision is a JSON integer from 16 through 200, not a string. |

For `pace`, `workload` and `curve`, keys are exactly the function parameter names; no wrapper object is used. Integer financial fields accept JSON integers or canonical nonnegative decimal strings (`"0"` or a nonzero digit followed by digits), not booleans, signs, leading zeroes, decimal points or exponent notation. The CLI parses fractional/exponent JSON number tokens directly as exact lexical strings, never binary floats: curve input `1.25` and `"1.25"` both retain exact value, while integer fields reject `1.0` and `1e3`. Curve values also accept rational strings such as `"1/3"`. Nonfinite numbers, duplicate object keys and malformed JSON are rejected.

Output is the direct calculation result as one JSON value on stdout, not a status envelope. Every Python integer, including counts, indices, precision and passed-through integer metadata, becomes a decimal string; signed results retain their minus sign. `Fraction` becomes `{"numerator":"...","denominator":"..."}`, `Decimal` becomes a string, arrays remain arrays, and booleans/null remain booleans/null. Fractional/exponent input tokens passed through in evidence retain their exact spelling as strings. No output numeric value requires a consumer to round through binary floating point. The library itself returns Python integers, `Fraction` and `Decimal`.

Exit **0** after a calculation means only that calculation completed; it does not certify evidence, coverage, receipts, canonicality, a round close or economic meaning. Standard `--help` also exits 0 without calculating. Exit **2** reports invalid arguments/input or an input-read failure on stderr. Successful partial summaries may retain unknown, deferred, disputed or removed observations. Neither CLI success nor optional JSON Schema validation is an answer or completeness gate.

### Small fictional stdin examples

Set `SRSTACK_ROOT` to the absolute path of the reviewed installed skill. These examples need no source-only fixtures, network access or live configuration; none is a financial observation:

```sh
SRSTACK_ROOT='/absolute/path/to/installed/srstack'
python3 -I -B "$SRSTACK_ROOT/scripts/research.py" weighted-price <<'JSON'
{"rows":[["2","105"],["3","99"]]}
JSON
python3 -I -B "$SRSTACK_ROOT/scripts/research.py" pace <<'JSON'
{"opening_raw":"1000","closing_raw":"970","opening_timestamp":"100","closing_timestamp":"110","opening_asset":"FICTIONAL_UNIT","closing_asset":"FICTIONAL_UNIT","opening_scale":"100","closing_scale":"100","period_seconds":"60"}
JSON
python3 -I -B "$SRSTACK_ROOT/scripts/research.py" workload <<'JSON'
{"ranges":[["10","19"],["30","34"]],"max_blocks_per_request":"4","overlaps":"reject"}
JSON
python3 -I -B "$SRSTACK_ROOT/scripts/research.py" curve <<'JSON'
{"opening":"10","floor":"2","half_life":"4","elapsed":"4","precision":32}
JSON
python3 -I -B "$SRSTACK_ROOT/scripts/research.py" rounds <<'JSON'
{"schema_version":"1","sources":[],"headers":{},"events":[],"coverage":{"requested":[],"scanned":[],"failed":[],"unsearched":[]},"assumptions":[{"label":"Fictional empty packet; no history coverage supplied"}]}
JSON
```

The weighted-price example's exact raw consideration is `507`, quantity is `5` and raw average is `507/5`, with quotient `101` and remainder `2`. The pace example deliberately has a negative ledger delta, not negative proved earnings. The rounds example supplies no observations or coverage; an empty summary cannot establish zero historical sales.

For a file instead of stdin, use `python3 -I -B "$SRSTACK_ROOT/scripts/research.py" rounds --input /absolute/path/to/evidence.json`. Keep research inputs/results outside the installed skill.

### Import the installed library

Direct callers can choose their own exact result handling without using the CLI. This explicit installed-path import works from any working directory and with Python isolation:

```sh
python3 -I -B - "$SRSTACK_ROOT/scripts" <<'PY'
import sys
from pathlib import Path

scripts = Path(sys.argv[1])
if not scripts.is_absolute():
    raise SystemExit("Supply the absolute installed scripts path")
sys.path.insert(0, str(scripts))
from calculations import weighted_price

print(weighted_price([("2", "105"), ("3", "99")]))
PY
```

`summarize_rounds(document)` performs arithmetic on the supplied observations. Its output does not make synthetic, index-only, incomplete or unverified inputs authoritative. Round outputs include ordered `first_observed`/`last_observed` records, header-derived `observed_span_seconds` when known, an uncontested minimum raw unit price and exact uncontested totals. Ties and disputed observations remain visible; none is automatically a closing sale. Deferred, conflicting and removed records are retained with provenance, and unavailable grouping/arithmetic inputs are not zero. Other established facts or conditional results remain usable.

## Exact arithmetic versus a mathematical scenario

Preserve unrounded input integers, asset identities and scales. Decimal-string serialization avoids JSON consumers silently rounding large financial integers. Use integer or rational arithmetic for exact calculations; where a scenario requires approximate numerical work, state precision, rounding and its effect at whole-purchase thresholds. These formulas are arithmetic identities or explicitly conditional models, **not certified deployed contract formulas**:

- **Scale:** with raw integer `x` and authenticated decimals `d`, the exact asset amount is `x / 10^d`. Format from integer digits or an exact rational, not a binary float. Unknown denomination leaves the amount raw; a stablecoin is not automatically USD.
- **Unit-price consideration:** when the event's authenticated semantics are quantity `q_i` at raw unit price `p_i`, `C_raw = sum(q_i × p_i)` and `Q = sum(q_i)`. For `Q > 0`, the quantity-weighted raw price is `C_raw / Q`; the asset price is `C_raw / (Q × 10^d)`. Preserve numerator and denominator for repeating decimals. For zero observed quantity there is no defined weighted sale price. Recompute totals from raw event units and quantities; never re-multiply a rounded displayed average by quantity or average event prices/already averaged rounds. See the [exact table and duration recipe](research-example.md#exact-table-and-duration) for display only.
- **Observed pending pace:** for the same authenticated position at header times `t0 < t1`, `r_raw = (P1 − P0) / (t1 − t0)`. With known decimals, `r_asset = r_raw / 10^d`; a daily equivalent is `86,400 × r_asset`. The difference can be negative. This is ledger-change pace, not earnings, until flows, ownership, eligibility and other contamination are addressed. Rescaling an observation is not proof of future continuation.
- **Per-asset reconciliation:** `closing = opening + inflows − outflows + evidenced adjustments`. Classify deposits, earnings, refunds, transfers and costs separately. An unexplained residual remains unexplained; do not force it into income.
- **Earned-budget accounting:** `available = verified unspent earned opening + future earned accrual − later earned debits − outstanding earned reservations`. Opening already reflects prior consumption. A filled reservation is replaced by actual spend, not deducted again; cancellation releases it. Unknown funding origin is not zero and not verified earnings.
- **One-state fixed-price bound:** with compatible units, positive fixed price `p`, spendable funds `S`, inventory `I`, allowance `A` and remaining capacity `C`, `q = min(floor(S / p), I, A, C)`. This is qualified by authenticated constraints and any fees, lot rules or execution gates. Unknown constraints stay unknown; a funds-only bound is not permission or a fill. Carry budget and constraints through resets instead of multiplying one snapshot across a horizon.
- **Work estimate:** for disjoint inclusive block intervals `[a_i, b_i]` and a supported maximum range length `L > 0`, the baseline request count is `sum(ceil((b_i − a_i + 1) / L))`. Reconcile or explicitly retain overlap; account separately for pagination, caps, retries, headers and receipts. The count estimates work, never proves completeness. Choose actual host/provider limits, not a skill-wide constant.

Continuous-share projections, assumed auction decay, future dilution and reinvestment paths are separate scenarios. Expose their equations, rates, scales, start state and horizon; distinguish effective activation, issuance, epoch and reset boundaries from hypothetical continuation. A sampled rate alone does not establish indefinite continuation, an unknown getter scale or a deployed checkpoint/integer-rounding rule. Independently chosen models remain useful when their assumptions and evidence limits are clear. See [accrual evidence and scenario limits](research-workflow.md#accrual-evidence).

The optional `pending_delta_pace` API requires explicit opening/closing asset identities and equal positive raw-units-per-asset scales, actual increasing integer timestamps and an explicit display period. It returns signed exact rational arithmetic rather than silently clamping a negative observation.

The separately named `gap_to_floor_scenario(opening, floor, half_life, elapsed, *, precision)` models the **assumed** curve `price(t) = floor + (opening − floor) × 2^(−t / half_life)`. All parameters come from the caller; no rate, duration or floor is a protocol default. It requires `0 ≤ floor ≤ opening`, positive half-life, nonnegative elapsed time and explicit decimal precision. Exact integer/rational/decimal inputs avoid binary-float contamination. Its approximation and lower/upper/error outputs qualify numerical error only, not model uncertainty or on-chain rounding. The API documents finite precision/magnitude limits for computation; they are not chain economics, retrieval budgets or restrictions on independent analysis.

`weighted_price` retains raw consideration, quantity, exact `Fraction` average and quotient/remainder. `estimate_workload` offers explicit overlap rejection or normalization; neither option starts a scan. Library return values use Python integers, `Fraction` and `Decimal`, not a required report format. For persistence, the host can serialize exact numerator/denominator pairs or decimal strings and retain its own source/evidence links.

### Fictional round worked by hand

This deliberately small example is separate from the regression fixture and is **not a live observation**. Assume a fictional asset `FICTIONAL_UNIT` with two decimals and an authenticated unit-price meaning only for this illustration. There are two synthetic purchases in one synthetic emitter/round:

| Ordered sale | Quantity | Raw unit price | Exact asset unit price | Raw consideration |
| --- | ---: | ---: | ---: | ---: |
| First | 2 | 105 | 1.05 | 210 |
| Last observed | 3 | 99 | 0.99 | 297 |

`Q = 2 + 3 = 5`; `C_raw = 210 + 297 = 507`, or exactly `5.07 FICTIONAL_UNIT`. The exact weighted price is `507 / (5 × 100) = 1.014 FICTIONAL_UNIT` per unit; a raw weighted price need not be an integer. The minimum observed price is `0.99`, and the last observed price is also `0.99`. Neither is an authenticated contract floor or future offer. No gas, refund or fee claim is included.

Suppose a fictional scheduled opening is at time `1000`, first purchase at `1010` and last observed purchase at `1030`, all in seconds on the same clock. The observed selling span is `20` seconds; scheduled-opening-to-last-observed-sale is `30` seconds. With no independent capacity/exhaustion and full-scope history evidence, neither duration establishes sellout, and the last observed sale is **not** a proved closing sale. Empty observations would not establish a zero-sale round without the relevant scope evidence.

## Optional external evidence interchange

The installed `assets/schemas/research-evidence-v1.json` defines version `"1"` as a portable example, not required storage, an access policy or a closed-world census. The host may choose any authorized external artifact and adapt any format. There is no default storage directory. Do not put live observations back into skill resources or persist credentials, provider API keys, secret endpoint query strings, wallet material or unrelated private data. Ordinary questions do not require persistence.

The optional document keeps these concerns distinct:

- `sources`: source ids and original public identities, public query/anchor metadata as needed, retrieval time and observation time (or `"unknown"`); publication time is separately optional. These times do not replace actual block timestamps.
- `headers`: a reusable map keyed `"<decimal chain_id>:<block_hash>"`, with chain, height, hash, integer-seconds timestamp (or `"unknown"`), optional source references and time-qualified canonicality checks. Fetch a relevant header once per distinct hash for a given collection pass and reuse it; recheck affected evidence on observed reorgs, competing hashes/headers, removed/disputed logs or a refresh crossing a declared provisional boundary. A provider transition calls for a scoped overlap/anchor cross-check, not automatic invalidation or full refetch. Retain replacement hashes at the same height and conflicting same-hash observations in `alternatives`; partial unkeyed observations can live in `unresolved_headers`.
- `events`: chain, emitter, generation when known, block/transaction hashes, numeric ordering, removed flag, optional raw topics/data, decoded fields and denomination. Ingest the full block number/hash, transaction hash/index, log index, emitter, removed flag and topics/data whenever `eth_getLogs` supplies them, together with the known chain and source context; do not wait for receipts to preserve identity. Chain ids, heights, indices, charter/round ids, quantities and raw unit prices are decimal strings; unknown fields are not zero. Decoded data remains an observation requiring ABI and semantic authentication. Known denomination is `{ "asset": "FICTIONAL_UNIT", "decimals": "2" }`; unknown denomination is the literal `"unknown"`. Header references use chain plus hash, never height alone.
- `receipt_checks` versus `verification_checks`: matching a log against a receipt and observing transaction success are narrower than authenticating event meaning, verifying current canonicality, proving a refund or establishing complete history. Preserve individual check outcomes and sources, including mismatches and unavailable checks, rather than a blanket verified flag.
- `coverage`: requested, scanned, failed and unsearched inclusive block ranges, with chain/emitter/generation/filter scope and pagination or stopping evidence where useful. Generation discovery, index/log scope, receipt checks and canonical header checks are distinct. Counts are descriptive, not proof. Empty arrays mean no supplied range evidence, not complete coverage or zero events. A scanned range does not by itself prove uncapped, exhaustive discovery, and a final index page proves only the index's evidenced universe.
- `assumptions` and `results`: separate assumptions from source observations and derived outputs. Preserve formulas, exact values, units, source/input references and claim-specific limitations in the chosen extension fields.

The schema accepts extensions and partial/unknown observations. Required structural slots are a convention only for someone choosing this interchange; they do not require every question to discover a complete universe. JSON Schema validation checks shape, not source truth, cross-reference consistency, range arithmetic or economic semantics. Preserve a degraded record with its source and missing fields even when it cannot support aggregation; another supported claim can still use it.

The optional `rounds` calculation has stricter arithmetic prerequisites than the permissive schema: full chain/emitter/block/transaction/log identity, block/transaction/log ordering, an explicit removed flag, decoded round id, quantity and raw unit price, and a denomination field. Incomplete records are deferred with their provenance. Unknown denomination may remain an observation/group, but cannot establish compatible units for `uncontested_totals`; those totals require known asset identity and scale and exclude removed, conflicting, disputed and deferred identities and known-invalid receipt/header evidence. Complete-looking fields do not prove canonicality, receipt matching or exhaustive coverage; “uncontested” is a calculation over supplied evidence, not a certification. Schema-valid partial evidence therefore need not yield an uncontested total, while useful source-scoped observations remain available.

For a derived ledger, reconcile canonicality before deduplicating by chain/transaction hash/log index. Preserve raw duplicates, their sources, conflicts and reorg alternatives; do not silently pick the first conflicting row or erase evidence. Exclude removed/noncanonical observations from an asserted canonical total. Order retained executions by block, transaction and log position, not retrieval arrival. Keep chain, emitter, round and denomination groups separate, including generations that reuse round ids. An exact subtotal can be valid for a partial scope without being a full-history total.

For optional incremental reuse, retain coverage gaps and provisional boundaries alongside observations. Retrieve only the additional scope or checks the question needs, reconcile overlap and canonical replacements before changing derived totals, and keep displaced/conflicting source observations rather than blindly appending or erasing them. [History guidance](auction-history.md#optional-incremental-evidence-reuse) supplies concrete refresh/cross-check triggers. Neither an external artifact, a mandatory dataset pipeline, a full rescan nor a never-refetch policy is required.

A receipt-verified last sale becomes a historical **closing sale** only with complete ordered purchase coverage through the relevant endpoint and authenticated historical inventory exhaustion, including capacity changes and reopenings. Receipt matching cannot prove discovery omitted nothing; log coverage cannot independently establish refund flows; headers do not prove economic semantics. Preserve these separate outcomes rather than demanding universal completeness before sharing any useful result.
