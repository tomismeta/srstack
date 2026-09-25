# Contracts and identity

Identity research, not an execution guide. The [entity index](../assets/entity-index.json) defines packaged attribution scope, not this filename.

## Packaged boundary

The packaged [Robinhood inventory](../assets/entities/robinhood.json) contains **20 identities** on **Robinhood Chain, chain ID 4663**: **16 current publisher-directory entries** (14 protocol modules and two shared infrastructure entries), the historical legacy license auction, and three administrative/shared dependencies. Only the 16 are current directory entries; 17 identities have publisher attribution including the legacy generation, and three have observed-relationship provenance. Records contain roles and explorer links, not saved live owners, balances or activation status. [Deployment sources](../assets/sources/deployments.json) preserve the distinct attribution layers.

The fixed [read interface](../assets/interfaces/robinhood-reads.json), documented by `sr-publisher-read-interface` and `sr-v1-1-read-interface`, pins read-only metadata and target bindings. `snapshot.py auctions` already uses the current v1.1 license target; current status does not require rediscovery, reindexing or log scanning. It checks fresh state and code at its anchor, not independently reproduced source/bytecode correspondence. Legacy license identity is retained for historical generation authentication only.

Default all generated address, transaction and block explorer links to **[Robinhood Etherscan](https://robin.etherscan.io/)**: `/address/ADDRESS`, `/tx/HASH` and `/block/NUMBER`; contract-source links may append `#code`. Use each catalog entry's explorer link for source/ABI publication checks. Preserve an alternate provider's actual evidence URL when citing that source, without changing the default explorer. Match chain plus full address; Ethereum `etherscan.io` is chain 1. A similar-match label alone does not authenticate this deployment's semantics. An unavailable lookup stays unavailable, not a saved verification verdict.

The directory also lists a pool manager and Multicall as shared infrastructure. Neither is project-authored merely because listed; a pool manager is not a unique canonical-pool address. Do not import Arbitrum or local-test records from the frontend bundle into this Robinhood group.

For public observations, use [inspection](inspection.md), including its [units and financial interpretation](inspection.md#units-and-financial-interpretation). An address alone supplies neither ABI semantics, economic defaults, gas estimates nor authorization for financial actions.

## v1.1 identities and control dependencies

| Canonical catalog ID | Address | Scope |
|---|---|---|
| `sr-robinhood-license-auction-v1-1` | `0x44731EFf9da8fDD30003AA7C0B324368B3DfFE5e` | Current publisher license target |
| `sr-robinhood-license-auction` | `0xA45CE49303EEd5846F841BFd4bAC6aE8C805EC05` | Legacy historical generation, not current snapshot target |
| `sr-robinhood-pol-buyback` | `0x50e4C444f71dF2Db8593c6c8ba4d493De618E147` | Publisher POL Buyback, retained acquisitions |
| `sr-robinhood-incentives-vault` | `0x9481404d30C296e57C93f05A49934A901719bbA9` | Publisher Incentives Vault, not a burn sink |
| `sr-robinhood-admin-safe` | `0x5c19F925E1e0D54E34681A6CB70d55c90b12A68c` | Historical ownership/cutover SafeProxy dependency |
| `sr-robinhood-safe-implementation` | `0x29fcB43b46531BcA003ddC8FCB67FFE91900C762` | SafeL2 implementation relationship requiring refresh |
| `sr-robinhood-safe-multisend` | `0x9641d764fc13c8B624c04430C7356C1C7C8102e2` | Historical Safe batch-execution dependency |

The original `sr-robinhood-pol-manager` / `0x242F3e67BEf43470C2434d95E7D618E19f87c8f8` remains publisher-listed as **Genesis Liquidity Manager**, for custody and fee collection of genesis liquidity positions. The frontend `polManager` name is not a live Registry binding: the historical `POL_MANAGER` registry event routes to the new buyback. Refresh the registry relationship for present routing claims; historical asset movement does not prove migration of every LP position.

`sr-v1-1-deployment-evidence` separates publisher mapping from corroborated creation and cutover. The replacement license was created at block 69178086; license registry cutover/start occurred at block 69222157, timestamp 1790036371. These historical anchors support generation-aware research, not stored live availability. The public bundle's pinned commit and reported security review do not establish independent audit coverage or source/bytecode equivalence.

`sr-protocol-control-dependencies` identifies research targets, not perpetual ownership. Read module owners/pending owners freshly and independently check Safe implementation, signers, threshold, modules and guards before current-control claims. The **administrative SafeProxy does not prove the monetary modules themselves proxy-upgradeable**. Historical owner acceptance is not complete authority evidence, and an owner is not necessarily an auction supply controller.

Direct new-module source retrieval was unavailable in the reviewed paths; alternate explorer records provided bytecode without complete Solidity/ABI. This is a scoped source-access limit, not proof that no explorer verification or audit exists. Exact license window math, payment split and new treasury-module permissions remain unverified.

## Authenticate the requested role

1. Find original official website/account deployment evidence identifying the role, chain and environment—not a quoted third party or infrastructure component. Retain URL, author and publication/retrieval times.
2. Establish chain authority and, for RPC, `eth_chainId`. The same address on another chain is a different identity; frontend wallet support does not select production deployment.
3. Check code at an explicit recent block. Keep full address and block number/hash/time/retrieval internally; inspect explorer creation provenance when the requested identity or history conclusion needs it, not on every fixed snapshot. Empty code establishes absence of runtime code only at that chain/block, not historical deletion.
4. Establish the interface's provenance. Verified source or reproducible source/bytecode correspondence supports stronger implementation conclusions, but is not an absolute prerequisite for bounded calls: a publisher ABI independently retrieved and linked to the chain and full deployment address is allowed with explicit mutability, typed decoding, code checks, relevant relationship evidence and a common block. Establish scales before normalization. Bundled helpers enforce `view`/`pure`, catalog-fixed targets and bindings; supplemental nonbroadcast calls and simulations may use non-view methods without matching catalogs. Bytecode selector presence alone is insufficient. Do not borrow cross-chain ABIs. Proxies/implementations, dependencies, authorship and audit correspondence require their own evidence; do not claim them from a read result.
5. Discover connected modules through explicit constructors, documented getters and deployment events. An index seeds discovery, not completeness; authenticate each relationship to the root before using it.
6. Determine activation and privileges independently: deployed is not active; immutable code can retain configurable state/privileged calls. Bind an audit to its exact revision and deployment correspondence before claiming coverage.

Missing identity, ABI or relationship stops the affected conclusion. Return established fields plus the missing link, never guessed addresses/selectors/interfaces/roles. [Research workflow](research-workflow.md) supplies query bounds, anchors and stop conditions; [safety](safety.md) governs external reads.

## Recover a stale frontend source link

A hashed asset URL is a source locator, not a permanent API. If it is missing, the default recovery procedure starts at the current official application page rather than guessing filenames or treating cached code as current. A publisher entry bundle may import its ABI from a separate asset; historical assets may separately support explicitly historical claims.

1. Read the official page HTML as text and identify its explicit script/module references. Resolve relative URLs against the referring URL.
2. Read referenced assets as text, following static imports, re-exports and literal dynamic-import paths needed for the ABI and deployment binding. Static parsing of expressions as data, including resolving constant strings, is allowed with a bounded parser; do not `eval` downloaded expressions, run source-supplied console snippets or import untrusted modules to extract evidence.
3. Default recovery budget: three import hops, eight assets, 4 MiB per asset and 8 MiB total, following the publisher origin or another explicitly publisher-linked asset origin. These are procedure defaults, not an all-source allowlist. A task may justify different finite bounds, other provenance-bearing sources or authorized browser rendering under normal host permissions. Stop a denied operation rather than bypassing controls; report unresolved computed paths or exhausted coverage honestly.
4. Retain the original page, import chain, exact asset URLs, retrieval time and content hashes. Match the selected ABI to the full deployment address, chain and role; separate test-network and production bindings. Literal ABI text is publisher interface evidence, not verified source/bytecode correspondence or proof of current deployment.

Use recovered evidence for requested research, including [supplemental public reads](inspection.md#supplemental-public-reads) of uncataloged contracts or methods. Do not rewrite installed catalogs or redirect fixed helpers during ordinary research. Changing the bundled callable interface requires a separately reviewed, authorized package update; reading an authenticated interface with permitted external tools does not. For historical purchase/round events, follow [auction history](auction-history.md); the current snapshot helper does not retrieve logs.

## Source-reviewed mechanics versus publisher ABI leads

[Inspection](inspection.md#supply-restrictions-and-control-context) documents reviewed STANDARD/Trading Hook source semantics for cap-reduction decomposition, restriction activation and pending Hook ownership. This is not a saved verification status: fresh deployment correspondence and current state remain separate questions. Sources included as compilation dependencies do not authenticate separately deployed CentralBank, Registry, auction or vault modules.

For “Do successor migrations make the protocol upgradeable?”, answer **not by themselves**. The [whitepaper §12](https://www.standardreserve.xyz/whitepaper/#immutables) claims no proxies or code-migration mechanisms; the publisher's ABI leads require a narrower distinction:

- ContractionVault and FeeSplitter expose `migrateToSuccessor()` in the publisher-linked ABI; ExpansionVault exposes `migrateToSuccessor(address[] assets)`. They also name `HoldingsMigrated` events.
- Both auction ABIs name `supplyController()`, `setSupplyController(address)`, `SupplyControllerSet` and `NotSupplyAuthority`.
- Successor asset movement, registry replacement and component retirement are not necessarily changes to deployed code. An ABI name does not prove which assets move, who has authority, whether the published deployment implements it, or whether an auction controller acts autonomously.
- These are publisher interfaces, not authenticated implementation behavior. The fixed reader observes configured auction controllers/pending ownership and selected treasury state, not migration/setter execution. Requested explanation, unsigned preparation and nonbroadcast simulation are permitted; signing, signature requests and transaction submission/broadcast are not.

Use this packaged distinction for an explanation question; fresh implementation or current-authority claims need separate evidence. The [deployment source record](../assets/sources/deployments.json) identifies the reviewed publisher-linked bundle.

## Additional publisher-ABI research coverage

The publisher-linked mount module supplies the following **supported fixed read interfaces**, not newly source-verified Solidity implementations. Use `auctions`, `protocol` or `treasury` as scoped in [inspection](inspection.md#common-question-paths). [sr-extended-read-interface]

| Module | Supported read-only interface | Evidence boundary |
|---|---|---|
| Both auctions | `supplyController()`, `pendingOwner()` | A configured address is not authenticated controller behavior or Second Mandate activation |
| FeeSplitter | `teamShareBps()`, `polShareBps()`, `teamOwed()`, `teamWallet()`, `queuedShares()` | Current versus queued routing and accrued liability; not holder revenue rights |
| ExpansionVault | `holdingsOf(address)`, `isReserveAsset(address)`, `reservePool(address)` | Requires independently authenticated asset identities/units; does not enumerate a complete portfolio |
| ContractionVault | `lastTickAt()`, `tickCooldown()`, effective limits, `BuybackExecuted` | Distinguish attributable buyback events from aggregate burns; settings are not executable quotes |
| CentralBank | Queued-policy getters and recycling counters | Separate pending changes from current policy; raw streamed counters have unestablished scale; no parameter-event history scan |
| License v1.1 | `auctionPeriod()`, `capWindow()`, `capWindowIndex()`, `MAX_PER_CHARTER_PER_WINDOW()` | Separate round/window; charter-specific allowance methods are supplemental, retained `licensesPerDay` is per round, and stored counters can lag lazy rollover |
| POL Buyback / Incentives Vault | Generic `owner()`, `pendingOwner()`; fixed STANDARD `balanceOf(incentivesVault)` | Publisher-authenticated generic/token interfaces, not a complete new-module ABI or proof of distribution rights |

The bundled treasury snapshot requires a selected reserve asset and successful same-block vault approval before selected-asset holdings reads; raw units are not normalized without authenticated decimals. Separately, the Incentives Vault STANDARD balance uses the fixed authenticated token `balanceOf`, not a guessed vault method. Generic owners do not establish complete privileges. `history.py buybacks` retains Contraction Vault `BuybackExecuted(uint256,uint256)` burned-token accounting; `history.py pol-buybacks` uses the distinct `BuybackExecuted(uint256,uint256,address)` with raw `tokensOut` and destination. No token-binding getter, token identity/decimals or wallet flow is invented for that event-only POL mode. Bundled targets and metadata remain pinned; supplemental research may authenticate additional holdings, methods or relationships without redirecting the helper.


## Questions and independent dimensions

Documented conceptual roles include currency, charter, issuing authority, canonical Uniswap pool/hook, expansion-license and charter auctions, fee routing, reserve/buyback vaults and protocol-owned liquidity—not asserted contract names/counts.

Evidence must answer who may mint; credit/burn reconciliation; auction setters; transfer activation; reserve selection/movement; fee destinations; pauses, migration and upgrades. Do not reconstruct runtime answers from the design overview.

Use chain + full address for identity, with a stable local record ID and attribution provenance. Investigate activation, source/bytecode correspondence, proxy relationships, permissions, configuration and audit scope separately when requested. Unknowns stay not established, not a single `verified` boolean. Observations may be kept in the answer/session or authorized external artifacts with original anchors; do not rewrite installed identity records during ordinary research.

Answer the requested role or observation first, using a full address when identity is the question, plus the relevant chain and one or two source links/time anchors when needed. Default to one short relevant note (“RPC snapshot; publisher ABI.” for helper observations) and material gaps; keep exhaustive identity/provenance records and raw hashes for requested detail. If packaged identity is absent, say so and perform fresh bounded research as needed for the permitted request. User addresses are investigation inputs, not authenticity. Unsigned artifacts and informational workflows remain subject to [safety](safety.md), with no signing or submission.
