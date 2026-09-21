# Ongoing charter and license auctions

Publisher design: [v1 sources](../assets/sources/website-v1.json), `sr-whitepaper-v1` §§6–8,12. Exact settings: [participation parameters](../assets/parameters/participation.json). These daily post-genesis mechanics are not the [founding sale](launch-mint.md).

For “how did each auction go?”, historical quantities, paid prices or sellout timing, use [bounded auction-history research](auction-history.md), not the current auction snapshot or these design rules.

## Availability, payments and capacity

The published lifecycle keeps the license auction dormant until owner activation, then starts a fresh `auction-duration` first day. Additional charter supply starts at `initial-daily-charter-count` and remains policy-controlled (`charter-count-policy`). Use a fresh `auctions` snapshot for activation, configured duration and inventory; do not infer them from these reference rules or treat a price-function output as buyable inventory. If the read is unavailable, current availability is unknown. [sr-whitepaper-v1: branches, auctions; sr-publisher-read-interface]

For a requested time-to-buy model, use the observed auction duration or an explicitly assumed duration and price curve, labelled as such. Missing current availability prevents a live purchase claim, not conditional arithmetic.

When enabled, ongoing purchases execute immediately at the current price, first come first served, with no bids, escrow or refunds. Unsold daily capacity does not roll over; unpurchased charters are never minted. The **founding sale does escrow proceeds** until finalization, so §8's no-escrow description must not be generalized to it. [sr-whitepaper-v1: charters, auctions]

`license-auction-activation` and `auction-unsold-policy` preserve the lifecycle rules; `auction-owner-controls` records the bounded tuning authority. None establishes live activation or current auction configuration.

The publisher frontend ABIs additionally name `supplyController()`, `setSupplyController(address)`, `SupplyControllerSet` and `NotSupplyAuthority` for both auctions. This is an authority-review lead distinct from the whitepaper's owner description, not proof of deployed correspondence, a configured controller, its powers or autonomous supply policy. The bounded reader does not inspect that controller; do not infer complete count-setting authority from an owner getter. [sr-contract-directory: publisher-linked app ABI; contracts](contracts.md)

- **License:** payment permanently removes $STANDARD value (`license-burn-share`); daily supply is `licenses-per-day`, with `licenses-per-charter-per-day` and `maximum-branches` caps. The next opening price uses `license-open-multiple` times the last sold base price, or floor if no sale occurred. The license day ends on sellout or expiry.
- **Post-genesis charter:** ETH enters the ongoing fee engine. The charter and first branch arrive in the purchase transaction. `charter-open-multiple` applies to the previous closing sale, or floor if no sale occurred. Its floor is the admin-set `charter-reserve-price`, not the license's issuance-linked floor.

[Source: sr-whitepaper-v1: branches, auctions]

**Proposal boundary:** the [reviewed @0xbeans thread](updates.md#reviewed-branch-auction-burn-and-pol-proposal) proposes 12-hour branch auctions with half the daily allocation each, and a 50/50 immediate-burn/incentive-vault proceeds split. This qualifies the full-removal description above without changing `auction-duration`, `licenses-per-day` or `license-burn-share`: those remain whitepaper reference rules, not verified current settings. It does not halve the buyer's license cost, double daily issuance or establish a changed charter-auction cadence. A duration getter cannot authenticate proceeds routing or incentive-vault controls.

## Published floor and price-curve gap

§7 publishes `license-floor-formula`: P_floor = 2 × (700,000 × m / N), using the launch base, policy multiplier and total system branches. `license-floor-yield-days` captures its two-day yield interpretation. The source also permits later base-rate reductions; do not infer live floor recomputation, snapshot timing or rounding without implementation evidence. [sr-whitepaper-v1: branches equation 7.1; policy]

**Deployed auction price curve: Not established from current source; verified implementation required for deployment claims.** Requested source-rule calculations and curve comparisons may use explicitly selected assumptions, but are not executable purchase quotes. Do not substitute the founding-sale description. [sr-whitepaper-v1: branches, auctions]

The unresolved descriptions are specific: §7 equation 7.1 prints `P(t) = P_start × (P_floor / P_start)^(t / 24h)`, while the §7 table and §8 prose describe halving the **distance to the floor** every four hours, then settling at the floor. A fixed gap half-life instead has the form `P_floor + (P_start - P_floor) × 2^(-t / 4h)` before any clamp; these are different functions. Either may be calculated as a labeled source-rule scenario, including an explicit assumption for any clamp, or compared side by side; neither is established as the canonical deployed curve. Keep `license-decay-setting` null/not-established; neither description overrides fresh availability checks or supplies an execution quote.

The publisher's early-buy certainty versus wait-for-price tradeoff and illustrative `license-repricing-week-multiple` are explanations, not guaranteed allocation, returns or prices. Requested buy-now/wait comparisons may model those tradeoffs with explicit price, inventory and demand assumptions under [modeling boundaries](risks.md#what-economics-alone-cannot-establish). Owner-adjustable floors, windows and decay settings require fresh state for current claims; [risks](risks.md) describes that authority. Design text does not establish source-code/ABI correspondence.
