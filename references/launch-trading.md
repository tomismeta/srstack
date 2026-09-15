# Launch trading, taxes and activation

Current publisher design: [v1 sources](../assets/sources/website-v1.json), `sr-whitepaper-v1` §§7,11–12,15 and companion pages. Exact settings: [launch parameters](../assets/parameters/launch.json), not observed execution.

## Pool launch and fees

For current pool initialization, epoch and tax settings, use a fresh fixed-reader snapshot with the publisher ABI. If the read is unavailable, report the requested state as unknown; application links are discovery routes, not packaged state evidence. [sr-protocol-conditions; sr-publisher-read-interface]

The published launch schedule opens at **90% buy / 90% sell**. The excess above the **2% buy / 3% sell** floors halves every **4 minutes**, reaching the floors **one hour** after trading starts. Canonical records: `launch-trading-tax`, `launch-trading-tax-curve`, `launch-tax-half-life`, `launch-tax-duration`. These are reference rules, not current rates. Current getters may differ from launch values or reflect an override; the fixed scenario engine uses an approved terminal tax assumption. [sr-whitepaper-v1: immutables, parameters; sr-publisher-read-interface]

The canonical pool's `canonical-pool-lp-fee` and `canonical-pool-tick-spacing` are separate published settings. The token page says protocol taxes apply on top of the LP fee; that description does not establish the deployed fee basis or computation order. [sr-whitepaper-v1: parameters; sr-token-page-v1]

## Activation boundary

Licenses remain dormant during founding distribution, then the owner activates them once with a published opening price and a fresh first day (`license-auction-activation`). Additional daily charter supply starts at `initial-daily-charter-count`. Design rules do not establish live activation or current configuration. [sr-whitepaper-v1: branches, auctions]

Read a fresh `auctions` snapshot when availability matters. A decaying price-function value after sellout is not a purchasable quote; use last-sale/closing price labels separately. No fresh status means availability is unknown. [sr-publisher-read-interface]

[Launch mint](launch-mint.md) covers founding terms; [reserves](reserves.md) separates founding proceeds, ongoing revenue, LP fees and protocol taxes. [Contracts](contracts.md) routes deployment evidence; [risks](risks.md) records remaining gaps.
