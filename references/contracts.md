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

## Source-reviewed mechanics versus publisher ABI leads

[Inspection](inspection.md#supply-restrictions-and-control-context) documents reviewed STANDARD/Trading Hook source semantics for cap-reduction decomposition, restriction activation and pending Hook ownership. This is not a saved verification status: fresh deployment correspondence and current state remain separate questions. Sources included as compilation dependencies do not authenticate separately deployed CentralBank, Registry, auction or vault modules.

For “Do successor migrations make the protocol upgradeable?”, answer **not by themselves**. The [whitepaper §12](https://www.standardreserve.xyz/whitepaper/#immutables) claims no proxies or code-migration mechanisms; the publisher's ABI leads require a narrower distinction:

- ContractionVault and FeeSplitter expose `migrateToSuccessor()` in the publisher-linked ABI; ExpansionVault exposes `migrateToSuccessor(address[] assets)`. They also name `HoldingsMigrated` events.
- Both auction ABIs name `supplyController()`, `setSupplyController(address)`, `SupplyControllerSet` and `NotSupplyAuthority`.
- Successor asset movement, registry replacement and component retirement are not necessarily changes to deployed code. An ABI name does not prove which assets move, who has authority, whether the published deployment implements it, or whether an auction controller acts autonomously.
- These are publisher-interface research leads, not authenticated deployed behavior. They are outside the fixed reader and never authorize a migration or setter call.

Use this packaged distinction for an explanation question; fresh implementation or current-authority claims need separate evidence. The [deployment source record](../assets/sources/deployments.json) identifies the reviewed publisher-linked bundle.

## Questions and independent dimensions

Documented conceptual roles include currency, charter, issuing authority, canonical Uniswap pool/hook, expansion-license and charter auctions, fee routing, reserve/buyback vaults and protocol-owned liquidity—not asserted contract names/counts.

Evidence must answer who may mint; credit/burn reconciliation; auction setters; transfer activation; reserve selection/movement; fee destinations; pauses, migration and upgrades. Do not reconstruct runtime answers from the design overview.

Use chain + full address for identity, with a stable local record ID and attribution provenance. Investigate activation, source/bytecode correspondence, proxy relationships, permissions, configuration and audit scope separately when requested. Unknowns stay not established, not a single `verified` boolean. Keep observations in the answer/session; do not persist state or verification results in identity records or rewrite installed resources.

Answer the requested role or observation first, using a full address when identity is the question, plus the relevant chain and one or two source links/time anchors when needed. Default to one short relevant note (“RPC snapshot; publisher ABI.” for helper observations) and material gaps; keep exhaustive identity/provenance records and raw hashes for requested detail. If packaged identity is absent, say so and perform fresh bounded public research only when requested/permitted. User addresses are investigation inputs, not authenticity. Never prepare state-changing artifacts.
