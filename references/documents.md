# Documents and reviewed coverage

This directory maps the discovered public documentation to concise topic references. [Coverage](../assets/coverage.json) is the machine-readable page/section map; [source index](../assets/sources.json) resolves provenance groups. [Parameters](../assets/parameters.json) is the authoritative package location for economic values and explicit unknowns.

## Website discovery boundary

The reviewed [sitemap](https://www.standardreserve.xyz/sitemap.xml) lists the seven URLs below. All seven page presentations were reviewed in the September 14 snapshot; redirects and shared-content forms are not independent corroboration. Sitemap coverage is not a claim to have found every possible website URL, implementation document or social post. [sr-sitemap]

| Source | URL and role | Read next |
|---|---|---|
| `sr-protocol` | [Protocol Information](https://www.standardreserve.xyz/app/protocol/): navigation, launch banner, flow introduction and links to mint, whitepaper and About. Rendered counters are not economic configuration. | [Protocol](protocol.md) |
| `sr-mint` | [Mint](https://www.standardreserve.xyz/app/mint/): not-live presentation, whitelist liquidity fee, allocation/selection explanation, eligibility warning and public-genesis auction announcement. No address check or wallet action performed. | [Genesis entry](genesis.md) |
| `sr-whitepaper` | [Whitepaper](https://www.standardreserve.xyz/whitepaper/): v0.1 design overview, implementation warning, mechanics and still-redacted launch summary. | Section map below |
| `sr-about` | [How It Works](https://www.standardreserve.xyz/about/): standalone visual explanation of policy, charters, branches, retirement, fee response and feedback loops; examples are not live state. | [Protocol](protocol.md), [charters](charters.md), [reserves](reserves.md), [risks](risks.md) |
| `sr-app-about` | [App About](https://www.standardreserve.xyz/app/about/): same substantive explainer in the app navigation shell, not a distinct whitepaper or independent confirmation. | Same topics as standalone About |
| `sr-disclaimer` | [Disclaimer](https://www.standardreserve.xyz/disclaimer/): experimental/non-bank/no-customer-funds/no-advice statement, also present in whitepaper. About uses no-deposits wording. | [Risks](risks.md) |
| `sr-app-redirect` | [App root](https://www.standardreserve.xyz/app/): observed final URL is `/app/protocol/`, not an additional substantive document. | [Protocol](protocol.md) |

## Whitepaper section map

All section texts, visible equations and tables were reviewed, including redacted placeholders. “Reviewed” means the published material was read, not that hidden parameters were recovered or mechanics were tested.

| Section / source locator (`sr-whitepaper`) | Topic coverage |
|---|---|
| 01 `#introduction` | [Protocol](protocol.md): monetary-economy scope and publisher autonomy claim |
| 02 `#entities` | [Protocol](protocol.md): token, pool, central bank, charters, branches, vaults and flows |
| 03 `#currency` | [Supply and policy](protocol-policy.md): genesis versus withdrawal minting, cumulative budget, burns, supply identities; [reserves](reserves.md): LP ownership |
| 04 `#net-flow` | [Supply and policy](protocol-policy.md): current flow versus trailing policy signal |
| 05 `#policy` | [Supply and policy](protocol-policy.md): streamed issuance, asymmetric policy and hidden rule/settings |
| 06 `#charters` | [Genesis](genesis.md): revised entry and remaining public supply; [charters](charters.md): lifecycle; [reserves](reserves.md): proceeds distinction |
| 07 `#branches` | [Charters](charters.md): branch shares and paid expansion; [auctions](auctions.md): visible curve and hidden floor |
| 08 `#auctions` | [Auctions](auctions.md): separate daily license/charter opens, payment, decay, caps, close and rollover rules |
| 09 `#exits` | [Exits](exits.md): pro-rata retirement, minting, pressure, commitment fee and redistribution |
| 10 `#dormancy` | [Exits](exits.md): reporting, bounty, revocation, shutdown/check-in; [conflicts](risk-conflicts.md): unresolved payout ordering |
| 11 `#reserves` | [Reserves](reserves.md): ongoing ETH split, asset ownership, POL and tick-limited buyback equation |
| 12 `#transfers` | [Exits](exits.md): future one-way transfer switch and whole-seat movement |
| 13 `#flywheels` | [Protocol](protocol.md): publisher's adoption/expansion/fee/policy feedback-loop thesis |
| 14 `#parameters` | [Parameters](../assets/parameters.json): canonical visible and missing settings; [risks](risks.md): redacted summary versus earlier disclosures |
| 15 `#disclaimer` | [Risks](risks.md): experimental protocol and legal/financial scope disclaimer |

The document keeps the v0.1 label despite changed genesis wording. `sr-whitepaper-historical-free` records the superseded charter section observed earlier; it is not a second current whitepaper or a source for today's entry price. [History](announcement-history.md) preserves the change with dates and attribution.

## Announcements and linked identity discovery

Website navigation links [@standard_rsv](https://x.com/standard_rsv). The reviewed profile bio says no token or NFT set is live yet; that is time-bounded publisher wording, not independent deployment verification (`sr-x-profile`). Post-level statements, reply/image distinctions, audit announcements and publication/retrieval dates belong in [updates](updates.md) and its source records.

The launch thread adds genesis scheduling, temporary trading-tax terms, a schedule graphic distinguishing token launch without liquidity from later liquidity addition, and day-one auction/emission sequencing. These extend rather than replace the daily-auction design; their numerical settings are in [launch parameters](../assets/parameters/launch.json). [sr-post-2098969960404103353; sr-post-2098969968201359736; sr-post-2098969974044066298; sr-post-2098969982503915891]

No whitepaper label, canonical-site notice, source-code line-count claim, audit announcement or screenshot authenticates a deployed contract by itself. Use [contracts](contracts.md) for identity status and [research workflow](research-workflow.md) for fresh public evidence. This package does not treat linked scripts, frontend examples or unreviewed URLs as implementation specifications.

## Direct provenance routes

[Website core](../assets/sources/website-core.json): protocol, mint, whitepaper. [Website context](../assets/sources/website-context.json): About variants, disclaimer, app redirect, sitemap and profile. [Updates](updates.md) routes the complete recovered launch/policy threads, audit and allocation history, critical images and third-party context without requiring unrelated source groups.
