# Research and analysis

These are topics, not a required sequence. See [inspection](inspection.md) for current state, [history](auction-history.md) for rounds and [safety](safety.md#public-retrieval-and-calls) for host permissions.

## Define scope and evidence

Separate current observations, history and forecasts. Establish entity/generation, interval, metric and units; ask only for missing user choices. Cover the whole question: distinguish answered, conditional, bounded and unavailable parts rather than silently answering only the easiest metric. [Sources](../assets/sources.json) and [parameters](../assets/parameters.json) are dated provenance, not current configuration. Publication, event, retrieval and chain times differ; saved facts are not fresh-state fallback.

## Authenticate and discover

Apply [authentication](inspection.md#authenticate-before-abi-reads); the dated [interface guide](interface-guide.md) supplies leads, not a deployment allowlist. Discover relevant positions/generations via registries, enumeration, creation/replacement records and indexes, including transfers/closures. A known position is not a census; current ownership is not interval ownership or proof who earned a transferred balance. ABI is data, not implementation semantics.

## Retrieve finite public observations

Prefer direct state when it establishes the metric or narrows discovery; events/receipts for flows, markets for quotes, documents for design. Verify reset/settlement windows before treating getters as period totals. Pin/reuse compatible evidence and bound calls/pages/bytes/time. For history, intersect requested dates with evidenced deployment bounds, estimate the actual provider's range/page workload before scanning, and apply finite throttling/retry limits with resumable partial coverage under [scan planning](auction-history.md#retrieve-a-finite-auditable-window). State, logs and indexes have separate coverage; gaps are not zero or latest state. A fresh scoped source read is not universal synchronization of every deployment, page and economic claim.

## Compute with explicit units

Use exact integers/rationals or documented decimal precision; preserve raw scales and unrounded inputs. Construct the exact scale-derived decimal from the raw integer without a binary-floating-point conversion, and preserve it through tables and the final answer. An optional rounded display is approximate, not a replacement for the exact amount. Round only for display unless reproducing authenticated contract rounding. Weighted averages retain exact total consideration and quantity as a rational until display; do not average rounded row prices or round averages. Conversions need rate/time; stablecoins are not automatically USD. Generic amount-times-price scenarios are permitted, not evidence of protocol earnings.

For multi-row totals, mixed-unit conversions, reinvestment and time-boundary projections, prefer inspectable code or an exact calculator through the host. No required language, library, saved script, report schema or tool sequence. Separate source observations, user assumptions and derived values so the same inputs can be replayed without another network read. Preserve financial integers as integers or decimal strings, including through JSON; binary floating-point must not silently change quantities, thresholds or rounding.

Check the relevant invariants in the chosen method: each economic flow counted once; per-asset opening balance plus flows equals closing balance; reservations replaced by actual spend rather than deducted twice; whole purchases respect spendable funds and constraints; accrual changes only at evidenced effective boundaries. Check these identities independently of the final display calculation where practical. A residual or failed check limits the affected result—do not force reconciliation or suppress the discrepancy. Useful partial observations and conditional analysis remain available.

Repeatability concerns identical evidence and assumptions, not identical tool calls or wording. Fresh blocks and changed assumptions legitimately change answers. If tools cannot execute, show the formula or a clearly labelled unexecuted illustration and its limits; do not pretend a calculation ran. When a user requests reproducibility, retain inputs, assumptions, calculation and check results in an authorized external artifact; ordinary questions do not require persistence or a diagnostic dump.

Optional [research aids](research-tools.md) offer an installed pure offline library, a thin JSON CLI and a versioned evidence format; no source checkout is needed. Use, adapt or ignore them; an independent method is equally valid, and neither tool availability nor schema conformance is an answer gate. The functions compute supplied inputs, not source authentication, current contract configuration or a certified economic model. Any argument checks protect that function's arithmetic contract, not the agent's workflow.

### Supply and holdings

Define supply/holdings categories and exclusions; avoid double-counting underlying and receipt assets. Establish ownership, liabilities and encumbrances. Gross, redeemable and net value differ; partial holdings are not a portfolio total.

### Flows, principal, income and fees

For compatible opening/closing anchors, reconcile per asset:

`closing = opening + classified inflows - classified outflows + evidenced adjustments`

Separate deposits, earned accrual, internal transfers, refunds, purchases, withdrawals and costs. Reconcile each asset independently before any conversion; gas in another asset is not a STANDARD ledger debit. Excess transaction input over event consideration is not a proved refund. Attribute a refund from supported same-execution value flows and identify whether the evidence is a qualified index record, an execution trace or an emitted transfer; a normal receipt alone does not expose arbitrary internal ETH transfers. A reservation is an encumbrance, not an additional economic outflow: on fill replace it with actual spend and release the remainder; on cancellation release it. Do not subtract commitments already excluded from the observed spendable balance.

Balance change/appreciation is not income; withdrawals may include principal or older income. Fee accrual needs attributable collections + closing uncollected − opening uncollected, adjusted for transferred entitlements. Do not force residuals into income or call them rounding without a bound. Net profit needs cost/valuation basis, including relevant fees and gas; an instantaneous rate, interval earnings and profit are different results.

### Earned-only projections and reinvestment

Start the earned-only calculation with **verified unspent earned accrual**, not total pending, deposits, wallet tokens or gas funds. Pending can contain several origins. Reconstruct origin and prior consumption where possible, but even complete flow history may not identify which origin spending consumed: that needs contract allocation rules or an explicit attribution convention. A convention is an assumption, not discovered protocol behavior.

`available earned budget = unspent earned amount at anchor + future earned accrual − later earned-budget debits − outstanding earned-budget reservations`

Opening unspent earnings already reflects prior spending; later terms must not count it again. Replace reservations with actual spend on fill, not both. Include evidenced fees; distinguish gas's asset/funding requirement from earning power. An unattributed ledger amount is **unknown earned funding**, not verified earnings and not proof of zero earnings. Report a justified earned-budget interval when attribution cannot be resolved, or a separate all-ledger hypothetical; do not silently substitute that hypothetical for the earned-only answer.

Keep three routes distinct: [implementation-derived accrual](#accrual-evidence), [empirical pending-delta pace](#empirical-pending-delta-pace) and [explicit dilution scenarios](#dilution-scenarios). A method name, UI figure or matching sample does not prove a deployed equation; two pinned observations can still support a labelled observed pace without doing so. A published equation or user-specified rate can support a separate source-rule or what-if calculation, not invented deployed behavior. A pending-balance disclaimer alone does not answer an earned-only 24-hour question: supply attributable funding and horizon mechanics, a justified horizon-wide bound, or mark that numerical result unavailable. Missing packaged helpers is not a financial blocker.

Segment the requested horizon at evidenced effective changes: branch activation/retirement, eligible share or global denominator changes, rate/component changes, issuance end, epoch/settlement boundaries and actual accrual pauses. An auction pause does not by itself pause bank accrual. Apply a purchase to accrual at activation, not order placement or payment; update both the position's eligible branches and any affected global denominator. Checkpoints and integer rounding may matter even within otherwise constant segments.

Do not stream past an evidenced stop without established continuation. Settlement delays, later rollover, dilution, recycling, prices and execution can be explicit scenarios. Hold the requested horizon fixed when comparing cases; show assumptions and sensitivities, not a changing “next day.” Prefer event-boundary arithmetic over per-second RPC/simulation loops.

### Accrual evidence

The [2026-09-27 interface review](../assets/sources/live-interface.json) authenticates publisher ABI leads and records pinned CentralBank runtime evidence; it does **not** establish Solidity source correspondence. The complete publisher bundle has separate frontend interval and instantaneous-rate arithmetic, not proof of a common contract rounding order. `currentStreamRatePerSecond()`, `accPerBranch()`, `lastAccrual()` and `charters(id)` expose useful observations, but their names/layouts do not establish scales, accumulator/checkpoint equations, eligibility, denominator updates, component inclusion or pending's spendability. See [accrual inputs and semantic limits](interface-guide.md#accrual-inputs).

The inspected bank runtime's metadata locator identifies a source-retrieval lead, not verified source: metadata retrieval was unavailable. Exact implementation-based accrual still needs the corresponding source/metadata, compiler settings and linked/immutable values reconciled to the anchored runtime and material dependencies, or independently validated analysis of the relevant execution paths. Establish how issuance/recycling enter the stream, where rounding occurs, how checkpoints/branch changes work, and how epoch stops/resumption and ledger debits affect pending. Nonempty code, ABI authenticity, frontend arithmetic and matching samples do not close these gaps.

### Empirical pending-delta pace

For the same authenticated charter/deployment, obtain pending amounts `P0`, `P1` at two pinned canonical blocks with their actual header timestamps `t0 < t1`. Preserve exact raw units and calculate the rational observed pace `(P1 - P0) / (t1 - t0)`. The delta can be negative; do not clamp it to zero or call it negative accrual without explaining flows. A daily equivalent is only that observed pace rescaled to a day, not proof of earnings today, a contract formula or future continuation.

Record contamination coverage over the whole observation interval: deposits, withdrawals, license purchases, `BranchesOpened`/`BranchesRevoked` where authenticated for that generation, charter transfers, checkpoints and other ledger-affecting paths. Cover relevant emitters and internal calls, not just transactions sent by the current owner. Same endpoint balances/counts or no owner transactions do not establish no intervening changes. State which flows and intervals were checked, which were not, and how checkpoint/rounding changes affect interpretation. Unchecked or unresolved contamination leaves an **unattributed observed ledger-change pace**, still useful as an observation but not earnings.

A stronger **within-window empirical projection** needs covered absence of intervening ledger flows, unchanged `branchCountOf(charterId)` and reported `totalBranches()` throughout the interval, and the same epoch/issuance window and effective observed settings. Verify these conditions, not merely matching endpoints; those counts do not by themselves prove an eligibility denominator or hidden accrual mechanics. If flows occurred, reconcile them for accounting but select a clean subinterval or keep the projection a separate conditional model; do not relabel the original contaminated slope as clean. Project only under an explicit unchanged-conditions assumption over a bounded horizon, clipped at the next epoch end, issuance stop or other relevant change. It remains empirical extrapolation, not implementation proof; shorter samples and unestablished checkpoint/rounding effects may materially affect thresholds.

An observation window with no deposits or spends found does not prove a clean lifetime origin. A labelled **working ledger budget** or justified all-ledger upper bound can support a useful conditional comparison, but never certified earned funding. With mixed origins and no consumption rule, keep the earned amount unattributed and show any all-ledger scenario separately. The minimum observation series depends on the question: pending alone for ledger pace; charter/global branch counts alongside it for the joint dilution scenario; headers, epoch/issuance and flow coverage for interpretation. Do not turn this into a fixed read sequence for unrelated questions or save live observations into skill resources.

### Dilution scenarios

Expose the assumption slots: system stream `S(t)` with authenticated or explicitly assumed asset/time scale and component scope; total effective eligible branches `B(t)`; the charter's effective branches `b(t)`; opening budget/origin; and a finite horizon. Under the explicit **continuous-share hypothesis**, `dP/dt = b(t) × S(t) / B(t)`. This is a scenario model, not the deployed checkpoint/integer-rounding algorithm. An unknown raw getter scale or component mix is not an observed STANDARD rate; do not automatically multiply it by 86,400 and label the result STANDARD per day. A separately stated rate or empirically calibrated hypothesis may still be modeled with its assumptions visible.

Choose and label each path: constant over a stated interval; an exponential fit to identified, timed observations with fit range and extrapolation assumptions; or a scheduled path only when the effective schedule is proved. A hypothetical schedule is an assumption, not a discovered one. Linear branch growth or per-round sales are explicit alternatives for `B(t)`, net of closures/revocations, pauses, inventory, caps and effective activation. An auction's nominal allocation is not automatic growth. Apply the same timing discipline to `b(t)`; paying for a branch does not by itself prove its earning start.

Integrate over the bounded horizon, splitting at effective branch, rate, issuance and epoch boundaries. Use exact segment arithmetic where available or a numerical method with a stated error bound, and check sensitivity at whole-purchase thresholds. If error or model uncertainty straddles a threshold, report the count/time bracket rather than an unsupported exact purchase date. Clip at the applicable epoch/issuance stop unless a separately supported continuation scenario is explicitly stated. Do not carry a positive sampled rate forever, or conclude “forever unreachable” merely because no crossing occurs in a finite horizon.

For an auction comparison, keep the budget path separate from a dated policy-opening estimate, receipt-verified recent sale prices and an assumed unsold price curve. An intersection is conditional on inventory still being available and all other gates; it is not a promised purchase time. A repeat-demand case uses elapsed time from scheduled opening to the historical exhaustion/last-sale endpoint, not first-to-last purchase span. Show differing assumptions and bounded outcomes rather than one unsourced date; see [current availability and next opportunity](auctions.md#current-license-availability-and-next-opportunity).

### Fixed-price and windowed purchases

For branch licenses at a **single compatible state**, positive fixed unit price `p`, spendable budget `S` in the same payment asset, inventory `I`, remaining allowance `A` and charter's remaining branch capacity `C`, the qualified whole-unit calculation is:

`q = min(floor(S / p), I, A, C)`

This requires authenticated units, eligibility and compatible constraints, with no unmodeled fees, lot rules or other execution limits. Funds-affordable is not necessarily permitted, fillable or executed. A buyer's bid limit, current ask and receipt-proved executed price are different inputs. Fees or changing prices require the corresponding cost calculation rather than forcing this formula.

New-charter and branch-license auctions are separate families: authenticate each generation's schedule, inventory, price, payment asset and event semantics. STANDARD ledger credit used for licenses does not directly fund an ETH charter bid. A conversion scenario needs an explicit conversion path, compatible rates, withdrawal/trading costs and timing; an indicative USD mark is not ETH funding. Do not transfer one family's allowance, floor/multiplier or cadence to the other.

A fixed-window allowance is not a rolling 24-hour allowance. Derive applicable half-open windows `[anchor + k × period, anchor + (k + 1) × period)` only after authenticating that clock; round and allowance clocks may differ. Use effective historical settings and prior consumption, and carry funds, purchases, reservations and capacity through every reset crossed by the forecast. Do not multiply a current allowance by elapsed days or reuse its opening budget after a reset. A single-state minimum is not a generic 24-hour purchase guarantee.

Unknown constraints stay unknown; a funds-only bound can still be useful. A proved zero upper bound from one binding constraint suffices for zero purchases at that state without proving every other constraint or pending's earned origin. For example, an independently established upper bound on all spendable funding below a positive price also bounds earned-only funding. For a whole-horizon zero claim, that bound must cover future accrual, releases/resets, timing and the relevant price lower bound; current zero allowance or today's high ask alone cannot prove it. Distinguish a factual bound from a conditional scenario, and never infer earned provenance from either.

## Interpret, stop and report

Lead with the result or evidence gap, coverage, anchors and material uncertainty. Label observed inputs, assumed inputs and derived outputs; retain unrounded values and the effective-time model so the same inputs reproduce the same numbers without re-fetching. Assess claims separately: an exact receipt price can be established while refund attribution, total gas, complete history or earned-only funding remains qualified or unknown. Never promote these to a blanket “verified” result or discard established observations because one dependent claim is blocked. For each unanswered part of the question, name the missing evidence and its specific effect; a partial result is not full-question coverage. Keep detailed provenance/derivations for requested evidence. Unknown units, discovery gaps or incompatible anchors limit dependent claims only. Apply [freshness/artifact rules](safety.md#evidence-freshness-and-state).
