# Contracts and identity

Identity research, not an execution guide. The [entity index](../assets/entity-index.json) defines packaged attribution scope, not this filename.

## Packaged boundary

The official website lists **14 addresses on Robinhood Chain, chain ID 4663**: 12 protocol modules and two shared infrastructure entries. Read [the Robinhood catalog](../assets/entities/robinhood.json) with its shared limits for full addresses, roles and Etherscan links. [Deployment sources](../assets/sources/deployments.json) establish current publisher attribution; [Etherscan sources](../assets/sources/etherscan.json) record source-publication observations.

The packaged explorer checks record bytecode at all 14 addresses, with no published protocol-module or Pool Manager source/ABI on RobinScan. Multicall's **Similar Match** points to Arbitrum Sepolia; that does not move this deployment off Robinhood Chain or authenticate protocol semantics. Separately, the official app publishes the ABI used by the fixed [read interface](../assets/interfaces/robinhood-reads.json), documented by `sr-publisher-read-interface`. This supports bounded publisher-ABI observations under the checks below, not independently reproduced source/bytecode correspondence. Owner/configuration getters are block-scoped observations; complete privileges, implementation properties and audit correspondence remain separate questions.

Use **[Robinhood Etherscan](https://robin.etherscan.io/)** for navigation and new explorer checks. Match chain plus full address; Ethereum `etherscan.io` is chain 1. Report unavailable reads as gaps, not verification verdicts.

The directory also lists a pool manager and Multicall as shared infrastructure. Neither is project-authored merely because listed; a pool manager is not a unique canonical-pool address. Do not import Arbitrum or local-test records from the frontend bundle into this Robinhood group.

For planning, use the [deployment-evidence handoff](planning-inputs.md#deployment-evidence-handoff). The fixed snapshot reader can inform a partial assumption sheet; an address alone supplies neither ABI semantics, economic defaults, gas estimates nor authorization for financial actions.

## Authenticate the requested role

1. Find original official website/account deployment evidence identifying the role, chain and environment—not a quoted third party or infrastructure component. Retain URL, author and publication/retrieval times.
2. Establish chain authority and, for RPC, `eth_chainId`. The same address on another chain is a different identity; frontend wallet support does not select production deployment.
3. Check code at an explicit recent block. Keep full address and block number/hash/time/retrieval internally; inspect explorer creation provenance when the requested identity or history conclusion needs it, not on every fixed snapshot. Empty code establishes absence of runtime code only at that chain/block, not historical deletion.
4. Establish the interface's provenance. Verified source or reproducible source/bytecode correspondence supports stronger implementation conclusions, but is not an absolute prerequisite for bounded reads: the fixed publisher-authenticated ABI is allowed with explicit read-only mutability, typed decoding/scales, code checks, matching module bindings and a common block. Bytecode selector presence alone is insufficient. Do not borrow cross-chain ABIs. Proxies/implementations, dependencies, authorship and audit correspondence require their own evidence; do not claim them from a read result.
5. Discover connected modules through explicit constructors, documented getters and deployment events. An index seeds discovery, not completeness; authenticate each relationship to the root before using it.
6. Determine activation and privileges independently: deployed is not active; immutable code can retain configurable state/privileged calls. Bind an audit to its exact revision and deployment correspondence before claiming coverage.

Missing identity, ABI or relationship stops the affected conclusion. Return established fields plus the missing link, never guessed addresses/selectors/interfaces/roles. [Research workflow](research-workflow.md) supplies query bounds, anchors and stop conditions; [safety](safety.md) governs external reads.

## Questions and independent dimensions

Documented conceptual roles include currency, charter, issuing authority, canonical Uniswap pool/hook, expansion-license and charter auctions, fee routing, reserve/buyback vaults and protocol-owned liquidity—not asserted contract names/counts.

Evidence must answer who may mint; credit/burn reconciliation; auction setters; transfer activation; reserve selection/movement; fee destinations; pauses, migration and upgrades. Do not reconstruct runtime answers from the design overview.

Use chain + full address for identity, with a stable local record ID. Keep attribution evidence, environment/generation, creation and current activation anchors, source/bytecode scope, proxy/implementation relationships, roles/permissions/configuration and audit scope/unresolved findings independent. Unknowns stay null/not established, not a single `verified` boolean. Do not persist changing balances/prices as identity attributes or rewrite installed records.

Answer the requested role or observation first, using a full address when identity is the question, plus the relevant chain and one or two source links/time anchors when needed. Default to one short relevant note (“RPC snapshot; publisher ABI.” for helper observations) and material gaps; keep exhaustive identity/provenance records and raw hashes for requested detail. If packaged identity is absent, say so and perform fresh bounded public research only when requested/permitted. User addresses are investigation inputs, not authenticity. Never prepare state-changing artifacts.
