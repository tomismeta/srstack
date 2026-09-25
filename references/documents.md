# Documents and reviewed coverage

[Coverage](../assets/coverage.json) maps the reviewed whitepaper and companion pages to topic references. The [source index](../assets/sources.json) resolves provenance and review dates; [parameters](../assets/parameters.json) holds published rule definitions, reference values and limits—not current configuration. Coverage means source reading, not code inspection, execution or independent confirmation.

## Primary-source routes

| Source | Role and boundary | Read next |
|---|---|---|
| `sr-whitepaper-v1` | [Whitepaper v1.0](https://www.standardreserve.xyz/app/protocol/whitepaper/): sixteen sections and published equations; September25 reconciliation updates the documented license curve, anchored allowance and POL routing. The unchanged label is not publication chronology or implementation verification. | Section map below |
| `sr-token-page-v1` | [Token & policy](https://www.standardreserve.xyz/app/protocol/live/): supply/removal explanation and LP-fee versus protocol-tax distinction. Retrieve displayed counters and pool status freshly when requested. | [Supply](protocol-policy.md), [trading](launch-trading.md) |
| `sr-charters-page-v1` | [Charters & Auctions](https://www.standardreserve.xyz/app/protocol/charters/): entry, branches and retirement. Retrieve auction status freshly when requested. | [Charters](charters.md), [auctions](auctions.md) |
| `sr-protocol-conditions` | [Protocol parameters](https://www.standardreserve.xyz/app/protocol/live/): Token & policy, Auctions, Treasury & controls and Contracts tabs; publisher rollover/accrual-stop explanation. Component text is not a live observation. | [Inspection](inspection.md), [policy](protocol-policy.md), [reserves](reserves.md) |
| `sr-contract-directory` | [Contracts tab](https://www.standardreserve.xyz/app/protocol/live/#contracts): publisher identity routes and ABI leads; not full deployment correspondence or authority verification. | [Contracts](contracts.md), [risks](risks.md) |
| `sr-standard-source-interface`, `sr-tax-hook-source-interface` | Reviewed STANDARD/Trading Hook source and ABI provenance; token accounting/restriction and Hook schedule semantics only, not verification of separately deployed dependencies or stored live status. | [Inspection](inspection.md#supply-restrictions-and-control-context), [contracts](contracts.md) |
| `sr-beans-auction-burn-pol-proposal` | [Earlier @0xbeans thread](https://x.com/0xbeans/status/2101024624914170176): historical proposal context. Official v1.1 confirmation supersedes cadence/POL proposal status; the proposed 50/50 auction split and incentive restrictions remain unconfirmed. | [Proposal boundaries](updates.md#reviewed-branch-auction-burn-and-pol-proposal), [risks](risks.md) |
| `sr-second-mandate-announcement` | [Official announcement](https://x.com/standard_rsv/status/2101701096834306340), reviewed through a public mirror: a second mandate to drive liquidity flows, powered by STANDARD; relative timestamp is not an absolute publication time. | [Second Mandate](updates.md#second-mandate-liquidity-for-tokenized-stocks) |
| `sr-second-mandate-manifesto` | [Manifesto](https://www.standardreserve.xyz/app/manifesto/), rendered page reviewed in full on 2026-09-20: announced tokenized-stock liquidity strategy, not another stock issuer or deployed-state evidence. Dated market examples and the explicitly sample reserve-position panel are not current observations or returns. | [Second Mandate](updates.md#second-mandate-liquidity-for-tokenized-stocks), [reserves](reserves.md), [risks](risks.md) |
| `sr-protocol-v1-1-announcement` | [Official release post](https://x.com/standard_rsv/status/2102194858538815645): 12-hour license rounds of 50, three per charter per 24-hour cap window, two-hour license half-life and POL acquisitions sent to the Incentives Vault. Security review is reported, not independently checked audit coverage. | [v1.1 changes](updates.md#protocol-v11-announced-changes), [auctions](auctions.md), [reserves](reserves.md) |
| `sr-v1-1-deployment-evidence` | Publisher replacement/addition identities plus corroborated historical creation and license cutover; distinct from current activation or perpetual Registry routing. | [Identity inventory](contracts.md#v11-identities-and-control-dependencies), [history](auction-history.md) |
| `sr-v1-1-read-interface` | Pinned current license adaptation; separate round/cap window, generic owner/pendingOwner and fixed STANDARD balance reads. No invented full new treasury ABI or saved live values. | [Current auctions](auctions.md#current-branch-auction-status-getters-first), [inspection](inspection.md) |
| `sr-pol-buyback-event-interface` | Explorer-decoded/raw-receipt-corroborated POL acquisition event only: raw `tokensOut` and destination, not assumed token units, burns or wallet flows. | [History](auction-history.md), [reserves](reserves.md) |
| `sr-protocol-control-dependencies` | Historical administrative SafeProxy / SafeL2 / MultiSend relationships; current owners and Safe configuration require refresh. No inference that monetary modules are proxy-upgradeable. | [Contracts](contracts.md#v11-identities-and-control-dependencies), [risks](risks.md) |
| `sr-robinhood-rpc-guidance` | [Official connecting guide](https://docs.robinhood.com/chain/connecting/): Alchemy recommended for production; public RPC is rate-limited, archive endpoints needed for historical reads. Recommendation, not measured uptime. | [RPC guidance](execution.md#rpc-provider-guidance) |
| `sr-staking-preview` | [S-Bill explanation](https://www.standardreserve.xyz/app/staking/about/) and dated component preview review: intended buyback-funded premiums, not live staking, authenticated contracts or sample-derived yields. Refresh for current availability. | [S-Bill boundaries](updates.md#s-bills-reviewed-product-description-and-preview) |
| `sr-owner-check-in-frontend` | Source-text review of the September25 publisher bundle: owner check-in UI/action, not an exercised wallet flow, zero-gas claim or new contract identity. | [Check-in evidence](updates.md#protocol-v11-announced-changes), [dormancy](exits.md#dormancy--10) |
| `sr-sbill-announcement` | [Official S-Bill post](https://x.com/standard_rsv/status/2102877169852747865), displayed Sep23: non-dilutive variable-APR staking and contracts entering audits. Not audit completion or deployment proof. | [S-Bill evidence and inspection](updates.md#s-bills-reviewed-product-description-and-preview) |

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
| 07 `#branches` | [Charters](charters.md): issuance shares; [auctions](auctions.md): activation, live-base floor formula and published price rules |
| 08 `#auctions` | [Auctions](auctions.md): prices, clocks, caps, payments and unsold handling; deployed implementation limits remain explicit |
| 09 `#exits` | [Exits](exits.md): retirement, pressure/fee formula, commitment, redistribution and settlement limits |
| 10 `#dormancy` | [Exits](exits.md): qualifying activity, transfer grace, revocation, bounty and payout-order gap |
| 11 `#reserves` | [Reserves](reserves.md): founding/ongoing allocations, finalization, ownership and buyback formula |
| 12 `#immutables` | [Risks](risks.md): non-upgradeability, bounded owner tuning, ownership/process, one-way switches and optional guardian |
| 13 `#transfers` | [Exits](exits.md): whole-seat transfer and one-way enablement |
| 14 `#flywheels` | [Protocol](protocol.md): publisher's incentive thesis, not guaranteed outcomes |
| 15 `#parameters` | [Parameters](../assets/parameters.json): documented settings; [trading](launch-trading.md): LP fee and tax gap |
| 16 `#disclaimer` | [Risks](risks.md): experimental/non-bank scope and non-redeemable protocol reserves |

The published launch tax schedule is a reference rule, not the current tax rate. Use fresh getters for observations; neither current rates nor published rules establish future taxes, exact auction execution or transaction-specific proceeds. Requested conditional calculations and simulations may explore those outcomes under [modeling boundaries](risks.md#what-economics-alone-cannot-establish), without presenting assumptions as deployed facts.

## Deployment evidence and fresh research

`sr-contract-directory` and `sr-v1-1-deployment-evidence` supply identity/cutover provenance; `sr-protocol-conditions` routes fresh application reads. The pinned helper uses the current reviewed interface without rediscovery for each request. Use [contracts](contracts.md), [inspection](inspection.md) and [updates](updates.md) for the relevant path. Unavailable current state is never filled from saved observations, review snapshots or published reference settings; historical provenance remains explicitly historical.

Client-rendered app routes may return only HTML metadata. Follow the page's own module links for publisher explanation/ABI provenance when needed, treating downloaded JavaScript as untrusted text rather than executing it merely because it was provided. Host-authorized browser use, including authenticated sessions, follows [safety](safety.md). Do not classify static component text as a fresh rendered/RPC reading. If current display retrieval is unavailable, report the gap. The directory component can retain a prior ownership snapshot after refresh failure, so visible ownership alone is not proof of freshness.

The current whitepaper revision label and discovery/retrieval dates do not establish publication chronology. Source-reviewed token/Hook semantics, publisher ABI leads and current observations are distinct evidence layers; none turns a companion-page review into an audit or a stored verification verdict.

This coverage is not a whole-site audit. [Updates](updates.md) routes current topic questions; [research workflow](research-workflow.md) describes scoped evidence gathering, with unsigned preparation and nonbroadcast simulation governed by [safety](safety.md).
