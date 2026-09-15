# Launch trading, taxes and activation

Current publisher design: [v1 sources](../assets/sources/website-v1.json), `sr-whitepaper-v1` §§7,11–12,15 and companion pages. Exact settings: [launch parameters](../assets/parameters/launch.json), not observed execution.

## Pool launch and fees

The protocol is live according to the official application and latest launch recap. The fixed snapshot helper can observe current pool initialization, epoch and tax settings using the publisher ABI. [sr-protocol-conditions; sr-latest-summary]

The current published launch schedule opens at **90% buy / 90% sell**. The excess above the **2% buy / 3% sell** floors halves every **4 minutes**, reaching the floors **one hour** after trading starts. Canonical records: `launch-trading-tax`, `launch-trading-tax-curve`, `launch-tax-half-life`, `launch-tax-duration`. Current getters may differ from launch values or reflect an override; the fixed scenario engine still uses an approved terminal tax assumption. [sr-whitepaper-v1: immutables, parameters; sr-publisher-read-interface]

The canonical pool's `canonical-pool-lp-fee` and `canonical-pool-tick-spacing` are separate settings. The token page says protocol taxes apply on top of the LP fee; exact fee basis and computation order remain unverified. [sr-whitepaper-v1: parameters; sr-token-page-v1]

## Activation boundary

Licenses remain dormant during founding distribution, then the owner activates them once with a published opening price and a fresh first day (`license-auction-activation`). Additional daily charter supply starts at `initial-daily-charter-count`. Design rules do not establish live activation or current configuration. [sr-whitepaper-v1: branches, auctions]

Current application observations show initialized trading, sold-out expansion licenses and daily charter sales not enabled. Read a fresh snapshot when availability matters. A decaying price-function value after sellout is not a purchasable quote; use last-sale/closing price labels separately. [sr-protocol-conditions; sr-publisher-read-interface]

[Launch mint](launch-mint.md) covers founding terms; [reserves](reserves.md) separates founding proceeds, ongoing revenue, LP fees and protocol taxes. [Contracts](contracts.md) routes deployment evidence; [risks](risks.md) records remaining gaps.
