# Launch trading, taxes and activation

Current publisher design: [v1 group](../assets/sources/website-v1.json), `sr-whitepaper-v1` §§7,11–12,15 and companion pages. Earlier [trading thread](../assets/sources/launch-trading.json) retains its own dates. Exact settings/conflicts: [launch parameters](../assets/parameters/launch.json), not observed execution.

## Current design and unresolved opening rates

Finalization is described as launching the pool, tax-decay clock and epoch-one emissions in one atomic transaction. It places genesis tokens above an owner-set launch price and the founding ETH floor bid below it. This is a design sequence, not a receipt proving launch occurred. [sr-whitepaper-v1: reserves]

**The current whitepaper contradicts itself:** §12's immutable schedule opens **90% buy / 90% sell**; §15 opens **20% buy / 40% sell** and describes linear decay. Both end at **2% buy / 3% sell**. `launch-trading-tax` and `launch-trading-tax-curve` therefore remain unresolved. Do not select one schedule, combine the rates or calculate an executable tax curve from them. Exact duration, rounding and implementation correspondence are separate evidence requirements. [sr-whitepaper-v1: immutables, parameters]

`launch-holding-cap` is a wallet holding cap for pool buys while launch fees decay; §15 says it lifts with that decay. It is not a founding-charter cap or a verified wallet balance limit. The canonical pool's `canonical-pool-lp-fee` and `canonical-pool-tick-spacing` are separate settings. The token page says protocol taxes apply on top of the LP fee; exact fee basis and computation order remain unverified. [sr-whitepaper-v1: parameters; sr-token-page-v1]

## Earlier announcement claims, not current reconciliation

[Post Mint + Token Trading](https://x.com/standard_rsv/status/2098969974044066298) announced post-mint liquidity/trading and an exponentially decaying anti-sniping tax before ordinary fees. Its body says the majority decays within the initial interval; its graphic instead calls that interval a half-life. Preserve `launch-trading-tax-duration`, `launch-trading-tax-half-life`, `launch-trading-tax-majority-decay-window` and the tax records' history as attributed announcement claims, not a verified calculator or resolution of the current §12/§15 conflict. The post says fees feed the protocol but leaves tax allocation and fee basis unspecified. [sr-post-2098969974044066298]

[Day 1 Protocol Details](https://x.com/standard_rsv/status/2098969982503915891) announced emissions and branch-license auctions with trading, with additional charter auctions disabled (`day-one-branch-auction-count`, `day-one-additional-charter-count`). Current §7 more specifically describes licenses as dormant during founding distribution, then activated once by the owner with a published opening price and fresh first day (`license-auction-activation`). Neither source establishes an activation transaction. [sr-whitepaper-v1: branches; sr-post-2098969982503915891]

The current token page displayed **Not launched** for the pool, and the charter page displayed both auctions **Not enabled**, with displayed block/time anchors preserved in source records. These are time-bounded UI observations, not independently authenticated chain state. Later directory/condition additions remain available in [contracts](contracts.md). [sr-token-page-v1; sr-charters-page-v1; sr-contract-directory; sr-protocol-conditions]

[Launch mint](launch-mint.md) preserves the earlier schedule; [reserves](reserves.md) separates founding proceeds, ongoing revenue, LP fees and protocol taxes.
