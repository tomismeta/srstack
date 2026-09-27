# Launch trading, taxes and activation

Apply the [preparation and wallet boundary](safety.md#preparation-and-wallet-boundary).

Publisher design reviewed through **2026-09-26**: [v1 sources](../assets/sources/website-v1.json), `sr-whitepaper-v1` §§7,11–12,15 and companion pages. Dated reference settings: [launch parameters](../assets/parameters/launch.json), not current configuration or observed execution.

## Pool launch and fees

Use host public-read tools and authenticated current deployments/interfaces for pool initialization, epoch or tax questions. Missing reads stay unknown; application links are discovery leads, not packaged state evidence. [Contracts](contracts.md) covers authentication.

The published launch schedule opens at **90% buy / 90% sell**. The excess above the **2% buy / 3% sell** floors halves every **4 minutes**, reaching the floors **one hour** after trading starts. Canonical records: `launch-trading-tax`, `launch-trading-tax-curve`, `launch-tax-half-life`, `launch-tax-duration`. These are reference rules, not current rates. Current getters may differ from launch values or reflect an override; they establish neither future taxes nor transaction-specific sale proceeds. [sr-whitepaper-v1: immutables, parameters; sr-publisher-read-interface]

The canonical pool's `canonical-pool-lp-fee` and `canonical-pool-tick-spacing` are separate published settings. The token page says protocol taxes apply on top of the LP fee; that description does not establish the deployed fee basis or computation order. [sr-whitepaper-v1: parameters; sr-token-page-v1]

Requested launch-tax curves, trade comparisons or liquidity scenarios may calculate these source rules under explicit assumptions about elapsed time, overrides, fee basis/order, prices and liquidity. Distinguish a source-rule estimate from a nonbroadcast implementation simulation and both from a settled transaction; see [modeling boundaries](risks.md#what-economics-alone-cannot-establish).

## Enabled versus active restrictions

Distinguish enabled holding limits from actually active restrictions and the Hook's launch schedule. The dated token/Hook source review tied restriction activation to related schedule state; taxes alone do not establish it. Authenticate deployment correspondence, units, pool-manager checks, exemptions and blocklist semantics before describing restrictions. Do not collapse them into one “unrestricted” flag. [Source provenance](../assets/sources/live-interface.json); [inspection](inspection.md#supply-restrictions-and-control-context).

The reviewed Hook source gated non-POL liquidity additions during its launch schedule. This is not current availability or a guarantee that liquidity changes or trades settle. Pending ownership is not accepted ownership, and related-address reads do not establish complete permissions.

## Activation boundary

The whitepaper's founding-distribution/one-time license activation sequence is historical design; the replacement v1.1 license cutover/start has separate provenance (`license-auction-activation`). Its `initial-daily-charter-count` zero allocation is an older design reference, **not current charter policy**: [v1.2](updates.md#protocol-v12-announced-changes) announces one charter per branch period, first opening at 5.5 ETH then 3× clearing price. These are announced rules, not live activation, current configuration or executable prices. Branch limit orders add a separately authenticated orderbook path; auction availability alone does not establish keeper fills.

Read authenticated current availability when it matters. A decaying price after sellout is not a purchasable quote, and retained last-sale state is not a round average. Use [history](auction-history.md) for past purchases; unavailable status remains unknown.

[Launch mint](launch-mint.md) covers founding terms; [reserves](reserves.md) separates founding proceeds, ongoing revenue, LP fees and protocol taxes. [Contracts](contracts.md) routes deployment evidence; [risks](risks.md) records remaining gaps.
