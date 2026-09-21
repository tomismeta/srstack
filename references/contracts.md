# Contracts and identity

Identity research, not an execution guide. The [entity index](../assets/entity-index.json) defines packaged attribution scope, not this filename.

## Packaged boundary

The packaged [Robinhood catalog](../assets/entities/robinhood.json) binds 12 protocol modules and two shared infrastructure entries to full addresses on **Robinhood Chain, chain ID 4663**. It contains identities, roles and explorer links, not deployment-status or verification results. [Deployment sources](../assets/sources/deployments.json) supply publisher-attribution provenance.

The fixed [read interface](../assets/interfaces/robinhood-reads.json), documented by `sr-publisher-read-interface`, pins publisher ABI metadata and target bindings for bounded read-only observations. It does not establish runtime code presence, source publication, activation or ownership; check the requested state freshly. Publisher ABI reads do not establish independently reproduced source/bytecode correspondence.

Use **[Robinhood Etherscan](https://robin.etherscan.io/)** and each catalog entry's explorer link for fresh source/ABI publication and verification lookups. Match chain plus full address; Ethereum `etherscan.io` is chain 1. A similar-match label alone does not authenticate this deployment's semantics. If the lookup or read is unavailable, report the affected result as unavailable; never reuse a saved verdict.

The directory also lists a pool manager and Multicall as shared infrastructure. Neither is project-authored merely because listed; a pool manager is not a unique canonical-pool address. Do not import Arbitrum or local-test records from the frontend bundle into this Robinhood group.

For public observations, use [inspection](inspection.md), including its [units and financial interpretation](inspection.md#units-and-financial-interpretation). An address alone supplies neither ABI semantics, economic defaults, gas estimates nor authorization for financial actions.

## Authenticate the requested role

1. Find original official website/account deployment evidence identifying the role, chain and environment—not a quoted third party or infrastructure component. Retain URL, author and publication/retrieval times.
2. Establish chain authority and, for RPC, `eth_chainId`. The same address on another chain is a different identity; frontend wallet support does not select production deployment.
3. Check code at an explicit recent block. Keep full address and block number/hash/time/retrieval internally; inspect explorer creation provenance when the requested identity or history conclusion needs it, not on every fixed snapshot. Empty code establishes absence of runtime code only at that chain/block, not historical deletion.
4. Establish the interface's provenance. Verified source or reproducible source/bytecode correspondence supports stronger implementation conclusions, but is not an absolute prerequisite for bounded reads: the fixed publisher-authenticated ABI is allowed with explicit read-only mutability, typed decoding/scales, code checks, matching module bindings and a common block. Bytecode selector presence alone is insufficient. Do not borrow cross-chain ABIs. Proxies/implementations, dependencies, authorship and audit correspondence require their own evidence; do not claim them from a read result.
5. Discover connected modules through explicit constructors, documented getters and deployment events. An index seeds discovery, not completeness; authenticate each relationship to the root before using it.
6. Determine activation and privileges independently: deployed is not active; immutable code can retain configurable state/privileged calls. Bind an audit to its exact revision and deployment correspondence before claiming coverage.

Missing identity, ABI or relationship stops the affected conclusion. Return established fields plus the missing link, never guessed addresses/selectors/interfaces/roles. [Research workflow](research-workflow.md) supplies query bounds, anchors and stop conditions; [safety](safety.md) governs external reads.

## Recover a stale frontend source link

A hashed asset URL is a source locator, not a permanent API. If it is missing, start at the current official application page—not guessed filenames or cached code. A publisher entry bundle may import its ABI from a separate asset.

1. Read the official page HTML as text and identify its explicit script/module references. Resolve relative URLs against the referring URL.
2. Read the referenced entry asset as text. Follow only explicit static imports, re-exports or literal dynamic-import paths needed to locate the relevant ABI and deployment binding. Do not evaluate expressions, execute downloaded JavaScript, run a browser-console snippet or import the module into a local runtime.
3. Keep discovery finite: at most three import hops, eight assets, 4 MiB per asset and 8 MiB total. Stay on the publisher origin unless the official page explicitly authenticates another asset origin. Stop at access denial, exhausted bounds, unreadable content or an unresolved computed import; report the missing evidence rather than bypassing restrictions.
4. Retain the original page, import chain, exact asset URLs, retrieval time and content hashes. Match the selected ABI to the full deployment address, chain and role; separate test-network and production bindings. Literal ABI text is publisher interface evidence, not verified source/bytecode correspondence or proof of current deployment.

Use recovered evidence for the requested research, including [supplemental public reads](inspection.md#supplemental-public-reads) of uncataloged contracts or methods. Never rewrite installed catalogs or redirect a fixed helper to a discovered address. Changing the bundled callable interface requires a separately reviewed package update; reading an authenticated interface with permitted external tools does not. For historical purchase/round events, follow [auction history](auction-history.md); the current snapshot helper does not retrieve logs.

## Source-reviewed mechanics versus publisher ABI leads

[Inspection](inspection.md#supply-restrictions-and-control-context) documents reviewed STANDARD/Trading Hook source semantics for cap-reduction decomposition, restriction activation and pending Hook ownership. This is not a saved verification status: fresh deployment correspondence and current state remain separate questions. Sources included as compilation dependencies do not authenticate separately deployed CentralBank, Registry, auction or vault modules.

For “Do successor migrations make the protocol upgradeable?”, answer **not by themselves**. The [whitepaper §12](https://www.standardreserve.xyz/whitepaper/#immutables) claims no proxies or code-migration mechanisms; the publisher's ABI leads require a narrower distinction:

- ContractionVault and FeeSplitter expose `migrateToSuccessor()` in the publisher-linked ABI; ExpansionVault exposes `migrateToSuccessor(address[] assets)`. They also name `HoldingsMigrated` events.
- Both auction ABIs name `supplyController()`, `setSupplyController(address)`, `SupplyControllerSet` and `NotSupplyAuthority`.
- Successor asset movement, registry replacement and component retirement are not necessarily changes to deployed code. An ABI name does not prove which assets move, who has authority, whether the published deployment implements it, or whether an auction controller acts autonomously.
- These are publisher interfaces, not authenticated implementation behavior. The fixed reader now observes configured auction controllers/pending ownership and selected treasury state; migration/setter calls remain forbidden.

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

The bundled treasury snapshot requires a selected asset and successful same-block reserve approval before holdings reads; this is a helper filter, not permission to inspect the asset. Amounts remain raw token units without authenticated decimals. Flat tuples preserve component types/units and pending flags. Buyback history uses `BuybackExecuted` events, not aggregate burn counters. Bundled bindings, selectors and units remain pinned in the reviewed catalogs; do not redirect the helper. For additional holdings, metadata, events or relationships, use [supplemental public reads](inspection.md#supplemental-public-reads), including locally authored read-only request code. The [Second Mandate](updates.md#second-mandate-liquidity-for-tokenized-stocks) supplies intended functions, not named new contracts.


## Questions and independent dimensions

Documented conceptual roles include currency, charter, issuing authority, canonical Uniswap pool/hook, expansion-license and charter auctions, fee routing, reserve/buyback vaults and protocol-owned liquidity—not asserted contract names/counts.

Evidence must answer who may mint; credit/burn reconciliation; auction setters; transfer activation; reserve selection/movement; fee destinations; pauses, migration and upgrades. Do not reconstruct runtime answers from the design overview.

Use chain + full address for identity, with a stable local record ID and attribution provenance. Investigate activation, source/bytecode correspondence, proxy relationships, permissions, configuration and audit scope separately when requested. Unknowns stay not established, not a single `verified` boolean. Keep observations in the answer/session; do not persist state or verification results in identity records or rewrite installed resources.

Answer the requested role or observation first, using a full address when identity is the question, plus the relevant chain and one or two source links/time anchors when needed. Default to one short relevant note (“RPC snapshot; publisher ABI.” for helper observations) and material gaps; keep exhaustive identity/provenance records and raw hashes for requested detail. If packaged identity is absent, say so and perform fresh bounded public research only when requested/permitted. User addresses are investigation inputs, not authenticity. Never prepare state-changing artifacts.
