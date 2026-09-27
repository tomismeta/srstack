# Research and analysis

These are topics, not a required sequence. See [inspection](inspection.md) for current state, [history](auction-history.md) for rounds and [safety](safety.md#public-retrieval-and-calls) for host permissions.

## Define scope and evidence

Separate current observations, history and forecasts. Establish entity/generation, interval, metric and units; ask only for missing user choices. [Sources](../assets/sources.json) and [parameters](../assets/parameters.json) are dated provenance, not current configuration. Publication, event, retrieval and chain times differ; saved facts are not fresh-state fallback.

## Authenticate and discover

Apply [authentication](inspection.md#authenticate-before-abi-reads). Discover relevant positions/generations via registries, enumeration, creation/replacement records and indexes, including transfers/closures. A known position is not a census; current ownership is not interval ownership. ABI is data, not implementation semantics.

## Retrieve finite public observations

Prefer direct state when it establishes the metric or narrows discovery; events/receipts for flows, markets for quotes, documents for design. Verify reset/settlement windows before treating getters as period totals. Pin/reuse compatible evidence and bound calls/pages/bytes/time. State, logs and indexes have separate coverage; gaps are not zero or latest state.

## Compute with explicit units

Use exact integers/rationals or documented decimal precision; preserve raw scales and unrounded inputs. Round for display unless reproducing contract rounding. Conversions need rate/time; stablecoins are not automatically USD. Generic amount-times-price scenarios are permitted, not evidence of protocol earnings.

For multi-row totals, mixed-unit conversions, reinvestment and time-boundary projections, prefer inspectable code or an exact calculator through the host. No required language, library, saved script, report schema or tool sequence. Separate source observations, user assumptions and derived values so the same inputs can be replayed without another network read. Preserve financial integers as integers or decimal strings, including through JSON; binary floating-point must not silently change quantities, thresholds or rounding.

Check the relevant invariants in the chosen method: each economic flow counted once; per-asset opening balance plus flows equals closing balance; reservations replaced by actual spend rather than deducted twice; whole purchases respect spendable funds and constraints; accrual changes only at evidenced effective boundaries. Check these identities independently of the final display calculation where practical. A residual or failed check limits the affected result—do not force reconciliation or suppress the discrepancy. Useful partial observations and conditional analysis remain available.

Repeatability concerns identical evidence and assumptions, not identical tool calls or wording. Fresh blocks and changed assumptions legitimately change answers. If tools cannot execute, show the formula or a clearly labelled unexecuted illustration and its limits; do not pretend a calculation ran. When a user requests reproducibility, retain inputs, assumptions, calculation and check results in an authorized external artifact; ordinary questions do not require persistence or a diagnostic dump.

### Supply and holdings

Define supply/holdings categories and exclusions; avoid double-counting underlying and receipt assets. Establish ownership, liabilities and encumbrances. Gross, redeemable and net value differ; partial holdings are not a portfolio total.

### Flows, principal, income and fees

For compatible opening/closing anchors, reconcile per asset:

`closing = opening + classified inflows - classified outflows + evidenced adjustments`

Separate deposits, accrual, internal transfers, purchases, withdrawals and costs. Balance change/appreciation is not income; withdrawals may include principal or older income. Fee accrual needs attributable collections + closing uncollected - opening uncollected, adjusted for transferred entitlements. Do not force residuals into income or call them rounding without a bound. Net profit needs cost/valuation basis.

### Earned-only projections and reinvestment

Start with **verified unspent earned accrual**, not total pending, deposits, wallet tokens or gas funds. Reconcile origin/prior spending; exclude unknown attribution:

`available earned budget = verified unspent earnings at anchor + projected future earned accrual - outstanding commitments - subsequent purchases/other earned-budget debits`

Count debits once: replace filled-order reservations with actual spend. Opening unspent earnings already reflects prior purchases. Include evidenced fees in spend; distinguish gas's asset/funding requirement from earning power.

Derive pace from the authenticated deployed calculation: units, accumulator/checkpoints, eligible shares/denominator, effective changes, rounding, pauses, epochs and settlement. Method names, UI daily figures or guessed stream-times-share formulas are insufficient. Never hardcode rates, recycling, multipliers, auction economics or fees. Unknown semantics leaves factual pace unavailable, not a ban on labelled what-ifs.

Apply purchases at effective accrual time, not order placement/payment. Respect verified eligibility, inventory, caps and settlement delays; new branches affect position share and applicable global denominator. Recompute affordability/accrual at event boundaries; do not credit branches before activation, reuse spent earnings or ignore outstanding commitments.

Stop at the evidenced epoch boundary unless continuation is independently established. Later rollover, rates, dilution, recycling, prices and execution require labelled scenarios. Show horizon, formulas, assumptions and sensitivities; separate gross accrual, spendable budget, net outcome and time-to-target. Prefer event-driven arithmetic over per-second RPC/simulation loops.

## Interpret, stop and report

Lead with the result or evidence gap, coverage, anchors and material uncertainty. Keep detailed provenance/derivations for requested evidence. Unknown units, discovery gaps or incompatible anchors limit dependent claims. Apply [freshness/artifact rules](safety.md#evidence-freshness-and-state).
