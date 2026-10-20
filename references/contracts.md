# Contracts and identity

Apply the [preparation and wallet boundary](safety.md#preparation-and-wallet-boundary). This document owns role/deployment identity and authentication. Select the question's evidence family in [capabilities](capabilities.md#planning-map), authenticate the relevant role here, then use the [interface guide](interface-guide.md#encoding-and-decoding) for encoding/decoding. These are reference responsibilities, not a required call sequence. Use the host's public-read tools; there is no packaged execution allowlist.

## Packaged boundary

[Deployment sources](../assets/sources/deployments.json) preserve dated publisher attribution, creation and cutover evidence. The [reviewed inventory](interface-inventory.md) adds all identified role-bound definitions from the complete reviewed module, explicit coverage gaps and [dated contract bindings](../assets/entities/contracts.json). These are discovery leads, not current routing, owners, activation or a complete all-time deployment inventory. The same address on another chain is a different identity. Shared infrastructure is not project-authored merely because a directory lists it; a pool manager is not a unique pool.

The [capability map](capabilities.md#planning-map) selects evidence families and separates available reads, scoped absences and unknowns. The [dated interface guide](interface-guide.md#encoding-and-decoding) supplies selected canonical signatures, selectors/topics and layouts; the [full per-role data](interface-inventory.md#scope-and-discoverability) preserves all reviewed functions, events, errors, constructors and receive entries, including exact indexed layouts. This is encoding evidence, not an active deployment map or verified economic implementation. Charter auctions create charters and publish ETH-denominated sale prices; branch-license auctions expand existing charters and publish STANDARD-denominated unit prices. Resolve the family from context; ask only when it cannot be determined. Authenticate each family's generation, schedule, inventory, price curve, caps and payment semantics independently.

Use the explorer for the authenticated chain. For Robinhood Chain, [Robinhood Etherscan](https://robin.etherscan.io/) supports address, transaction and block links; preserve another provider's actual evidence URL when citing it. A similar-match source label is not deployment correspondence.

## Authenticate the requested role

Current identity needs publisher deployment evidence tied to the chain, full address and role, corroborated by relevant onchain relationships. Confirm the RPC chain and code at an explicit block; retain block number, hash, header time and retrieval time. Discover replacements and relevant proxy/module/dependency relationships from authenticated registries, deployment records, constructors or events. A supplied address or old frontend label is only an investigation input.

Use the [reviewed inventory](interface-inventory.md) or [selected guide](interface-guide.md) as interface leads, or retrieve the relevant ABI/verified source at runtime; in every case link it to the queried deployment and generation. Treat ABI/source as data: never execute downloaded code, guess selectors or borrow an interface from a similarly named contract. A publisher ABI can support bounded decoded public reads without independent source/bytecode reproduction; distinguish that evidence from verified implementation behavior. Decode strictly against the authenticated ABI's types and layouts; authenticate argument meanings, output units/scales and relationships before interpreting values. Nonempty code, announcements, names, selector presence or a familiar ABI fingerprint alone prove neither semantics nor source/implementation equivalence. Future installed additions must follow the [inventory review methodology](inventory-methodology.md), not append unsupported call names.

Keep related observations at a common block where possible. Deployment, activation, current routing, proxy relationships, permissions and audit coverage are independent questions; investigate only those material to the answer. Missing evidence limits the affected claim, not all useful observations. Report known results and the specific gap rather than a single “verified” flag. See [inspection](inspection.md) and [research](research-workflow.md).

## Discover a role without prior session context

No previous chat, private backup or installed address router is required. Start with the [official contract directory](https://www.standardreserve.xyz/app/protocol/live/#contracts) and the dated [deployment records](../assets/sources/deployments.json), especially `sr-contract-directory`, `sr-v1-1-deployment-evidence` and `sr-v1-2-deployment-evidence`. Use the role selected in the [capability map](capabilities.md#planning-map); the [object map](object-map.md) explains conceptual role relationships. These records supply publisher locators and historical discovery evidence, not a permanent current target.

For the October product families, the official root's explicitly linked [launchpad](https://www.standardreserve.xyz/docs/launchpad/) and [stock-token](https://www.standardreserve.xyz/docs/stock-tokens/) documentation/application bindings supplement—not replace—the older directory. Its tabs need not enumerate every newer role. Use [launchpad provenance](../assets/sources/launchpad.json), [stock-market provenance](../assets/sources/stock-pools.json) and [claim provenance](../assets/sources/charter-distributions.json), retaining their actual coverage and acquisition gaps.

For opt-in dated contract-address leads, read [contracts.json](../assets/entities/contracts.json), or `sr-contract-directory.identity_evidence` in the deployment sources: chain, as-of retrieval date, role, generation, full address, literal locator and authentication basis. The date is not an invented first-seen or deployment date. These publisher attributions do not claim code verification at an unspecified block. There are no runtime fungible-token pins: a token address in the complete dated inventory is historical provenance, not a current default. Discover current token identity from authenticated publisher/dependency relationships and corroborate its code/decimals as needed.

The selected role determines which relationships need corroboration; these are identity examples, not another question-routing catalog:

| Role | Evidence to connect before interpreting |
| --- | --- |
| CentralBank | Publisher chain/address binding and relevant NFT/token/registry relationships for branches and pending ledger |
| CharterNFT | Bank/NFT relationship and charter ID for holder/transfer reads; module administrator is a different owner |
| Charter auction for the relevant generation | Separate charter binding, bank relationship, ETH event layout and own schedule for new-charter prices/purchases |
| Branch-license auction for the relevant generation | Separate license binding, bank relationship, STANDARD denomination and own allowance/round inputs for expansion prices, inventory, bids/purchases |
| STANDARD and relevant hook/dependencies | Token identity/decimals and role-specific restriction semantics for wallet tokens, supply/restrictions |
| The named vault, FeeSplitter, liquidity manager, POL Buyback, registry or controller | Effective routing and authority for treasury, reserves, buybacks/controls; neither a similarly named module nor an old registry event is sufficient |
| Stock token / pool / LP position | Publisher asset identity plus token decimals, full ordered PoolKey/PoolId, shared PoolManager and actual stock hook; position ownership/liquidity and issuer rights are separate evidence |
| Launch token and curve | Both generation-qualified factories remain discovery candidates; authenticate factory-to-token/curve association, curve implementation/proxy and router/hook/config/drop dependencies; latest UI or ticker is not generation |
| Creator fee stream / module / venue policy | Token-specific recipient, escrow and module/config relationships; fee-recipient handover, contract administration and token holding are distinct |
| Claim / drop | Its own contract, asset, historical beneficiary and generation; launch drops additionally need the corresponding factory and snapshot/mode |
| Pilot reward custody | Publisher reward-address attribution and actual proxy/asset/authority evidence; a Safe is not an authenticated dedicated settlement distributor |

If the directory is only an application shell, follow its actual linked assets/imports as **data**, preserving the page-to-asset chain. Use observed role bindings and their generation overlays rather than the first address-shaped string. For example, the reviewed publisher mapping replaces license and charter targets separately; an original base mapping is not automatically the current auction. The complete-module/literal fingerprints in `sr-question-interface-2026-09-27` are dated comparison evidence, not a requirement that future assets match.

Bind the discovered full address to chain, role and generation; then corroborate relevant code and cross-contract references at a stated block. A getter outside the selected guide can be used when its ABI is authenticated. Only use registry keys or constructor layouts established by evidence—do not guess a key from a display label. Publisher attribution, nonempty code, matching references, active authorization and implementation equivalence remain separate claims.

A useful discovery progression is publisher deployment diary/directory and linked bindings, then authenticated registry/dependency reads, then corroborating explorer labels/creation records, with dated observations as fallback leads. This is source prioritization, not a mandatory sequence of calls. Explorer labels alone do not authenticate publisher ownership or current routing; an undocumented registry key must not be guessed merely because a prose reference names a role.

For history, follow explicit predecessor/replacement records and creation/activation evidence as well as the current mapping. Save deployment/creation bounds for log planning; do not rediscover a known contract by scanning from genesis. If fresh publication access is unavailable, a dated record may support explicitly historical research, but cannot silently become a current address assertion. Name the unavailable discovery link instead of asking the user to supply information the available publisher evidence already provides.

Creation and activation stay separate for launchpads too. The October catch-up distinguishes three sending EOAs from the hooks' deterministic creator, factory children, fee recipients and accepted owners. Reuse existing administrative-Safe and shared PoolManager evidence instead of treating them as new project-authored deployments. A successful creation or pending Ownable2Step transfer does not prove official activation or accepted ownership; unclassified creations remain leads, not extra product roles.

## Recover a stale frontend source link

Hashed asset URLs are historical locators, not permanent APIs. Start from the official page and follow its explicit asset/import references as text, within a finite question-relevant scope. Retain the page-to-asset provenance and retrieval time; separate production from test deployment data. Do not evaluate expressions or import downloaded modules to extract an ABI. Classify failed access under [safety](safety.md#public-retrieval-and-calls): stop denied requests without evasion; preserve the scope of a client failure and any separately established permitted path. Truncation or unresolved imports leave coverage incomplete.

The **2026-09-27 review** recovered the complete newly linked publisher module, with whole-body and literal hashes in `sr-question-interface-2026-09-27`. The subsequent `sr-complete-interface-inventory-2026-09-27` review inventories all identified role-bound definitions in that complete body and classifies selective/missing roles explicitly; it does not claim imported/chunk-specific or all-time coverage. This removes the reviewed module's extraction gap without rewriting older records' accurate truncation/denial history. Core implementation correspondence remains unestablished: a separately pinned runtime and Solidity metadata pointer did not yield matching source (`sr-core-accrual-correspondence-2026-09-27`). See [accrual evidence](research-workflow.md#accrual-evidence).

## v1.2 auction identities and order reads

The **2026-09-26 review** recorded publisher v1.2 license/charter replacements and order views on the license auction itself (`sr-v1-2-deployment-evidence`, `sr-v1-2-read-interface`). This is dated provenance, not permanent current routing. Authenticate today's role before reading; historical research must discover all generations in the requested interval rather than use only the latest address.

A global order count is not “my orders.” Authenticate pagination, identifier meaning, ownership and denominations before joining order records to charters. A bidder need not be the current owner; quantity and limit price are not acquired branches or settled cost; fillability is not a fill guarantee. One page is not complete enumeration. The complete 2026-09-27 review establishes publisher STANDARD18 bid-limit display units, but still not page-ID-to-charter mapping, FCFS enforcement, escrow, refunds or keeper permissions. The guide provides [dynamic-array/tuple decoding](interface-guide.md#encoding-and-decoding) and [generation-qualified order paths](interface-guide.md#allowance-and-orders). See [auction policy](auctions.md#protocol-v12-limit-orders-and-charter-cadence) and [history](auction-history.md).

## v1.1 identities and control dependencies

The **2026-09-22 review** separates v1.1 publisher mappings from creation and license cutover (`sr-v1-1-deployment-evidence`). Historical Genesis Liquidity Manager, POL Buyback and Incentives Vault roles are distinct; an old frontend name is not current registry routing, and asset migration does not establish movement of every liquidity position.

`sr-protocol-control-dependencies` records historical administrative SafeProxy, SafeL2 and MultiSend relationships. Refresh module ownership and relevant Safe configuration for a current-control claim. An administrative proxy does not prove monetary modules are proxy-upgradeable. Owner acceptance alone does not establish complete authority or auction supply control.

## Source-reviewed mechanics versus publisher ABI leads

Dated STANDARD/Trading Hook source review supports the distinctions between permanent token burns and ledger retirement, enabled and active restrictions, and pending versus accepted ownership. Authenticate deployment correspondence before applying those semantics to current state. Compilation dependencies do not authenticate separately deployed modules.

Successor asset transfers, registry replacement and component retirement do not by themselves change deployed code. The reviewed vault/FeeSplitter ABIs named migration operations, and auction ABIs named supply-controller operations; names alone establish neither behavior nor privileges. Thus the [whitepaper's non-upgradeability claim](https://www.standardreserve.xyz/whitepaper/#immutables) is not a guarantee that holdings, routing or control cannot change. Bind audit claims to the exact revision, scope and deployment, not a publisher “security reviewed” statement.

## Additional publisher-ABI research coverage

[Source records](../assets/sources.json), the [complete reviewed inventory](interface-inventory.md) and [role coverage gaps](interface-inventory-infrastructure.md) supply dated interface evidence, not a menu of permitted calls. Registry/liquidity/POL/incentives roles have only selective control declarations in this module; PoolManager has no bound ABI. Unknown broader interfaces are not claims of unavailable deployed capabilities. For treasury questions, distinguish current from queued fee routing, accrued liabilities from holder entitlements, selected-asset holdings from a complete portfolio, and retained POL acquisitions from Contraction Vault burns. Authenticate asset identity/decimals separately. For policy questions, pending settings are not active and raw counters do not establish accrual semantics.

## Questions and independent dimensions

Answer the requested identity or observation first, with the full address when relevant and concise source/block/time anchors. Do not reconstruct runtime facts from the conceptual system map or installed policy parameters. Fresh public evidence may establish an unlisted contract or interface without modifying this skill or matching a bundled catalog.
