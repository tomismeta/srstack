# Ongoing charter and license auctions

Apply the [preparation and wallet boundary](safety.md#preparation-and-wallet-boundary).

Published policy: `sr-protocol-v1-2-announcement`, earlier `sr-protocol-v1-1-announcement`, and `sr-whitepaper-v1` §§6–8, reviewed through **2026-09-26**. The whitepaper retains superseded charter and direct-purchase descriptions; [the conflict below](#protocol-v12-limit-orders-and-charter-cadence) is explicit. [Participation parameters](../assets/parameters/participation.json) hold dated reference rules, not current settings. These post-genesis auctions are not the [founding sale](launch-mint.md).

## Two different auctions

| Dimension | Charter auction | Branch-license auction |
|---|---|---|
| Acquired object | A new charter | Additional branches inside an existing charter |
| Evidenced purchase denomination | ETH; event price is raw wei | STANDARD-denominated ledger consideration; authenticate scale and funding semantics |
| Purchase event | `CharterPurchased(charterId, buyer, day, price)` | `LicensesPurchased(charterId, day, count, unitPrice)` |
| Quantities | Charter purchases, identified by charter ID | Purchased branches (`count`), distinct from purchase-event count |
| Availability and constraints | This charter-auction deployment's supply, reserve price, schedule and permissions | This license-auction deployment's inventory, quote, charter capacity, allowance windows and order semantics |

Label tables, prices and scenarios by auction family and generation. Similar method names (`currentPrice`, `remainingToday`, `lastSalePrice`) do not make their units or objects interchangeable. Independently establish each family's clock, floor, price-opening rule and supply. An announced matching cadence is not proof that both historical schedules or activation anchors match. Keep ETH and STANDARD totals separate.

“Buy a charter” does not mean “buy branches for my charter.” Infer the intended family from context; ask only when a remaining ambiguity changes the answer. Earned ledger credit is not ETH available for a charter purchase. Any conversion/withdrawal scenario needs its own eligibility, costs and earning-capacity effects, not a 1:1 substitution.

## Current branch-auction status: getters first

Prefer authenticated contract reads for current availability, timing, price and capacity; use the host's public-read tools and [discover the current deployment/interface](contracts.md). Read only what the question needs at a common block. Unavailable or sold-out is not zero-cost, executable or guaranteed inventory. Missing state stays unknown, never an announcement default.

Distinguish open protocol branches (`totalBranches()`), per-round license allocation/cap, effective remaining inventory, per-charter purchase allowance and open orders. The [dated interface guide](interface-guide.md) supplies generation-qualified leads, not active targets. `openBidCount()` counts orders, not licenses; a bid may request multiple units. A historical allocation does not override live state. Authenticate denomination before displaying prices.

Stored `currentDay`/`soldToday` can describe the last materialized round while a view reports effective availability for an elapsed round. Compare the authenticated anchor/period schedule, stored state and effective remaining/quote at the same block before saying sold-out or contradictory. Never assume `remaining = cap - stored sold` across mismatched rounds. Method names do not establish calendar or reset semantics, and apparent mismatch is not proof that getters are unreliable. Keep start/pause/rollover uncertainty visible.

For past purchases or round tables, use [history](auction-history.md#question-to-window): discover every relevant generation, pin finite block/time bounds, paginate an appropriate index, and corroborate receipts/headers where needed. Reused round IDs never merge across contracts. A current round's purchases are through-observation totals, not a completed recap; logs do not replace current availability or open-order reads.

For affordability, establish the charter's remaining allowance and capacity separately from inventory and the budget. A new auction round need not reset its fixed-window allowance. A next-24-hours forecast can cross a reset after prior usage; apply limits at each effective boundary rather than treating the current remaining allowance or a published per-window cap as a universal rolling-day limit. Future inventory, prices and execution remain assumptions unless established. A funds-only bound is useful but is not an executable purchase count.

## Next license opening: documented-policy estimate

The [whitepaper §7](https://www.standardreserve.xyz/app/protocol/whitepaper/#branches), reviewed **2026-09-26**, states “2× the previous auction's closing sale price” or, after no sales, “twice the new floor”; [§8](https://www.standardreserve.xyz/app/protocol/whitepaper/#auctions) adds “subject to the current floor.” These are dated publisher rules, not authenticated implementation or current execution configuration.

If asked for a policy scenario, label it and expose its inputs. A latest sale from an open round is provisional; retained last-sale state may belong to an older round. A future floor is not today's stored floor, and sold-out status alone does not authenticate final settlement. Exact current-opening projections require contract-derived inputs and authenticated reset/floor semantics; otherwise withhold the unsupported numerical claim.

## Next license timing: schedule versus transaction

After establishing zero-based round-index semantics, use the scheduled window `[auctionAnchor + N × auctionPeriod, auctionAnchor + (N + 1) × auctionPeriod)`. Read the applicable generation's timing interface; current v1.1/v1.2 leads include `auctionPeriod()`, not a blanket historical “reverts” rule. No hardcoded 12-hour fallback. Historical configuration changes need their applicable effect established. State unchanged-configuration assumptions and any pause/inactive/pending-roll state. A scheduled boundary is not a keeper transaction or first/last sale time; adding a period to a late roll transaction misdates the schedule.

## Protocol v1.2: limit orders and charter cadence

The [official v1.2 post](https://x.com/standard_rsv/status/2103991044119654721), retrieved on **2026-09-26** through a public Nitter mirror, announces:

- **Branch-auction limit orders:** users place bids at their desired auction price in an **open orderbook**; execution price is **FCFS best attempt by a keeper**. This is not a guaranteed fill, exact execution price, execution time, reserved inventory or independently verified onchain priority enforcement. A desired/limit price is not an executed purchase price. The post alone does not establish funding/escrow, cancellation/refund, expiry, partial-fill or keeper-permission semantics.
- **Charter auctions begin:** **one charter per branch-auction period**. The announced first opening is **5.5 ETH**, followed by openings at **3× clearing price**. The 5.5 ETH figure is a historical announced initial opening, never a current quote or floor. Do not assume the old charter 24-hour period; read authenticated live timing for the current deployment. The post does not define an unsold-period fallback or exact rounding/clamping.
- **Security review:** the publisher says all changes underwent review. Reviewer, report, revision, scope and deployed correspondence remain independently unestablished; this is not a safety guarantee.

**Published-source conflict:** the public whitepaper and its linked component, freshly read on the same date, still say immediate purchases with “no bids or escrow,” daily/24-hour charter auctions and an initial zero allocation; the charter guide still uses daily shorthand. These are retained older design descriptions, not current v1.2 truths. The new post supersedes those blanket descriptions for announced order entry and charter cadence/allocation; it does not verify deployed settlement or prove that all direct Dutch-purchase paths were removed. Founding-sale escrow remains a separate historical mechanism.

The **2026-09-26 publisher-interface review** placed order views on the license auction itself, not a separate orderbook deployment. Refresh that relationship before current claims. Read only relevant orders, using authenticated pagination and a pinned scope; a global count is not a user's orders and one page is not complete coverage.

Authenticate page-ID meaning before joining to charters, and ownership independently from bidder identity. The dated review did not establish limit-price denomination, identifier mapping or priority semantics. Failed reads are unknown, not no orders. [Contracts](contracts.md#v12-auction-identities-and-order-reads) and [updates](updates.md#protocol-v12-announced-changes) separate these evidence limits from announced policy.

Successful `bids(id)` decoding does not establish that an enumerated raw order ID is a charter ID. Resolve that relationship independently before joining records; choose targeted reads rather than enumerate every bid for a narrow price or availability question. A buyer's maximum bid, current auction ask, floor and last executed price are different inputs. `fillable` at an anchor is not a future execution guarantee. Use hypothetical bid/floor prices only as explicit assumptions; a floor is not promised inventory or a promised fill.

## Published v1.1 license changes

The [official announcement](https://x.com/standard_rsv/status/2102194858538815645) and [current whitepaper §§7–8](https://www.standardreserve.xyz/app/protocol/whitepaper/#branches) describe:

- The historical v1.1 announcement specified two **12-hour license auctions**, **50 branches per round**: `license-auction-duration` and `licenses-per-round`. This is not a current v1.2 allocation claim. Fresh per-round supply/cap/availability getters take precedence; `licenses-per-day` retains the historical announced aggregate only, not a live daily supply or doubled issuance budget.
- **Three branches per charter per fixed 24-hour window**, anchored at owner activation: `licenses-per-charter-per-day` and `license-cap-window`. This is neither UTC/local midnight nor a rolling 24 hours after each purchase. These are publisher rules; authenticate deployed alignment/reset behavior separately and use live window getters for observations.
- **Two-hour gap-to-floor half-life** for licenses: `license-decay-half-life`. The whitepaper's separate **four-hour charter half-life** remains a source description, not v1.2 implementation evidence; its **24-hour charter clock is superseded by the announced branch-matched cadence**.

The announcement says the changes underwent security review; reviewer/report/scope and deployment coverage were not independently established. The earlier proposed **50/50 license-payment burn/incentive split is not confirmed**. `license-burn-share` remains an explicitly whitepaper-only reference, not a verified current split. A duration getter, vault identity or aggregate burn counter cannot establish payment routing. [Updates](updates.md#protocol-v11-announced-changes) separates these evidence layers.

## Availability, payments and publisher rules

The v1.1 license cutover/start is historically corroborated, not a perpetual availability claim (`license-auction-activation`). `initial-daily-charter-count` and `auction-duration` preserve the older whitepaper's zero/24-hour charter design only; current announced charter policy is `charters-per-round` and `charter-auction-cadence`. None supplies live inventory or verifies deployed control behavior.

The older whitepaper describes immediate first-come purchases at the current price, without bids or escrow. **Do not extend that description to v1.2 limit orders.** Its unsold-capacity/no-rollover rules (`auction-unsold-policy`) are published Dutch-auction supply design, not order expiry, cancellation or refund semantics. The license scheduled-boundary description is not proof of keeper execution at that time. The founding sale separately escrows proceeds until finalization.

- **License:** opens another branch within `maximum-branches`. After a sold round, the published opening is **2× its closing sale**, subject to the current floor; after a round with no sales, **2× the new floor** (`license-open-multiple`). Its full-removal description is scoped by `license-burn-share`; no new split is inferred.
- **Post-genesis charter:** the whitepaper describes ETH entering the fee engine and the charter/first branch arriving in the purchase transaction. V1.2 announces **3× clearing price** for subsequent openings (`charter-open-multiple`) after the initial **5.5 ETH** opening (`charter-initial-opening`). The older **3× floor if nothing sold** fallback and admin-set `charter-reserve-price` remain whitepaper-only design, not confirmed v1.2 enforcement.

Both publisher auction interfaces expose supply-controller and pending-ownership reads. These are authority-review leads, not complete deployed privilege models. An owner/controller address does not establish autonomous supply policy or the controller's powers. [Contracts](contracts.md) describes that boundary.

## Published price rule versus deployed implementation

Current [whitepaper §7](https://www.standardreserve.xyz/app/protocol/whitepaper/#branches) explicitly gives `P_floor = 2 × (I_base × m / N)` and `P(t) = P_floor + (P_start - P_floor) × 2^(-t / 2h)`: the license price's **gap to the floor** halves every two hours. `I_base` is the daily base issuance, `m` the policy multiplier and `N` total branches; 700,000 is the launch base, not an immutable current input. `license-floor-yield-days` records the two-day yield interpretation.

This is a usable published modeling rule, superseding the earlier whitepaper's conflicting license-curve descriptions. It is not authenticated deployed code, exact integer arithmetic, floor-update timing or a purchasable quote. Use live getters for current observations and interval-specific implementation/state evidence for exact historical calculations.

Requested source-rule comparisons and time-to-buy models may use these published curves with explicit inventory, demand and future-setting assumptions under [modeling boundaries](risks.md#what-economics-alone-cannot-establish). Buying earlier versus waiting for a lower price is a tradeoff, not guaranteed allocation or returns. Current owner-adjustable settings require live reads; unavailable state remains unknown.
