# Documents and reviewed coverage

[Coverage](../assets/coverage.json) maps the reviewed whitepaper and companion pages to topic references. The [source index](../assets/sources.json) resolves provenance and review dates; [parameters](../assets/parameters.json) holds published rule definitions, reference values and limits—not current configuration. Coverage means source reading, not code inspection, execution or independent confirmation.

## Primary-source routes

| Source | Role and boundary | Read next |
|---|---|---|
| `sr-whitepaper-v1` | [Whitepaper v1.0](https://www.standardreserve.xyz/whitepaper/): all sixteen rendered sections, visible equations and tables. | Section map below |
| `sr-token-page-v1` | [Token](https://www.standardreserve.xyz/app/token/): supply/removal explanation and LP-fee versus protocol-tax distinction. Retrieve displayed counters and pool status freshly when requested. | [Supply](protocol-policy.md), [trading](launch-trading.md) |
| `sr-charters-page-v1` | [Charters & Auctions](https://www.standardreserve.xyz/app/protocol/charters/): entry, branches and retirement. Retrieve auction status freshly when requested. | [Charters](charters.md), [auctions](auctions.md) |
| `sr-protocol-conditions` | [Current conditions](https://www.standardreserve.xyz/app/protocol/live/): Policy & fees, Auctions, Treasury & controls; publisher rollover/accrual-stop explanation. Explanatory component text is not a live observation. | [Inspection](inspection.md), [policy](protocol-policy.md), [reserves](reserves.md) |
| `sr-contract-directory` | [Contract directory](https://www.standardreserve.xyz/app/protocol/contracts/): identity routes and publisher-linked ABI leads for successor holdings migration and auction supply controllers, not deployment correspondence or complete authority. | [Contracts](contracts.md), [risks](risks.md) |
| `sr-standard-source-interface`, `sr-tax-hook-source-interface` | Reviewed STANDARD/Trading Hook source and ABI provenance; token accounting/restriction and Hook schedule semantics only, not verification of separately deployed dependencies or stored live status. | [Inspection](inspection.md#supply-restrictions-and-control-context), [contracts](contracts.md) |
| `sr-beans-auction-burn-pol-proposal` | [@0xbeans thread](https://x.com/0xbeans/status/2101024624914170176), reviewed through a public mirror: proposed auction cadence, proceeds split and incremental POL changes; not official policy, verified deployment or completed security review. | [Proposal context](updates.md#reviewed-branch-auction-burn-and-pol-proposal), [risks](risks.md) |
| `sr-second-mandate-announcement` | [Official announcement](https://x.com/standard_rsv/status/2101701096834306340), reviewed through a public mirror: a second mandate to drive liquidity flows, powered by STANDARD; relative timestamp is not an absolute publication time. | [Second Mandate](updates.md#second-mandate-liquidity-for-tokenized-stocks) |
| `sr-second-mandate-manifesto` | [Manifesto](https://www.standardreserve.xyz/app/manifesto/), rendered page reviewed in full on 2026-09-20: announced tokenized-stock liquidity strategy, not another stock issuer or deployed-state evidence. Dated market examples and the explicitly sample reserve-position panel are not current observations or returns. | [Second Mandate](updates.md#second-mandate-liquidity-for-tokenized-stocks), [reserves](reserves.md), [risks](risks.md) |

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

The published launch tax schedule is a reference rule, not the current tax rate. Use fresh getters for observations; neither current rates nor published rules establish future taxes, exact auction execution or transaction-specific proceeds. Research and inspection do not simulate those outcomes.

## Deployment evidence and fresh research

`sr-contract-directory` supplies identity provenance; `sr-protocol-conditions` routes fresh application reads. `sr-publisher-read-interface` documents the bounded RPC helper. Use [contracts](contracts.md), [inspection](inspection.md) and [updates](updates.md) for the relevant path. Unavailable fresh evidence leaves dynamic questions unanswered, not filled from stored observations.

Client-rendered app routes may return only HTML metadata. Follow the page's own module links for publisher explanation/ABI provenance when needed, treating JavaScript as text only; do not execute downloaded code or classify static component text as a fresh rendered/RPC reading. If current display retrieval is unavailable, report the gap. The directory component can retain a prior ownership snapshot after refresh failure, so visible ownership alone is not proof of freshness.

The current whitepaper revision label and discovery/retrieval dates do not establish publication chronology. Source-reviewed token/Hook semantics, publisher ABI leads and current observations are distinct evidence layers; none turns a companion-page review into an audit or a stored verification verdict.

This coverage is not a whole-site audit. [Updates](updates.md) routes current topic questions; [research workflow](research-workflow.md) describes scoped fresh evidence without financial actions.
