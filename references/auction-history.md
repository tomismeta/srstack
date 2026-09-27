# Auction and buyback history

Current availability is state; purchases and realized totals need execution evidence. Use host tools under [safety](safety.md#public-retrieval-and-calls), not fixed emitters or scan recipes. Bids, cancellations and reverted transactions are not purchases.

## Question to window

Resolve dates/timezone or rounds to a finite scope and pinned upper block/hash/time. Use indexed timestamps checked against boundary headers or bounded header search, never average block-time estimates. Ongoing intervals end at the anchor, labelled through-observation.

Full-history/cross-contract tables cover every dynamically discovered generation from creation through the anchor, not only current targets. Discover predecessors/successors through publisher history, registries/factories, creation and replacement records. Creation differs from activation/cutover; retain initialization and old-generation activity. Unresolved discovery is a gap, never permission to silently narrow scope.

For last N rounds, use evidenced chronology across requested generations, not reused numeric IDs; state whether an open round is included. Complete totals require the oldest selected round's beginning, not arbitrary lookback/early stopping. Never fabricate rows from equal endpoint state.

## Retrieve a finite, auditable window

Use authenticated state when it establishes timing/configuration or narrows discovery. Equal endpoint counters do not prove inactivity without verified reset/monotonicity semantics.

For large histories, prefer suitable transaction/event indexes with finite filters and exhausted pagination over tiny-window RPC crawling. Retain coverage, filters, cursors and terminal-page evidence; detect truncation/gaps. Index exhaustion is not independent chain completeness.

Fetch relevant receipts once, decode applicable events and check canonical headers/timestamps. Keep chain/emitter/block hash/transaction hash/log index; deduplicate and exclude removed records. Authenticate historical event types/units. Reuse receipts/headers, batch calls and use bounded logs for gaps or when better suited. Choose collection limits appropriate to the question and actual provider constraints, not a fixed skill budget; disclose any stopping boundary. Recheck canonicality as needed; reorgs invalidate affected observations.

## Coverage and stopping

Separate generation discovery, index scope/page exhaustion, receipt verification and header/canonicality coverage. Receipts cannot prove an index omitted nothing. Identify checked, failed/unsearched intervals per emitter and missing boundaries. No matches means zero only in demonstrated scope; no coverage means unknown. A recent subset cannot satisfy a full-history request.

## Auction observations

Key rounds by chain, address and emitted identity; keep denominations separate. Show opening, first sale, quantity-weighted average, last sale and quantity as relevant, with gaps. Opening is not first-sale price; last observed is not final close. No purchases gives no average.

Use authenticated consideration and exact raw totals: average is `sum(consideration) / sum(quantity)`, not an average of round averages. Transaction value and maximum input may differ. Sellout/duration needs evidenced opening, effective historical capacity/changes, complete purchases and exhaustion endpoint, not today's cap or lazy-roll time. Zero-sale scheduled rows need authenticated schedule and no-sale coverage, not interpolation.

For aggregation, use the [calculation guidance](research-workflow.md#compute-with-explicit-units). Order executions by block, transaction and log position, not index arrival order. Deduplicate by chain/transaction hash/log index after canonical reconciliation; conflicting duplicates are evidence gaps, not an arbitrary first-row choice. Reconcile raw quantity and consideration totals per denomination; preserve exact weighted averages until display. These checks do not turn incomplete discovery into complete history.

### Buyback event accounting

Discover emitters and authenticate assets/scales. Separate spend, permanent burns, retained tokens and reported destinations. Events are not automatically reconciled transfers, all burns or holder income. Attribute with same-execution receipts without double-counting; unknown identity/decimals leaves amounts raw.
