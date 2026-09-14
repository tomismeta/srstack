# Post-mint trading, tax and activation

Sources: [launch trading](../assets/sources/launch-trading.json), `sr-post-2098969974044066298` and `sr-post-2098969982503915891`; exact settings: [launch parameters](../assets/parameters/launch.json). Part of the [launch mint thread](launch-mint.md), not observed deployment or execution.

- **Trading transition.** [Post Mint + Token Trading](https://x.com/standard_rsv/status/2098969974044066298) plans liquidity seeding and trading after genesis mint, an initial exponentially decaying anti-sniping tax, then ordinary protocol fees. It says fees feed the protocol and promises public addresses before launch. No address is supplied in the reviewed text/image. Canonical records: `launch-trading-tax`, `launch-trading-tax-duration`, `launch-trading-tax-half-life`, `launch-trading-tax-majority-decay-window` and `launch-trading-tax-curve`.
- **Text/image tension.** That trading post says the majority of the tax decays in the initial interval, while its image describes that interval as a half-life. Both claims are retained in the parameter records; neither a precise executable tax formula nor reconciliation against code was established. Do not choose one silently or use the graphic as a verified trading calculator.
- **Day-one activation.** [Day 1 Protocol Details](https://x.com/standard_rsv/status/2098969982503915891) says emissions for active Charters and STANDARD-paid, exponentially descending branch auctions start with trading. Additional charter auctions are not enabled then. Canonical records: `day-one-branch-auction-count` and `day-one-additional-charter-count`. This is distinct from the genesis public charter auction.

## Unspecified accounting

The trading post says fees feed the protocol, but does not specify the launch tax’s allocation split or fee basis. Neither genesis routing nor the regular ETH split settles those questions; see [reserves](reserves.md). [sr-post-2098969974044066298]
