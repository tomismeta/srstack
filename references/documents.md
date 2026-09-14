# Documents and reviewed coverage

[Coverage](../assets/coverage.json) maps pages and sections to concise topic references; the [source index](../assets/sources.json) resolves provenance groups. [Parameters](../assets/parameters.json) is authoritative for exact settings, current conflicts, limits and prior observations.

## Dated website coverage

The earlier September 14 sitemap review covered seven page presentations. The current addition refreshes the whitepaper and two companion pages, **not every website surface**. Redirects and shared presentations are not independent corroboration; sitemap coverage is not an exhaustive URL or announcement archive. [sr-sitemap]

| Source | Role and boundary | Read next |
|---|---|---|
| `sr-whitepaper-v1` | [Current whitepaper](https://www.standardreserve.xyz/whitepaper/), captured 2026-09-14T22:15:13.789Z: sixteen sections, visible equations/tables and newly included Immutables. | Section map below |
| `sr-token-page-v1` | [Token](https://www.standardreserve.xyz/app/token/), captured 22:18:03.457Z: supply/removal explanation, LP-fee versus protocol-tax distinction and displayed not-launched pool. Block/time/counters remain UI evidence. | [Supply](protocol-policy.md), [trading](launch-trading.md) |
| `sr-charters-page-v1` | [Charters & Auctions](https://www.standardreserve.xyz/app/protocol/charters/), captured 22:18:03.462Z: entry/branch/retirement explanation; displayed disabled auctions. | [Charters](charters.md), [auctions](auctions.md) |
| `sr-protocol` | Earlier [Protocol Information](https://www.standardreserve.xyz/app/protocol/) navigation/banner/flow and links; rendered counters are not configuration. | [Protocol](protocol.md) |
| `sr-mint` | Earlier [Mint](https://www.standardreserve.xyz/app/mint/) not-live presentation, liquidity fee, selection and eligibility warning. No wallet/address check performed. | [Genesis](genesis.md) |
| `sr-whitepaper` | Earlier same-URL v0.1 snapshot: fifteen sections and redacted summary, preserved as dated evidence, **not current disclosure status**. | [History](announcement-history.md) |
| `sr-about`, `sr-app-about` | Earlier [standalone](https://www.standardreserve.xyz/about/) and [app](https://www.standardreserve.xyz/app/about/) explainers; same substantive content, different shell, examples not state. | [Protocol](protocol.md), [conflicts](risk-conflicts.md) |
| `sr-disclaimer` | Earlier [Disclaimer](https://www.standardreserve.xyz/disclaimer/), non-bank/no-customer-funds/no-advice scope. | [Risks](risks.md) |
| `sr-app-redirect` | Earlier [app root](https://www.standardreserve.xyz/app/) redirected to protocol page, not another substantive document. | [Protocol](protocol.md) |

## Current whitepaper: all sixteen sections

Frozen text and equation annotations were reviewed. Coverage means source reading, not code inspection, execution, independent fact confirmation or discovery of hidden content. All locators below belong to `sr-whitepaper-v1` and retain the source's anchors.

| Section / locator | Topic coverage |
|---|---|
| 01 `#introduction` | [Protocol](protocol.md): closed-economy model and publisher authority rhetoric |
| 02 `#entities` | [Protocol](protocol.md): six entities and trading/issuance/auction flows |
| 03 `#currency` | [Supply](protocol-policy.md): genesis liquidity, original issuance budget, withdrawal mints, permanent burns/ledger removals versus deposit conversions, revised supply identities |
| 04 `#net-flow` | [Policy](protocol-policy.md): current-epoch fee routing versus trailing-completed-epoch issuance signal |
| 05 `#policy` | [Policy](protocol-policy.md): unscaled launch base, downward owner ratchet, published multiplier rule/bounds, streaming and source-only timing illustrations |
| 06 `#charters` | [Genesis](genesis.md): paid entry, limits, escrow/finalization; [charters](charters.md): lifecycle |
| 07 `#branches` | [Charters](charters.md): issuance shares; [auctions](auctions.md): owner activation, floor formula and equation/prose decay conflict |
| 08 `#auctions` | [Auctions](auctions.md): license versus charter prices, caps, payments, unsold handling and contradictory decay descriptions |
| 09 `#exits` | [Exits](exits.md): retirement, published pressure/fee formula, commitment claim, redistribution and settlement-dependency limits |
| 10 `#dormancy` | [Exits](exits.md): qualifying activity, transfer timestamp/grace, report/revocation/bounty and unresolved payout order |
| 11 `#reserves` | [Reserves](reserves.md): founding versus ongoing allocation, atomic finalization, ownership and buyback formula |
| 12 `#immutables` | [Risks](risks.md): non-upgradeability, bounded owner tuning, deployer ownership/no enforced delay, one-way switches, optional guardian; [conflicts](risk-conflicts.md): tax contradiction |
| 13 `#transfers` | [Exits](exits.md): future whole-seat transfer and one-way enablement |
| 14 `#flywheels` | [Protocol](protocol.md): publisher's adoption/expansion/fee/policy thesis, not guaranteed outcomes |
| 15 `#parameters` | [Parameters](../assets/parameters.json): visible launch settings; [trading](launch-trading.md): tax contradiction, LP fee and holding cap |
| 16 `#disclaimer` | [Risks](risks.md): experimental/non-bank scope and non-redeemable protocol reserves |

The earlier `sr-whitepaper` and superseded `sr-whitepaper-historical-free` retain their observations. Source evolution is not package/software release history. The former's redactions must not be described as still present in current guidance. [Announcement history](announcement-history.md)

## Announcements and deployment additions

[Updates](updates.md) routes the earlier official profile, recovered launch/policy threads, audits, allocations and image-specific claims. Their stated dates and time-bounded not-live language are not silently refreshed. The launch thread adds schedule and tax claims; current paper contradictions and changes remain explicit rather than overwriting announcement history.

The separately reviewed `sr-contract-directory` and `sr-protocol-conditions` additions remain intact, with their entity index and source group accessible through [contracts](contracts.md). Those surfaces are publisher identity/condition evidence, not an authenticated source-code/ABI or deployed-bytecode audit. No whitepaper, line count, audit claim or screenshot closes that gap.

## Direct provenance routes

[Current website v1](../assets/sources/website-v1.json): current whitepaper/token/charter companions. [Website core](../assets/sources/website-core.json): earlier protocol/mint/whitepaper. [Website context](../assets/sources/website-context.json): About variants, disclaimer, redirect, sitemap and profile. [Updates](updates.md): announcement groups. [Research workflow](research-workflow.md): scoped fresh evidence without financial actions.
