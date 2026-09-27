# Auction and buyback history

Current availability is state; purchases and realized totals need execution evidence. Use host tools under [safety](safety.md#public-retrieval-and-calls), not fixed emitters or scan recipes. Bids, cancellations and reverted transactions are not purchases.

Choose and label the auction family explicitly. **Charter auctions** emit `CharterPurchased` with a per-charter ETH price; **branch-license auctions** emit `LicensesPurchased` with branch quantity and a STANDARD-denominated unit price. Authenticate the emitting generation and scales in the [interface guide](interface-guide.md). Keep family/chain/address/round identity and denominations separate; do not transfer a license schedule, price rule or allowance to charter history merely because getter names or round IDs match.

## Question to window

Resolve dates/timezone or rounds to a finite scope and pinned upper block/hash/time. Use indexed timestamps checked against boundary headers or bounded header search, never average block-time estimates. Ongoing intervals end at the anchor, labelled through-observation.

For an authenticated zero-based round index `N` and anchor/period schedule, the scheduled window is `[anchor + N × period, anchor + (N + 1) × period)`. The v1.1/v1.2 timing leads are `auctionAnchor()` and `auctionPeriod()`; `LicensesPurchased.day` is the emitted round identifier. Establish that relationship for the selected generation before applying it. Read the applicable period rather than hardcoding 12 hours. If configuration can change, establish its historical effect; today's period is not automatically valid for old rounds. Scheduled dating needs no header lookup for every sale; actual execution times and canonical verification still need relevant headers.

Full-history/cross-contract tables cover every dynamically discovered generation from creation through the anchor, not only current targets. Discover predecessors/successors through publisher history, registries/factories, creation and replacement records. Creation differs from activation/cutover; retain initialization and old-generation activity. Unresolved discovery is a gap, never permission to silently narrow scope.

For last N rounds, use evidenced chronology across requested generations, not reused numeric IDs; state whether an open round is included. Complete totals require the oldest selected round's beginning, not arbitrary lookback/early stopping. Never fabricate rows from equal endpoint state.

First-to-last purchase time is the observed selling span, not scheduled round duration or proof of a closing event. Concentrated early purchases are a dataset observation, never a safe universal scan cutoff. Overlapping predecessor/successor windows do not permit dropping either contract's activity.

## Retrieve a finite, auditable window

Use authenticated state when it establishes timing/configuration or narrows discovery. Equal endpoint counters do not prove inactivity without verified reset/monotonicity semantics.

For large histories, prefer suitable transaction/event indexes with finite filters and exhausted pagination over tiny-window RPC crawling. Retain coverage, filters, cursors and terminal-page evidence; detect truncation/gaps. Index exhaustion is not independent chain completeness.

Fetch relevant receipts once, decode applicable events and check canonical headers/timestamps. Keep chain/emitter/block hash/transaction hash/log index; deduplicate and exclude removed records. Authenticate historical event types/units. Reuse receipts/headers, batch calls and use bounded logs for gaps or when better suited. Choose collection limits appropriate to the question and actual provider constraints, not a fixed skill budget; disclose any stopping boundary. Recheck canonicality as needed; reorgs invalidate affected observations.

### Range-limited providers and degraded discovery

Read the first error before adapting. Range limits, unavailable archive state, unsupported methods, authentication refusal and empty results are different outcomes under [execution guidance](execution.md). Archive state is not an event index. Check the actual provider/chain/plan capabilities; an API key or paid plan alone proves none of them. Prefer supported batches over repeated receipt/header requests, with batch size chosen for actual limits.

When broad log retrieval is unavailable, an authorized explorer transaction list or transfer index can identify candidate transactions/blocks. Paginate the explicit interval, retrieve each relevant receipt once, filter by authenticated emitter and event topic, and decode the event layouts in the [interface guide](interface-guide.md). Small supported log windows around discovered blocks may help locate events; they do not turn the discovery list into an exhaustive event index.

External transfers or `to == auction` lists can omit internally invoked purchases, zero-value calls and other relevant paths. Explorer HTML pagination is fragile and may be capped. State what candidate universe was searched, terminal-page evidence, missing ranges and which receipt/event/header checks completed. Do not label this degraded path full history without independent evidence that discovery covers all relevant call paths. Never silently switch providers or evade a denied underlying action.

## Coverage and stopping

Separate generation discovery, index scope/page exhaustion, receipt verification and header/canonicality coverage. Receipts cannot prove an index omitted nothing. Identify checked, failed/unsearched intervals per emitter and missing boundaries. No matches means zero only in demonstrated scope; no coverage means unknown. A recent subset cannot satisfy a full-history request.

## Auction observations

Key rounds by chain, address and emitted identity; keep denominations separate. Show opening, first sale, quantity-weighted average, last sale and quantity as relevant, with gaps. Opening is not first-sale price; last observed is not final close. No purchases gives no average.

Use authenticated consideration and exact raw totals: average is `sum(consideration) / sum(quantity)`, not an average of round averages. Transaction value and maximum input may differ. Sellout/duration needs evidenced opening, effective historical capacity/changes, complete purchases and exhaustion endpoint, not today's cap or lazy-roll time. Zero-sale scheduled rows need authenticated schedule and no-sale coverage, not interpolation.

`lastSalePrice()` is stored contract state and a useful search/scenario input; it is not a receipt or proof of which purchase produced it. Authenticate the matching event and successful receipt before identifying a completed sale, buyer or purchase time. Report event unit price/consideration separately from transaction value, maximum payment and net cost. Excess transaction value does not prove a refund; net-paid claims require supported payment/refund evidence. Gas is a separate cost.

For aggregation, use the [calculation guidance](research-workflow.md#compute-with-explicit-units). Order executions by block, transaction and log position, not index arrival order. Deduplicate by chain/transaction hash/log index after canonical reconciliation; conflicting duplicates are evidence gaps, not an arbitrary first-row choice. Reconcile raw quantity and consideration totals per denomination; preserve exact weighted averages until display. These checks do not turn incomplete discovery into complete history.

Reconcile event totals against independently meaningful counters or supporting flows only when their scope and semantics match. A discrepancy remains explicit until explained: check interval endpoints, generations, multiple purchases per transaction, quantities versus event/transaction counts, canonical replacements and counter meaning. Do not force a residual into a missing sale or declare a getter broken. Failed transactions are attempts, not purchases.

### Buyback event accounting

Discover emitters and authenticate assets/scales. Separate spend, permanent burns, retained tokens and reported destinations. Events are not automatically reconciled transfers, all burns or holder income. Attribute with same-execution receipts without double-counting; unknown identity/decimals leaves amounts raw.
