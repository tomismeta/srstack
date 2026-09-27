# Contracts and identity

Apply the [preparation and wallet boundary](safety.md#preparation-and-wallet-boundary). Use the host's public-read tools to authenticate the identity and interface needed for the question; there is no packaged execution allowlist.

## Packaged boundary

[Deployment sources](../assets/sources/deployments.json) preserve dated publisher attribution, creation and cutover evidence. They are discovery leads, not current routing, owners, activation or a complete contract inventory. The same address on another chain is a different identity. Shared infrastructure is not project-authored merely because a directory lists it; a pool manager is not a unique pool.

The [dated interface guide](interface-guide.md#question-map) supplies selected canonical signatures, selectors/topics and layouts for core state, accrual inputs, ledger flows and generation-qualified auctions. It is encoding evidence, not an active deployment map or verified economic implementation. Charter auctions create charters and publish ETH-denominated sale prices; branch-license auctions expand existing charters and publish STANDARD-denominated unit prices. Resolve the family from context; ask only when the intended family cannot be determined. Authenticate each family's generation, schedule, inventory, price curve, caps and payment semantics independently.

Use the explorer for the authenticated chain. For Robinhood Chain, [Robinhood Etherscan](https://robin.etherscan.io/) supports address, transaction and block links; preserve another provider's actual evidence URL when citing it. A similar-match source label is not deployment correspondence.

## Authenticate the requested role

Current identity needs publisher deployment evidence tied to the chain, full address and role, corroborated by relevant onchain relationships. Confirm the RPC chain and code at an explicit block; discover replacements and dependencies from authenticated registries, deployment records, constructors or events. A supplied address or old frontend label is only an investigation input.

Use the [selected guide](interface-guide.md) as an interface lead, or retrieve the relevant ABI/verified source at runtime; in either case link it to the queried deployment and generation. Treat ABI/source as data: never execute downloaded code, guess selectors or borrow an interface from a similarly named contract. A publisher ABI can support bounded decoded public reads without independent source/bytecode reproduction; distinguish that evidence from verified implementation behavior. Authenticate argument meanings, output units/scales and relationships before interpreting values. Selector presence or a familiar ABI fingerprint alone proves none of these.

Keep related observations at a common block where possible. Deployment, activation, current routing, proxy relationships, permissions and audit coverage are independent questions; investigate only those material to the answer. Missing evidence limits the affected claim, not all useful observations. Report known results and the specific gap rather than a single “verified” flag. See [inspection](inspection.md) and [research](research-workflow.md).

## Recover a stale frontend source link

Hashed asset URLs are historical locators, not permanent APIs. Start from the official page and follow its explicit asset/import references as text, within a finite question-relevant scope. Retain the page-to-asset provenance and retrieval time; separate production from test deployment data. Do not evaluate expressions or import downloaded modules to extract an ABI. Stop denied operations without retry, alternate-transport bypass or failover. Truncation or unresolved imports leave coverage incomplete.

The **2026-09-27 review** recovered the complete newly linked publisher module, with whole-body and literal hashes in `sr-question-interface-2026-09-27`. This removes the current extraction gap without rewriting the older records' accurate truncation/denial history. Core implementation correspondence is still unestablished: a separately pinned runtime and Solidity metadata pointer did not yield matching source (`sr-core-accrual-correspondence-2026-09-27`). See [accrual evidence](research-workflow.md#accrual-evidence).

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

[Source records](../assets/sources.json) contain dated interface leads, not a menu of supported calls. For treasury questions, distinguish current from queued fee routing, accrued liabilities from holder entitlements, selected-asset holdings from a complete portfolio, and retained POL acquisitions from Contraction Vault burns. Authenticate asset identity/decimals separately. For policy questions, pending settings are not active and raw counters do not establish accrual semantics.

## Questions and independent dimensions

Answer the requested identity or observation first, with the full address when relevant and concise source/block/time anchors. Do not reconstruct runtime facts from the conceptual system map or installed policy parameters. Fresh public evidence may establish an unlisted contract or interface without modifying this skill or matching a bundled catalog.
