# Ongoing charter and license auctions

Current identity/interface: `sr-v1-1-deployment-evidence` and `sr-v1-1-read-interface`. Published v1.1 changes: `sr-protocol-v1-1-announcement`; current publisher design: `sr-whitepaper-v1` §§6–8,12. Exact reference values and scopes live in [participation parameters](../assets/parameters/participation.json); none is a saved live setting. These post-genesis auctions are not the [founding sale](launch-mint.md).

## Current branch-auction status: getters first

Use `scripts/snapshot.py auctions` directly for current availability, round timing, price and capacity. It uses the packaged v1.1 license address and publisher-authenticated read interface at one block: **no address rediscovery, reindexing or history scanning is needed**. Read errors and availability alongside price; an unavailable or sold-out auction is not a zero-cost or executable purchase quote. If fresh reads fail, current state is unavailable, not a stored snapshot or announcement default.

Default answer: **getter-reported status; available licenses; current price in STANDARD if returned; elapsed round / rollover context; observation time**. Use the matching `charter_auction_*` fields and ETH denomination when the question is about charters. Keep owners, controller addresses and full diagnostics out unless relevant. No price-helper quote, wallet connection or history call is needed for either current-status answer.

The license generation uses `auctionPeriod()`; the charter auction retains its separate `AUCTION_DAY()`. For licenses, `capWindow()`, `capWindowIndex()` and `MAX_PER_CHARTER_PER_WINDOW()` separate the charter allowance from the auction round. A new 12-hour round does not imply a fresh three-license allowance. The publisher also authenticates `purchasedInWindow(charterId,window)` and `remainingForCharter(charterId)`, but these charter-specific methods are **supplemental ABI scope**, not bundled auction calls or a new auction charter-ID input; use bounded [supplemental reads](inspection.md#supplemental-public-reads) when that allowance is requested.

**Lazy rollover matters:** interpret `currentDay()`, `soldToday()` and `remainingToday()` with stored-versus-elapsed round context, not as human-calendar-day sales. Compare the live anchor, observed period and pinned block timestamp with the stored round. Availability getters may already account for the elapsed round while stored counters still describe an earlier round; do not combine them into “X sold / Y remaining today.” Report the helper's availability basis and pending-rollover context. `licensesPerDay()` is a retained method name for **per-round** supply on this generation, not a daily aggregate. Full-detail last-sale/closing diagnostics are marked `not_historical` and cannot establish past paid prices or sellout.

**Getter decoding boundary:** the helper gives `started()` and `paused()` precedence, then maps `remainingToday() == 0` to `sold_out`, otherwise `open`. Its `basis: contract_availability_getters` is not independent inventory reconciliation, charter eligibility or a transaction-success guarantee. `aligned` only means the stored index matches the anchor/period calculation; unknown or inconsistent round context must accompany the reported availability.

**Not established:** exact deployed storage/derived behavior, rollover arithmetic and an invariant linking `soldToday()`, `remainingToday()` and cap getters. Do not replace remaining inventory with `cap − sold`, infer sellout from a documented cap, or assume either getter is stale. Apparent disagreement needs same-block, same-generation evidence and authenticated semantics before an accounting cross-check; retain the observations and name the uncertainty meanwhile.

For “this round's purchases,” “last round” or a date-window performance question, use the [short history recipes](auction-history.md#question-to-window): resolve generation/round and evidenced block bounds, then request quantities, event-accounted consideration and weighted prices. License history preserves both legacy and v1.1 addresses; reused round IDs must not merge. A current round's purchases are a through-observation total, not a completed auction recap. Historical logs never replace the getter path above for current availability.

## Published v1.1 license changes

The [official announcement](https://x.com/standard_rsv/status/2102194858538815645) and [current whitepaper §§7–8](https://www.standardreserve.xyz/app/protocol/whitepaper/#branches) describe:

- Two **12-hour license auctions**, **50 branches per round**: `license-auction-duration` and `licenses-per-round`. `licenses-per-day` is the announced aggregate of two allocations, not a current getter result or doubled issuance budget.
- **Three branches per charter per fixed 24-hour window**, anchored at owner activation: `licenses-per-charter-per-day` and `license-cap-window`. This is neither UTC/local midnight nor a rolling 24 hours after each purchase. These are publisher rules; authenticate deployed alignment/reset behavior separately and use live window getters for observations.
- **Two-hour gap-to-floor half-life** for licenses: `license-decay-half-life`. Charters retain their own **24-hour clock and four-hour half-life**; neither description authenticates deployed arithmetic or rounding.

The announcement says the changes underwent security review; reviewer/report/scope and deployment coverage were not independently established. The earlier proposed **50/50 license-payment burn/incentive split is not confirmed**. `license-burn-share` remains an explicitly whitepaper-only reference, not a verified current split. A duration getter, vault identity or aggregate burn counter cannot establish payment routing. [Updates](updates.md#protocol-v11-announced-changes) separates these evidence layers.

## Availability, payments and publisher rules

The v1.1 license cutover/start is historically corroborated, not a perpetual availability claim (`license-auction-activation`). Additional charter supply starts at the whitepaper `initial-daily-charter-count` and remains policy-controlled (`charter-count-policy`). `auction-duration` now refers only to the whitepaper's post-genesis **charter** schedule; it is not an alternative current license duration.

The whitepaper describes immediate first-come purchases at the current price, without bids or escrow; unsold capacity does not roll over and unpurchased charters are not minted (`auction-unsold-policy`). The next license round begins at its scheduled boundary even if the prior round sold out early. The founding sale does escrow proceeds until finalization, so this description must not be generalized to it. These source rules do not independently establish every deployed settlement path.

- **License:** opens another branch within `maximum-branches`. After a sold round, the published opening is **2× its closing sale**, subject to the current floor; after a round with no sales, **2× the new floor** (`license-open-multiple`). Its full-removal description is scoped by `license-burn-share`; no new split is inferred.
- **Post-genesis charter:** ETH enters the ongoing fee engine; the charter and first branch arrive in the purchase transaction. The published opening is **3× the previous closing sale**, or **3× the floor** if nothing sold (`charter-open-multiple`). The floor is the admin-set `charter-reserve-price`, not the license's issuance-linked floor.

Both publisher auction interfaces expose supply-controller and pending-ownership reads. These are authority-review leads, not complete deployed privilege models. An owner/controller address does not establish autonomous supply policy or the controller's powers. [Contracts](contracts.md) describes that boundary.

## Published price rule versus deployed implementation

Current [whitepaper §7](https://www.standardreserve.xyz/app/protocol/whitepaper/#branches) explicitly gives `P_floor = 2 × (I_base × m / N)` and `P(t) = P_floor + (P_start - P_floor) × 2^(-t / 2h)`: the license price's **gap to the floor** halves every two hours. `I_base` is the daily base issuance, `m` the policy multiplier and `N` total branches; 700,000 is the launch base, not an immutable current input. `license-floor-yield-days` records the two-day yield interpretation.

This is a usable published modeling rule, superseding the earlier whitepaper's conflicting license-curve descriptions. It is not authenticated deployed code, exact integer arithmetic, floor-update timing or a purchasable quote. Use live getters for current observations and interval-specific implementation/state evidence for exact historical calculations.

Requested source-rule comparisons and time-to-buy models may use these published curves with explicit inventory, demand and future-setting assumptions under [modeling boundaries](risks.md#what-economics-alone-cannot-establish). Buying earlier versus waiting for a lower price is a tradeoff, not guaranteed allocation or returns. Current owner-adjustable settings require live reads; unavailable state remains unknown.
