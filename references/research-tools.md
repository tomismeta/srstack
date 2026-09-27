# Optional offline research tools and evidence

These are optional aids, not a dependency, required workflow, answer gate or prescribed tool budget. Use, adapt or ignore them; an independent exact calculator, host-native code or another suitable evidence format is equally valid. Missing helpers do not block an answer whose arithmetic and evidence can be established another way. The [research guidance](research-workflow.md) and [history guidance](auction-history.md) describe the underlying distinctions, not a required sequence of calls.

## Source checkout, not installed execution

The [source repository](https://github.com/tomismeta/srstack)'s `research/` directory contains a standard-library Python calculation module (`calculations.py`), an optional JSON Schema (`evidence.schema.json`) and fictional regression fixtures (`fixtures/`). These are source-only maintenance resources, not code or live datasets installed with the skill. This runtime reference does not fetch, install or execute anything. No CLI, provider, RPC transport, fixed address, live price, live rate or fixed allocation is supplied by these helpers.

If useful, inspect a source checkout under the host's existing permissions at the reviewed commit recorded in the external installation record, and choose to run its offline library. Otherwise use the host's preferred tools, language or dependencies, or write an independent calculation. A documentation link does not grant execution permission or justify running unreviewed external code; ordinary [host permissions](safety.md#public-retrieval-and-calls) still apply to code, dependencies, public retrieval and artifact storage. Nothing here permits signing, transactions, wallet-secret access or a change to the existing wallet boundary.

For an optional example, run this **from the skill directory of an inspected source checkout** (the directory containing `research/`). It uses only the synthetic fixture, not network data:

```sh
python3 - <<'PY'
import json
import sys
from pathlib import Path
from pprint import pprint

root = Path.cwd()
sys.path.insert(0, str(root / "research"))
from calculations import summarize_rounds

fixture = json.loads((root / "research/fixtures/round-v1.json").read_text())
pprint(summarize_rounds(fixture))
PY
```

`summarize_rounds(document)` performs arithmetic on the supplied observations. Its output does not make synthetic, index-only, incomplete or unverified inputs authoritative. The fixture's values and routing metadata are fictional. Round outputs include ordered `first_observed`/`last_observed` records, header-derived `observed_span_seconds` when known, an uncontested minimum raw unit price and exact uncontested totals. Ties and disputed observations remain visible; none is automatically a closing sale. Deferred, conflicting and removed records are retained with provenance, and unavailable grouping/arithmetic inputs are not zero. Other established facts or conditional results remain usable.

## Exact arithmetic versus a mathematical scenario

Preserve unrounded input integers, asset identities and scales. Decimal-string serialization avoids JSON consumers silently rounding large financial integers. Use integer or rational arithmetic for exact calculations; where a scenario requires approximate numerical work, state precision, rounding and its effect at whole-purchase thresholds. These formulas are arithmetic identities or explicitly conditional models, **not certified deployed contract formulas**:

- **Scale:** with raw integer `x` and authenticated decimals `d`, the exact asset amount is `x / 10^d`. Format from integer digits or an exact rational, not a binary float. Unknown denomination leaves the amount raw; a stablecoin is not automatically USD.
- **Unit-price consideration:** when the event's authenticated semantics are quantity `q_i` at raw unit price `p_i`, `C_raw = sum(q_i × p_i)` and `Q = sum(q_i)`. For `Q > 0`, the quantity-weighted raw price is `C_raw / Q`; the asset price is `C_raw / (Q × 10^d)`. Preserve numerator and denominator for repeating decimals. For zero observed quantity there is no defined weighted sale price. Do not average event prices or already averaged rounds.
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

`research/evidence.schema.json` defines version `"1"` as a portable example, not required storage, an access policy or a closed-world census. The host may choose any authorized external artifact and adapt any format. There is no default storage directory. Do not put live observations back into skill resources or persist credentials, provider API keys, secret endpoint query strings, wallet material or unrelated private data. Ordinary questions do not require persistence.

The optional document keeps these concerns distinct:

- `sources`: source ids and original public identities, public query/anchor metadata as needed, retrieval time and observation time (or `"unknown"`); publication time is separately optional. These times do not replace actual block timestamps.
- `headers`: a reusable map keyed `"<decimal chain_id>:<block_hash>"`, with chain, height, hash, integer-seconds timestamp (or `"unknown"`), optional source references and time-qualified canonicality checks. Fetch a relevant header once per distinct hash for a given collection pass and reuse it; **recheck on reorgs, anchor changes or conflicts**, and refetch when needed. This is not a “never refetch” rule. Retain replacement hashes at the same height and conflicting same-hash observations in `alternatives`; partial unkeyed observations can live in `unresolved_headers`.
- `events`: chain, emitter, generation when known, block/transaction hashes, numeric ordering, removed flag, optional raw topics/data, decoded fields and denomination. Chain ids, heights, indices, charter/round ids, quantities and raw unit prices are decimal strings; unknown fields are not zero. Decoded data remains an observation requiring ABI and semantic authentication. Known denomination is `{ "asset": "FICTIONAL_UNIT", "decimals": "2" }`; unknown denomination is the literal `"unknown"`. Header references use chain plus hash, never height alone.
- `receipt_checks` versus `verification_checks`: matching a log against a receipt and observing transaction success are narrower than authenticating event meaning, verifying current canonicality, proving a refund or establishing complete history. Preserve individual check outcomes and sources, including mismatches and unavailable checks, rather than a blanket verified flag.
- `coverage`: requested, scanned, failed and unsearched inclusive block ranges, with chain/emitter/generation/filter scope and pagination or stopping evidence where useful. Generation discovery, index/log scope, receipt checks and canonical header checks are distinct. Counts are descriptive, not proof. Empty arrays mean no supplied range evidence, not complete coverage or zero events. A scanned range does not by itself prove uncapped, exhaustive discovery, and a final index page proves only the index's evidenced universe.
- `assumptions` and `results`: separate assumptions from source observations and derived outputs. Preserve formulas, exact values, units, source/input references and claim-specific limitations in the chosen extension fields.

The schema accepts extensions and partial/unknown observations. Required structural slots are a convention only for someone choosing this interchange; they do not require every question to discover a complete universe. JSON Schema validation checks shape, not source truth, cross-reference consistency, range arithmetic or economic semantics. Unknown or conflicting fields can prevent a particular aggregation while leaving other observations usable.

For a derived ledger, reconcile canonicality before deduplicating by chain/transaction hash/log index. Preserve raw duplicates, their sources, conflicts and reorg alternatives; do not silently pick the first conflicting row or erase evidence. Exclude removed/noncanonical observations from an asserted canonical total. Order retained executions by block, transaction and log position, not retrieval arrival. Keep chain, emitter, round and denomination groups separate, including generations that reuse round ids. An exact subtotal can be valid for a partial scope without being a full-history total.

A receipt-verified last sale becomes a historical **closing sale** only with complete ordered purchase coverage through the relevant endpoint and authenticated historical inventory exhaustion, including capacity changes and reopenings. Receipt matching cannot prove discovery omitted nothing; log coverage cannot independently establish refund flows; headers do not prove economic semantics. Preserve these separate outcomes rather than demanding universal completeness before sharing any useful result.
