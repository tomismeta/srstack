# Documents and reviewed coverage

[Coverage](../assets/coverage.json) maps the current whitepaper and companion pages to topic references. The [source index](../assets/sources.json) resolves provenance and retrieval dates; [parameters](../assets/parameters.json) holds exact settings and limits. Coverage means source reading, not code inspection, execution or independent confirmation.

## Current primary sources

| Source | Role and boundary | Read next |
|---|---|---|
| `sr-whitepaper-v1` | [Whitepaper v1.0](https://www.standardreserve.xyz/whitepaper/): all sixteen rendered sections, visible equations and tables. | Section map below |
| `sr-token-page-v1` | [Token](https://www.standardreserve.xyz/app/token/): supply/removal explanation, LP-fee versus protocol-tax distinction and displayed pool status. Counters and status remain source-dated UI observations. | [Supply](protocol-policy.md), [trading](launch-trading.md) |
| `sr-charters-page-v1` | [Charters & Auctions](https://www.standardreserve.xyz/app/protocol/charters/): entry, branches, retirement and displayed auction status. | [Charters](charters.md), [auctions](auctions.md) |

## Whitepaper: all sixteen sections

All locators below belong to `sr-whitepaper-v1` in [current website sources](../assets/sources/website-v1.json).

| Section / locator | Topic coverage |
|---|---|
| 01 `#introduction` | [Protocol](protocol.md): system model and ownership |
| 02 `#entities` | [Protocol](protocol.md): entities and trading/issuance/auction flows |
| 03 `#currency` | [Supply](protocol-policy.md): genesis liquidity, issuance budget, withdrawal mints, permanent removals, deposit conversions and supply identities |
| 04 `#net-flow` | [Policy](protocol-policy.md): current-epoch fee routing versus trailing-completed-epoch issuance signal |
| 05 `#policy` | [Policy](protocol-policy.md): launch base, owner ratchet, multiplier rule/bounds, streaming and source-only timing illustrations |
| 06 `#charters` | [Genesis](genesis.md): paid entry, limits, escrow/finalization; [charters](charters.md): lifecycle |
| 07 `#branches` | [Charters](charters.md): issuance shares; [auctions](auctions.md): activation, floor formula and price-curve gap |
| 08 `#auctions` | [Auctions](auctions.md): prices, caps, payments, unsold handling and price-curve gap |
| 09 `#exits` | [Exits](exits.md): retirement, pressure/fee formula, commitment, redistribution and settlement limits |
| 10 `#dormancy` | [Exits](exits.md): qualifying activity, transfer grace, revocation, bounty and payout-order gap |
| 11 `#reserves` | [Reserves](reserves.md): founding/ongoing allocations, finalization, ownership and buyback formula |
| 12 `#immutables` | [Risks](risks.md): non-upgradeability, bounded owner tuning, ownership/process, one-way switches and optional guardian |
| 13 `#transfers` | [Exits](exits.md): whole-seat transfer and one-way enablement |
| 14 `#flywheels` | [Protocol](protocol.md): publisher's incentive thesis, not guaranteed outcomes |
| 15 `#parameters` | [Parameters](../assets/parameters.json): documented settings; [trading](launch-trading.md): LP fee and tax gap |
| 16 `#disclaimer` | [Risks](risks.md): experimental/non-bank scope and non-redeemable protocol reserves |

Launch tax rates/curve and ongoing auction price curve: **Not established from current source; verified implementation required.** No alternative schedule or executable quote is inferred.

## Deployment evidence and fresh research

`sr-contract-directory` and `sr-protocol-conditions` are routed through [contracts](contracts.md), the [entity index](../assets/entity-index.json) and [deployment sources](../assets/sources/deployments.json). Publisher identity and condition evidence does not establish source-code/ABI or deployed-bytecode correspondence. Explorer observations retain their own scope in those records.

This coverage is not a whole-site audit. [Updates](updates.md) routes current topic questions; [research workflow](research-workflow.md) describes scoped fresh evidence without financial actions.
