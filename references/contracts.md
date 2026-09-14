# Contracts and identity

Identity research, not an execution guide. The [entity index](../assets/entity-index.json) defines packaged attribution scope, not this filename.

## Packaged boundary

The official website lists **14 addresses on Robinhood Chain, chain ID 4663**: 12 protocol modules and two shared infrastructure entries. Read [the Robinhood catalog](../assets/entities/robinhood.json) with its shared limits for full addresses, roles and Etherscan links. [Deployment sources](../assets/sources/deployments.json) establish current publisher attribution; [Etherscan sources](../assets/sources/etherscan.json) record source-publication observations.

All 14 address pages display bytecode. The 12 protocol modules and Pool Manager have no published source/ABI on RobinScan; Multicall exposes source and ABI through **Similar Match** to a contract on Arbitrum Sepolia. The deployment itself is still on Robinhood Chain. Similar Match is not independently reproduced exact-bytecode verification, and infrastructure source availability does not authenticate protocol-module semantics. Current ownership, proxy/implementation relationships, activation and audit correspondence remain unestablished.

Use **[Robinhood Etherscan](https://robin.etherscan.io/)** for navigation and new explorer checks. Match chain plus full address; Ethereum `etherscan.io` is chain 1. Report unavailable reads as gaps, not verification verdicts.

The directory also lists a pool manager and Multicall as shared infrastructure. Neither is project-authored merely because listed; a pool manager is not a unique canonical-pool address. Do not import Arbitrum or local-test records from the frontend bundle into this Robinhood group.

For planning, use the [deployment-evidence handoff](planning-inputs.md#deployment-evidence-handoff). An address enables targeted research, not automatic gas estimates, economic defaults, ABI calls or financial actions.

## Authenticate the requested role

1. Find original official website/account deployment evidence identifying the role, chain and environment—not a quoted third party or infrastructure component. Retain URL, author and publication/retrieval times.
2. Establish chain authority and, for RPC, `eth_chainId`. The same address on another chain is a different identity; frontend wallet support does not select production deployment.
3. Check code at an explicit recent block and explorer creation provenance. Keep full address, block number/hash/time, retrieval time, creation transaction and role. Empty code establishes absence of runtime code only at that chain/block, not historical deletion.
4. Establish verified source or reproducible source/bytecode correspondence. Identify proxies, implementations, constructors/initializers, libraries and external dependencies. A badge does not establish authorship or an audit.
5. Discover connected modules through explicit constructors, documented getters and deployment events. An index seeds discovery, not completeness; authenticate each relationship to the root before using it.
6. Determine activation and privileges independently: deployed is not active; immutable code can retain configurable state/privileged calls. Bind an audit to its exact revision and deployment correspondence before claiming coverage.

Missing identity, ABI or relationship stops the affected conclusion. Return established fields plus the missing link, never guessed addresses/selectors/interfaces/roles. [Research workflow](research-workflow.md) supplies query bounds, anchors and stop conditions; [safety](safety.md) governs external reads.

## Questions and independent dimensions

Documented conceptual roles include currency, charter, issuing authority, canonical Uniswap pool/hook, expansion-license and charter auctions, fee routing, reserve/buyback vaults and protocol-owned liquidity—not asserted contract names/counts.

Evidence must answer who may mint; credit/burn reconciliation; auction setters; transfer activation; reserve selection/movement; fee destinations; pauses, migration and upgrades. Do not reconstruct runtime answers from the design overview.

Use chain + full address for identity, with a stable local record ID. Keep attribution evidence, environment/generation, creation and current activation anchors, source/bytecode scope, proxy/implementation relationships, roles/permissions/configuration and audit scope/unresolved findings independent. Unknowns stay null/not established, not a single `verified` boolean. Do not persist changing balances/prices as identity attributes or rewrite installed records.

Answer **role; chain/environment; full authenticated address; attribution source; code/activation observations; limitations**. If packaged identity is absent, say so; perform fresh bounded public research only when requested/permitted. User addresses are investigation inputs, not authenticity. Never prepare state-changing artifacts.
