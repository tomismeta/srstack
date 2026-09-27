# Research and analysis

These are topics, not a required sequence. See [inspection](inspection.md) for current state, [history](auction-history.md) for rounds and [safety](safety.md#public-retrieval-and-calls) for host permissions.

## Define scope and evidence

Separate current observations, history and forecasts. Establish entity/generation, interval, metric and units; ask only for missing user choices. Cover the whole question: distinguish answered, conditional, bounded and unavailable parts rather than silently answering only the easiest metric. [Sources](../assets/sources.json) and [parameters](../assets/parameters.json) are dated provenance, not current configuration. Publication, event, retrieval and chain times differ; saved facts are not fresh-state fallback.

## Authenticate and discover

Apply [authentication](inspection.md#authenticate-before-abi-reads); the dated [interface guide](interface-guide.md) supplies leads, not a deployment allowlist. Discover relevant positions/generations via registries, enumeration, creation/replacement records and indexes, including transfers/closures. A known position is not a census; current ownership is not interval ownership or proof who earned a transferred balance. ABI is data, not implementation semantics.

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

Separate deposits, earned accrual, internal transfers, refunds, purchases, withdrawals and costs. Reconcile each asset independently before any conversion; gas in another asset is not a STANDARD ledger debit. A reservation is an encumbrance, not an additional economic outflow: on fill replace it with actual spend and release the remainder; on cancellation release it. Do not subtract commitments already excluded from the observed spendable balance.

Balance change/appreciation is not income; withdrawals may include principal or older income. Fee accrual needs attributable collections + closing uncollected − opening uncollected, adjusted for transferred entitlements. Do not force residuals into income or call them rounding without a bound. Net profit needs cost/valuation basis, including relevant fees and gas; an instantaneous rate, interval earnings and profit are different results.

### Earned-only projections and reinvestment

Start the earned-only calculation with **verified unspent earned accrual**, not total pending, deposits, wallet tokens or gas funds. Pending can contain several origins. Reconstruct origin and prior consumption where possible, but even complete flow history may not identify which origin spending consumed: that needs contract allocation rules or an explicit attribution convention. A convention is an assumption, not discovered protocol behavior.

`available earned budget = unspent earned amount at anchor + future earned accrual − later earned-budget debits − outstanding earned-budget reservations`

Opening unspent earnings already reflects prior spending; later terms must not count it again. Replace reservations with actual spend on fill, not both. Include evidenced fees; distinguish gas's asset/funding requirement from earning power. An unattributed ledger amount is **unknown earned funding**, not verified earnings and not proof of zero earnings. Report a justified earned-budget interval when attribution cannot be resolved, or a separate all-ledger hypothetical; do not silently substitute that hypothetical for the earned-only answer.

Derive factual pace from the [authenticated deployed calculation](#accrual-evidence), not a method name, UI daily figure or sample that fits a guessed formula. Unknown implementation or history limits that claim, not current state, source-rule models, explicit what-ifs or independently justified bounds. Missing packaged helpers is not a financial blocker; use the host's authorized tools.

Segment the requested horizon at evidenced effective changes: branch activation/retirement, eligible share or global denominator changes, rate/component changes, issuance end, epoch/settlement boundaries and actual accrual pauses. An auction pause does not by itself pause bank accrual. Apply a purchase to accrual at activation, not order placement or payment; update both the position's eligible branches and any affected global denominator. Checkpoints and integer rounding may matter even within otherwise constant segments.

Do not stream past an evidenced stop without established continuation. Settlement delays, later rollover, dilution, recycling, prices and execution can be explicit scenarios. Hold the requested horizon fixed when comparing cases; show assumptions and sensitivities, not a changing “next day.” Prefer event-boundary arithmetic over per-second RPC/simulation loops.

### Accrual evidence

The [2026-09-27 interface review](../assets/sources/live-interface.json) authenticates publisher ABI leads and records pinned CentralBank runtime evidence; it does **not** establish Solidity source correspondence. The complete publisher bundle has separate frontend interval and instantaneous-rate arithmetic, not proof of a common contract rounding order. `currentStreamRatePerSecond()`, `accPerBranch()`, `lastAccrual()` and `charters(id)` expose useful observations, but their names/layouts do not establish scales, accumulator/checkpoint equations, eligibility, denominator updates, component inclusion or pending's spendability. See [accrual inputs and semantic limits](interface-guide.md#accrual-inputs).

The inspected bank runtime's metadata locator identifies a source-retrieval lead, not verified source: metadata retrieval was unavailable. Exact implementation-based accrual still needs the corresponding source/metadata, compiler settings and linked/immutable values reconciled to the anchored runtime and material dependencies, or independently validated analysis of the relevant execution paths. Establish how issuance/recycling enter the stream, where rounding occurs, how checkpoints/branch changes work, and how epoch stops/resumption and ledger debits affect pending. Nonempty code, ABI authenticity, frontend arithmetic and matching samples do not close these gaps.

### Fixed-price and windowed purchases

For branch licenses at a **single compatible state**, positive fixed unit price `p`, spendable budget `S` in the same payment asset, inventory `I`, remaining allowance `A` and charter's remaining branch capacity `C`, the qualified whole-unit calculation is:

`q = min(floor(S / p), I, A, C)`

This requires authenticated units, eligibility and compatible constraints, with no unmodeled fees, lot rules or other execution limits. Funds-affordable is not necessarily permitted, fillable or executed. A buyer's bid limit, current ask and receipt-proved executed price are different inputs. Fees or changing prices require the corresponding cost calculation rather than forcing this formula.

New-charter and branch-license auctions are separate families: authenticate each generation's schedule, inventory, price, payment asset and event semantics. STANDARD ledger credit used for licenses does not directly fund an ETH charter bid. A conversion scenario needs an explicit conversion path, compatible rates, withdrawal/trading costs and timing; an indicative USD mark is not ETH funding. Do not transfer one family's allowance, floor/multiplier or cadence to the other.

A fixed-window allowance is not a rolling 24-hour allowance. Derive applicable half-open windows `[anchor + k × period, anchor + (k + 1) × period)` only after authenticating that clock; round and allowance clocks may differ. Use effective historical settings and prior consumption, and carry funds, purchases, reservations and capacity through every reset crossed by the forecast. Do not multiply a current allowance by elapsed days or reuse its opening budget after a reset. A single-state minimum is not a generic 24-hour purchase guarantee.

Unknown constraints stay unknown; a funds-only bound can still be useful. A proved zero upper bound from one binding constraint suffices for zero purchases at that state without proving every other constraint or pending's earned origin. For example, an independently established upper bound on all spendable funding below a positive price also bounds earned-only funding. For a whole-horizon zero claim, that bound must cover future accrual, releases/resets, timing and the relevant price lower bound; current zero allowance or today's high ask alone cannot prove it. Distinguish a factual bound from a conditional scenario, and never infer earned provenance from either.

## Interpret, stop and report

Lead with the result or evidence gap, coverage, anchors and material uncertainty. Label observed inputs, assumed inputs and derived outputs; retain unrounded values and the effective-time model so the same inputs reproduce the same numbers without re-fetching. For each unanswered part of the question, name the missing evidence and its specific effect; a partial result is not full-question coverage. Keep detailed provenance/derivations for requested evidence. Unknown units, discovery gaps or incompatible anchors limit dependent claims only. Apply [freshness/artifact rules](safety.md#evidence-freshness-and-state).
