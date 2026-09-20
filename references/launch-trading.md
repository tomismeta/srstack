# Launch trading, taxes and activation

Current publisher design: [v1 sources](../assets/sources/website-v1.json), `sr-whitepaper-v1` §§7,11–12,15 and companion pages. Exact settings: [launch parameters](../assets/parameters/launch.json), not observed execution.

## Pool launch and fees

For current pool initialization, epoch and tax settings, use a fresh fixed-reader snapshot with the publisher ABI. If the read is unavailable, report the requested state as unknown; application links are discovery routes, not packaged state evidence. [sr-protocol-conditions; sr-publisher-read-interface]

The published launch schedule opens at **90% buy / 90% sell**. The excess above the **2% buy / 3% sell** floors halves every **4 minutes**, reaching the floors **one hour** after trading starts. Canonical records: `launch-trading-tax`, `launch-trading-tax-curve`, `launch-tax-half-life`, `launch-tax-duration`. These are reference rules, not current rates. Current getters may differ from launch values or reflect an override; they establish neither future taxes nor transaction-specific sale proceeds. [sr-whitepaper-v1: immutables, parameters; sr-publisher-read-interface]

The canonical pool's `canonical-pool-lp-fee` and `canonical-pool-tick-spacing` are separate published settings. The token page says protocol taxes apply on top of the LP fee; that description does not establish the deployed fee basis or computation order. [sr-whitepaper-v1: parameters; sr-token-page-v1]

## Enabled versus active restrictions

Fresh `protocol`/`charter` observations distinguish `launch_holding_cap_enabled` from `launch_holding_cap_active`, and both from the Hook's `launch_schedule_active`. The reviewed token source requires cap enablement and an active schedule from its Registry-bound Hook; current tax rates alone do not answer either flag. `launch_holding_cap` is a STANDARD amount, not a transfer-success guarantee. The cap's from-PoolManager check, specified exemptions, separate `pool_manager_gate_enabled` setting and destination blocklist must not be collapsed into a single unrestricted/restricted label. The helper does not enumerate blocked addresses. [sr-standard-source-interface; sr-tax-hook-source-interface; inspection](inspection.md#supply-restrictions-and-control-context)

The reviewed Hook source gates non-POL liquidity additions while the launch schedule is active. Source-reviewed rules are not observed current availability or proof that a particular LP addition, withdrawal, router transfer or trade will settle. Token/Hook bindings and `hook_pending_owner` provide bounded control context, not complete permissions or a completed ownership transfer. No action workflow follows from these reads.

## Activation boundary

Licenses remain dormant during founding distribution, then the owner activates them once with a published opening price and a fresh first day (`license-auction-activation`). Additional daily charter supply starts at `initial-daily-charter-count`. Design rules do not establish live activation or current configuration. [sr-whitepaper-v1: branches, auctions]

Read a fresh `auctions` snapshot when availability matters. A decaying price-function value after sellout is not a purchasable quote. Summary omits last-sale/closing getters; full detail marks them `not_historical`, not round averages. Use [history](auction-history.md) for past purchases. No fresh status means availability is unknown. [sr-publisher-read-interface]

[Launch mint](launch-mint.md) covers founding terms; [reserves](reserves.md) separates founding proceeds, ongoing revenue, LP fees and protocol taxes. [Contracts](contracts.md) routes deployment evidence; [risks](risks.md) records remaining gaps.
