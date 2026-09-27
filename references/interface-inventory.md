# Reviewed interface inventory

**As of 2026-09-27.** Full data for every identified protocol-role ABI definition in the reviewed complete publisher module, not merely the question-driven guide's selected signatures. This is optional research/decoding evidence, not a runtime client, an execution allowlist, current address routing or implementation certification. Fresh authenticated interfaces remain usable without catalog membership.

Use the [capability map](capabilities.md) for available, not-exposed and unknown questions; the [question guide](interface-guide.md) for common reads and units; [contracts](contracts.md) for identity; and the [required addition methodology](inventory-methodology.md) for future contracts/interfaces. Missing implementation proof limits the affected interpretation, not all useful public observations.

## Scope and discoverability

The complete [official application module](https://www.standardreserve.xyz/assets/mountApp-z6PyBslD.js), explicitly linked by the [application HTML](https://www.standardreserve.xyz/app/), was parsed as data, never executed. The 860946-byte UTF-8 body has SHA-256 `8e2178e9e11adc78288afeb0a95bf1c62e7ac118ba08986b3033c2d740cdbd31`. Whole-body, literal/expression and binding fingerprints live in [shared reviews](../assets/interfaces/reviews.json), with the source chain in [source records](../assets/sources/live-interface.json). These are dated provenance, not a future source acceptance allowlist.

**15 interfaces, 905 entries, 19 dated bindings.** Twelve full protocol literals plus the explicit v1.1 license adaptation account for complete publisher definitions; two selective fragments supply control and shared Multicall leads. Constructors, functions, events, errors and receive entries are retained wherever present. No fallback is declared by these definitions. “Complete” means the reviewed publisher definition is fully represented, **not** that every deployed method or historical generation is known.

| Role / generation | Data | Entries | Discovery note |
| --- | --- | --- | --- |
| CentralBank / original | [central-bank](../assets/interfaces/central-bank.json) | 112 | [Core](interface-inventory-core.md): issuance, ledger, branch and activity surface |
| CharterNFT / original | [charter-nft](../assets/interfaces/charter-nft.json) | 47 | [Core](interface-inventory-core.md): ownership, approvals, both safe-transfer overloads |
| STANDARD / original | [standard](../assets/interfaces/standard.json) | 55 | [Core](interface-inventory-core.md): balances, supply, restrictions and token errors |
| TaxHook / original | [tax-hook](../assets/interfaces/tax-hook.json) | 80 | [Hook](interface-inventory-hook.md): pool tuples, callbacks, flow, taxes and oracle fields |
| ContractionVault / original | [contraction-vault](../assets/interfaces/contraction-vault.json) | 66 | [Treasury](interface-inventory-treasury.md): rate-limited buyback/burn interface |
| ExpansionVault / original | [expansion-vault](../assets/interfaces/expansion-vault.json) | 45 | [Treasury](interface-inventory-treasury.md): selected reserve assets and pool metadata |
| FeeSplitter / original | [fee-splitter](../assets/interfaces/fee-splitter.json) | 38 | [Treasury](interface-inventory-treasury.md): active/queued routing and team liability |
| GenesisMinter / original | [genesis-minter](../assets/interfaces/genesis-minter.json) | 91 | [Founding](interface-inventory-founding.md): founding sale, distinct from ongoing auctions |
| License auction / original | [license-auction-original](../assets/interfaces/license-auction-original.json) | 70 | [Auctions](interface-inventory-auctions.md): original day-keyed allowance |
| License auction / v1.1 | [license-auction-v1-1](../assets/interfaces/license-auction-v1-1.json) | 73 | [Auctions](interface-inventory-auctions.md): explicit adapter, constructor omitted |
| License auction / v1.2 | [license-auction-v1-2](../assets/interfaces/license-auction-v1-2.json) | 88 | [Auctions](interface-inventory-auctions.md): window allowance and charter-keyed bids |
| Charter auction / original | [charter-auction-original](../assets/interfaces/charter-auction-original.json) | 67 | [Auctions](interface-inventory-auctions.md): no separate v1.1 charter mapping found |
| Charter auction / v1.2 | [charter-auction-v1-2](../assets/interfaces/charter-auction-v1-2.json) | 67 | [Auctions](interface-inventory-auctions.md): independent ETH-priced auction |
| Publisher control fragment | [publisher-control-fragment](../assets/interfaces/publisher-control-fragment.json) | 3 | [Infrastructure and gaps](interface-inventory-infrastructure.md): selective reads, not full Registry ABI |
| Multicall infrastructure fragment | [multicall3-fragment](../assets/interfaces/multicall3-fragment.json) | 3 | [Infrastructure and gaps](interface-inventory-infrastructure.md): shared infrastructure, not project-authored protocol |

## Coverage and explicit gaps

The AST review classified **all 24 pure ABI-shaped literal arrays** in this module: 21 named arrays (12 protocol literals, the included Multicall fragment and eight SDK utility arrays) plus three inline SDK NFT-metadata/ENS arrays. The two composed SDK ENS definitions `d0`/`e6` are separately excluded. It also reviewed `sa` declaration strings, the explicit `b_` adaptation, subscription event subsets and bound role calls. SDK ERC20/ENS/DNS/signature/domain helpers do not authenticate additional protocol deployments. `Gp`/`yC` event subsets agree with the corresponding full role layouts, rather than constituting extra contracts.

Registry, Genesis Liquidity Manager (`polManager`), POL Buyback and Incentives Vault have **no complete role ABI bound here**. The publisher control fragment supplies only scoped administrator reads; `executionPermissionless()` is explicitly attributed to Registry alone. PoolManager has a dated shared-infrastructure identity but **no bound ABI**. These are unknown broader interfaces, not claims that the contracts lack other capabilities. Historical POL event evidence elsewhere remains separately scoped and does not manufacture a complete POL ABI.

Imported/chunk-specific interfaces outside this module and all-time deployment history are not claimed complete. Original/v1.1/v1.2 auction definitions are present here because the publisher retains explicit historical definitions and generation selection. The v1.1 license adapter removes the constructor and named original declarations, then adds literal window declarations; its complete adapter does not establish the deployed constructor. No separate v1.1 charter replacement is invented.

## Data layout and event decoding

Each interface has stable `id`, `role`, `generation`, one shared `review_id`, exact `coverage` metadata and ordered `entries`. Each entry carries:

- `abi`: complete JSON ABI entry, including input/output order, names, internal types, tuple components, mutability, event `anonymous` and every explicit `indexed` bit.
- `signature`: canonical input-type signature; tuples expand recursively. Overloads remain distinct. Return types/names/indexing are **not** part of selector/topic hashing.
- `declaration`: readable ABI declaration with **`indexed` visibly present** for event topic fields. Do not use `signature` alone as a decoder declaration.
- `selector` for functions/errors, or `topic0` for nonanonymous events: Ethereum Keccak-256, not NIST SHA3-256. Constructors/receive/fallback have no selector.
- `event_layout`: ordered fields with `abi_index`, canonical type, `indexed`, and either `topic_index` or `data_parameter_index`. A data parameter index is **not a word offset**: dynamic/tuple fields require ABI decoding. Indexed strings/bytes/arrays/tuples are hash commitments, not recoverable raw values.
- `explanation`, `units`, `limitations`, entry `generation` and `review_id`: bounded interpretation and explicit unknown semantics, not manufactured implementation proof.

For example, license `LicensesPurchased` has charterId/day in topics 1/2 and count/unitPrice in data. Charter `CharterPurchased` has charterId/buyer/day in topics 1/2/3 and only price in data. Bank `CheckedIn` has indexed wallet and empty data. NFT and ERC20 `Transfer(address,address,uint256)` share topic0 but place their third field differently; authenticate emitter/role before decoding. Full definitions are directly adjacent to these explanations in the JSON, avoiding signature-only indexing loss.

## Dated contract bindings

[contracts.json](../assets/entities/contracts.json) maps chain, full historical address, publisher role and generation to reviewed interface IDs with retrieval date and source locator. It has no active/default/current aliases. Publisher activation metadata, when present, is labelled separately from creation and independently established Registry cutover. `selected_functions` restricts fragment attribution—for example Registry's execution flag is not copied to liquidity/POL/incentives roles.

No installed entry selects today's target. Authenticate relevant chain, code, binding and block before reading; preserve historical generation/address for interval queries. A fungible-token address here is opt-in dated provenance, not a fixed runtime token identity.

## Maintenance integrity

Source-only `maintenance/inventory.py` exposes `validate_inventory(files)` for packaging. It checks inventory/review/source/binding closure; full ABI digests and entry-kind counts; canonical tuple signatures; Ethereum selectors/topics; explicit indexed layouts; entry provenance and semantic qualifications; and capability references/negative claims. `maintenance/check-inventory.py` contains behavior regressions. These helpers are not installed runtime clients and perform no network access. A new addition must follow the [review methodology](inventory-methodology.md), not merely append a function name or copy a similarly named ABI.
