# Ongoing charter and license auctions

Publisher design: [v1 sources](../assets/sources/website-v1.json), `sr-whitepaper-v1` §§6–8,12. Exact settings: [participation parameters](../assets/parameters/participation.json). These daily post-genesis mechanics are not the [founding sale](launch-mint.md).

## Availability, payments and capacity

The license auction stays dormant through founding distribution. The current owner activates it once with a published opening price and a fresh `auction-duration` first day. Additional charter supply starts at `initial-daily-charter-count` and remains policy-controlled (`charter-count-policy`). The current companion page displayed both auctions as not enabled; this is dated presentation, not an independently verified permission/state read. [sr-whitepaper-v1: branches, auctions; sr-charters-page-v1]

When enabled, ongoing purchases execute immediately at the current price, first come first served, with no bids, escrow or refunds. Unsold daily capacity does not roll over; unpurchased charters are never minted. The **founding sale does escrow proceeds** until finalization, so §8's no-escrow description must not be generalized to it. [sr-whitepaper-v1: charters, auctions]

`license-auction-activation` and `auction-unsold-policy` preserve the lifecycle rules; `auction-owner-controls` records the bounded tuning authority. None establishes live activation or current auction configuration.

- **License:** payment permanently removes $STANDARD value (`license-burn-share`); daily supply is `licenses-per-day`, with `licenses-per-charter-per-day` and `maximum-branches` caps. The next opening price uses `license-open-multiple` times the last sold base price, or floor if no sale occurred. The license day ends on sellout or expiry.
- **Post-genesis charter:** ETH enters the ongoing fee engine. The charter and first branch arrive in the purchase transaction. `charter-open-multiple` applies to the previous closing sale, or floor if no sale occurred. Its floor is the admin-set `charter-reserve-price`, not the license's issuance-linked floor.

[Source: sr-whitepaper-v1: branches, auctions]

## Published floor and unresolved decay conflict

§7 now publishes `license-floor-formula`: P_floor = 2 × (700,000 × m / N), using the launch base, policy multiplier and total system branches. `license-floor-yield-days` captures its two-day yield interpretation. The source also permits later base-rate reductions; do not infer live floor recomputation, snapshot timing or rounding without implementation evidence. [sr-whitepaper-v1: branches equation 7.1; policy]

**The same source gives incompatible price paths.** Equation 7.1 is geometric interpolation to the floor over a full day:

P(t) = P_start × (P_floor / P_start)^(t / 24h).

But §§7–8 prose says the **gap to the floor halves every four hours**, then settles at the floor for the rest of the day (`license-decay-setting`). The equation and that prose do not generally describe the same curve. The prose does not establish the exact floor-settlement cutoff either. Preserve both as source claims; **do not select, execute, endorse or use either as a purchase quote**. Founding-auction prose is a separate description and resolves neither. [sr-whitepaper-v1: branches equation 7.1; auctions Decay]

The publisher's early-buy certainty versus wait-for-price tradeoff and illustrative `license-repricing-week-multiple` are explanations, not guaranteed allocation, returns or prices. Owner-adjustable floors, windows and half-lives add a state dependency; [risks](risks.md) describes that authority. Source-code/ABI correspondence remains unverified. See [conflicts](risk-conflicts.md).
