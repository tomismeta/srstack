# Launch trading, taxes and activation

Current publisher design: [v1 sources](../assets/sources/website-v1.json), `sr-whitepaper-v1` §§7,11–12,15 and companion pages. Exact settings: [launch parameters](../assets/parameters/launch.json), not observed execution.

## Pool launch and fees

Finalization is described as launching the pool, tax clock and epoch-one emissions in one atomic transaction. It places genesis tokens above an owner-set launch price and the founding ETH floor bid below it. This design sequence is not a receipt proving launch occurred. [sr-whitepaper-v1: reserves]

**Launch tax rates and executable curve: Not established from current source; verified implementation required.** `launch-trading-tax` and `launch-trading-tax-curve` remain unknown. Do not calculate a launch tax or infer duration, rounding or fee composition. Steady-state directional taxes are recorded separately in `trading-fee`. [sr-whitepaper-v1: immutables, parameters]

The canonical pool's `canonical-pool-lp-fee` and `canonical-pool-tick-spacing` are separate settings. The token page says protocol taxes apply on top of the LP fee; exact fee basis and computation order remain unverified. [sr-whitepaper-v1: parameters; sr-token-page-v1]

## Activation boundary

Licenses remain dormant during founding distribution, then the owner activates them once with a published opening price and a fresh first day (`license-auction-activation`). Additional daily charter supply starts at `initial-daily-charter-count`. Design rules do not establish live activation or current configuration. [sr-whitepaper-v1: branches, auctions]

The token page displayed **Not launched** for the pool, and the charter page displayed both auctions **Not enabled**, with block/time anchors in their source records. These are time-bounded UI observations, not independently authenticated chain state. [sr-token-page-v1; sr-charters-page-v1]

[Launch mint](launch-mint.md) covers founding terms; [reserves](reserves.md) separates founding proceeds, ongoing revenue, LP fees and protocol taxes. [Contracts](contracts.md) routes deployment evidence; [risks](risks.md) records remaining gaps.
