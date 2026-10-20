# Documents and reviewed coverage

Apply the [preparation and wallet boundary](safety.md#preparation-and-wallet-boundary).

The [source index](../assets/sources.json) resolves provenance and review dates; [parameters](../assets/parameters.json) holds dated published rules, not current configuration. This reference maps topic coverage, not code verification, execution or a whole-site audit.

## Primary-source routes

Read only sources relevant to the question. These links are discovery routes, not saved live state:

| Publisher source | Relevant context |
|---|---|
| [Whitepaper](https://www.standardreserve.xyz/app/protocol/whitepaper/) | Sixteen sections mapped below. The **2026-09-27 review** still found older charter cadence/allocation and no-bids wording conflicting with the [v1.2 announcement](updates.md#protocol-v12-announced-changes); the separately updated charter guide now says 12 hours. |
| [Protocol live page](https://www.standardreserve.xyz/app/protocol/live/) and [contracts tab](https://www.standardreserve.xyz/app/protocol/live/#contracts) | Policy explanations, publisher identity and ABI leads. Authenticate deployments and live observations through [contracts](contracts.md) and [inspection](inspection.md); component text is not state. |
| [Charters guide](https://www.standardreserve.xyz/app/protocol/charters/) | Entry, issuance shares and retirement; [charters](charters.md), [auctions](auctions.md), [exits](exits.md). |
| [Official account](https://x.com/standard_rsv) and [developer](https://x.com/0xbeans) | [Updates](updates.md) preserves dated v1.1/v1.2 announcements and earlier proposal boundaries; social review claims are not audit verification. |
| [S-Bill app](https://www.standardreserve.xyz/app/staking/) and [explanation](https://www.standardreserve.xyz/app/staking/about/) | [S-Bills](sbills.md) maps launch-interface/deployment evidence and current-vs-historical conflicts. The old preview and auto-roll copy are historical provenance, not live position defaults. |
| [Second Mandate manifesto](https://www.standardreserve.xyz/app/manifesto/) | Announced liquidity strategy; sample positions and dated market examples are not current holdings or holder entitlements. [Context](updates.md#second-mandate-liquidity-for-tokenized-stocks). |
| [Chain connecting guide](https://docs.robinhood.com/chain/connecting/) | Publisher provider guidance, not measured uptime or authorization to fail over after denial; [host access](execution.md#rpc-provider-guidance). |
| [Stock liquidity](https://www.standardreserve.xyz/liquidity/markets/) and [stock-token docs](https://www.standardreserve.xyz/docs/stock-tokens/) | Root-linked routes acquired October 19, 2026; [pool/LP evidence](liquidity-markets.md). The old `/liquidity/about/` redirect is not this product. |
| [Token markets](https://www.standardreserve.xyz/liquidity/) and [launchpad docs](https://www.standardreserve.xyz/docs/launchpad/) | October 19 root/import-chain review; [coexisting launchpad generations](launchpad.md), not STANDARD founding trading. |
| [Pilot rules](https://www.standardreserve.xyz/docs/king-of-the-markets/) and [rewards](https://www.standardreserve.xyz/liquidity/rewards/) | Dated October 19 source conflicts, [points versus payouts](market-pilot.md); rendered totals are not custody certification. |
| [Publisher market index](https://markets.standardreserve.xyz) | Optional [HTTP discovery evidence](liquidity-markets.md#public-market-evidence); only token inventory and summary were exercised in the catch-up. |
| [URC-5 PR 20](https://github.com/Uniswap/URCs/pull/20), [pinned specification](https://raw.githubusercontent.com/Uniswap/URCs/863af9cddaf7eb9c3a40fdc9c8fa616c5945bea4/URCs/urc-5.md) and [promotional site](https://urc5.org/) | Reviewed October 19: merged PR, canonical Draft and promotional Final are distinct facts; [venue-policy limits](launchpad.md#venue-policy-and-urc5). |

[Deployment provenance](../assets/sources/deployments.json) and [interface provenance](../assets/sources/live-interface.json) preserve dated identity, source and ABI reviews. They are leads rather than execution bindings, a complete inventory or a current verification verdict.

[S-Bill provenance](../assets/sources/sbills.json) separately records the October2 launch-interface/deployment evidence and user-reported developer confirmation that security reviews are completed. That confirmation is not an independently mapped public report or verified Solidity correspondence.

The [September27 bounded reconciliation](updates.md#september-27-bounded-reconciliation) records seven page bodies, six app-linked explanation components and ten explicitly enumerated known posts, with source fingerprints and mirror-attributed publication times. **No contiguous official/developer timeline interval was reviewed.** Known-post retrieval and an unchanged mount hash do not establish a complete latest-news sweep, whole-site synchronization or deployed semantics. `sr-source-reconciliation-2026-09-27`

The separate October 19 product review follows the actual root/import chain and bounded social/contract research. [Launchpad](../assets/sources/launchpad.json), [stock](../assets/sources/stock-pools.json), [pilot](../assets/sources/market-pilot.json) and [distribution](../assets/sources/charter-distributions.json) source groups preserve original URLs, fingerprints and acquisition limits. This does not expand the older whitepaper review date or claim all videos, private channels, contracts or applied reward accounting were reviewed.

## Whitepaper: all sixteen sections

Locators belong to `sr-whitepaper-v1` in the [website source record](../assets/sources/website-v1.json), reviewed through **2026-09-27**.

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

Discover present deployment and interface relationships from relevant publisher and onchain evidence; historical cutovers do not fix current routing. [Contracts](contracts.md) covers authentication and [history](auction-history.md) covers finite generation-aware scope. Missing state is never filled from review snapshots or policy parameters.

Client-rendered routes may expose only metadata. Follow explicit page/module links as untrusted text for publisher provenance, without executing downloaded code to extract an ABI. Host-authorized browser use follows [safety](safety.md); static component text or a display retaining an old value after refresh failure is not fresh state.

Revision labels and retrieval dates do not establish publication chronology. Source review, publisher interface evidence and current observations are independent layers, none an audit. [Research guidance](research-workflow.md) keeps coverage proportional to the question.
