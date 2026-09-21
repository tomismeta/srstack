# Read-only research workflow

For live status, identity and observational accounting. Design explanations need only the topic and cited records; [inspection](inspection.md) defines public state, price and gross-value observations. Apply [safety](safety.md) before external requests. Procedures use existing host tools, not invented APIs.

For per-round auction purchases, quantities, weighted prices or sellout timing, go directly to the [bounded history helper and evidence rules](auction-history.md). `snapshot.py auctions` remains current-state inspection, not a historical reader.

Catalogs seed research; they do not limit which public contracts or methods may be inspected. If a flow getter, event or target is absent from the snapshot catalog, follow [supplemental public reads](inspection.md#supplemental-public-reads) rather than refusing or waiting for a package update. Keep fresh evidence separate from packaged coverage. For historical flow claims, establish the getter's reset/settlement window and the claimed interval; current-plus-previous flow is not two completed epochs.

## 1. Define scope and evidence

Identify entity/generation, network, metric, denomination, owner/beneficiary, interval and historical/current scope. Derive available inputs from evidence; ask only for missing user-dependent definitions. Total is not circulating supply; treasury value is not spendable income; policy allocation is not payment.

Follow direct relevant topic/record paths. Load [contracts](contracts.md) and [entity index](../assets/entity-index.json) for identity, [source index](../assets/sources.json) only for unknown record locations, and [parameter index](../assets/parameters.json) for publisher-design values—not live state. Unknown values stay unknown, not calculator defaults or conventions.

Offline answers can explain packaged identities, interfaces and published rules, not changing state. Dynamic claims require fresh evidence: UTC retrieval, original URL/provider, source timestamp and freshness limits. Distinguish publication, claimed event, retrieval and chain observation times; a freshly retrieved page can describe an old proposal. If retrieval is unavailable, report the requested result as unavailable—never fall back to a saved observation.

For routine current STANDARD price or gross amount/charter value, prefer the [inspection fast path](inspection.md#common-question-paths): `price.py`, and a fresh `charter` snapshot first only if a charter's accrued balance is needed. Ask only for missing scope. A known charter ID needs no unrelated address scan; a request about a public address may use bounded ownership, balance and event discovery to identify its public charters or holdings, without connecting a wallet or claiming the user owns that address. The current-value question authorizes necessary public reads under host permissions, not forecasts or an unrelated refresh.

## 2. Authenticate and discover

1. Establish network and identifier from publisher evidence suited to the role, then explorer/chain relationships. Names, tickers, logos, searches and unsolicited addresses are leads. Missing packaged identity does not prove no deployment.
2. Call `eth_chainId` and `eth_getBlockByNumber`; retain chain ID, block number/hash/time. Pin state to that block. Use supported hash selectors or recheck hashes when reorganizations matter; never assume finality.
3. Check `eth_getCode` there. Presence proves neither role, activation, ownership nor safety. Use either evidenced source correspondence or the reviewed publisher-authenticated ABI read path in [inspection](inspection.md), with fixed targets, explicit read-only mutability/types/scales, strict decoding and matching required bindings. Publisher ABI reads do not establish source equivalence. No borrowed cross-chain ABI, guessed slots/interfaces or selector-only authentication.
4. Discover resources through authenticated registries, factories, ownership, enumeration or decoded events. Re-read survivors; include relevant creations, closures, migrations and transfers, not just indexed records. Authenticate discovered relationships; current ownership differs from interval ownership. Discoveries belong in the answer, not rewritten catalogs.

Ambiguous chain, role, ABI or generation stops the affected conclusion. Report the missing link; do not probe guessed identities/interfaces.

## 3. Retrieve finite public observations

Choose already permitted sources by required capabilities, not directory order. Current state, historical logs and historical state are separate capabilities; a current call proves no archive support.

Bound interval, addresses/topics, pages, resources, batch sizes and retries to the question/provider. Only authenticated ABI `view`/`pure` reads, including every batch member. Resolve “latest” to a recorded block. Quotes need exact base/quote assets, venue/methodology, time and executable versus indicative/aggregated status.

For canonical-pool STANDARD pricing, prefer `price.py`: DEX Screener by default, labelled GeckoTerminal fallback only for availability failures, or an explicitly selected provider. The helper does not automatically fall back after access denial, invalid data or identity mismatch; its optional cross-check reads the other provider only when requested. These are helper limits, not a ban on supplemental public price research. Other relevant public providers, market discovery and chain-based quotes may be researched under [supplemental-read rules](inspection.md#supplemental-public-reads), with explicit asset/pool identities, units, methodology and source selection. Keep each source's results separate; never silently repair failed helper output with another source. The bundled APIs provide retrieval times but no price-observation timestamp or independent freshness/block assurance. Keep their `price_observed_at: null`; HTTP Date, cache age, pool/pair creation, image, trade and candle times cannot substitute. RPC blocks and API retrievals are different clocks, not atomic observations. Disclose source changes, material disagreements and failures; agreement is no independent-truth guarantee.

Fetch finite authenticated log windows. Keep block hash, transaction hash and log index; deduplicate overlaps and handle removed/reorganized logs. Check pagination, truncation, provider limits and coverage; never skip failed windows silently. Opening balances/entitlements may require pre-interval history.

Keep raw amounts, authenticated decimals, requested/observed anchors and limits; symbols do not establish scale. Failed decoding, unavailable methods/history, rate limits, empty provider responses and incomplete enumeration are not zeros. Successful empty event queries prove no matches only within demonstrated filters/coverage.

## 4. Compute with explicit units

Use exact integer/rational arithmetic or documented decimal precision. Preserve raw scales; derive totals from common unrounded inputs and round for display. Conversions require explicit rates and valuation times. USD differs from stablecoin denomination; price freshness differs from state freshness.

Prefer `price.py`'s optional `standard_amount` for its supported current gross marks. Local arithmetic outside the helper is permitted using evidenced quantities and prices: preserve exact decimal/integer inputs, scales, units, source times and the formula; round only for presentation. Label supplemental calculations separately from helper output. Preserve requested USD or ETH units and report unavailable denominations rather than inventing conversions. Charter `charter_pending` is the whole charter's accrued STANDARD ledger balance, not wallet tokens; its mark is before withdrawal/trading costs, not net proceeds, charter resale or earning capacity. Do not automatically divide by branch count or apply a zero-amount fee preview as an amount-specific exit fee. See [units and financial interpretation](inspection.md#units-and-financial-interpretation); no implicit USD=ETH or 1 ETH conversion.

### Supply and holdings

Define minted, burned, total, circulating, escrowed, staked, reserve-held or beneficial supply. Evidence exclusions; do not double-count underlying assets via receipt/LP tokens. Read authenticated balance/supply semantics at one block. Event-derived totals require complete relevant history, initial allocations, rebases and migrations; otherwise report only measured scope.

Establish reserve ownership and liabilities/encumbrances. Gross value, redeemable value and net backing differ. Incomplete coverage means partial holdings, not a portfolio total.

### Flows, principal, income and fees

Define opening/closing anchors and event inclusion (for example opening end-of-block balance, then events through closing block). Per asset:

`closing = opening + classified inflows − classified outflows + evidenced non-transfer adjustments`

Separate external deposits/withdrawals, internal transfers, income, purchases/sales and adjustments. Internal transfers cancel only within the consolidation boundary; retain gross records. Appreciation is valuation, not cash income. Evidence rebases/accrual rather than force transfer-only reconciliation.

For LP/strategy earnings, discover positions/ownership throughout the interval; establish deposits, removals, collections, transfers, opening/closing accrued entitlements and authenticated accounting semantics. Collections/withdrawals may mix principal, fees and pre-interval income. Gross collections, swap volume and position-value changes are not earned fees. If independently evidenced, reconcile period fee accrual as fee-only collections + closing uncollected fees − opening uncollected fees, adjusted for transferred entitlements. Missing components prevent an established-income claim.

Separate gross fees, costs, net receipts, uncollected entitlements, allocations and actual distributions. [Reserves](reserves.md) and [charters](charters.md) explain policy; genesis and ongoing routing differ and neither proves execution. Authenticate recipient, eligible base, interval and units before recipient-flow reconciliation.

Investigate residuals from common raw inputs; call a discrepancy rounding only after demonstrating its bound. Observational accounting supports evidenced historical/current facts, not forecasts or numerical strategy comparisons. Keep attributed estimates distinct from observations without a mandatory opening warning.

## 5. Interpret, stop and report

Align entity/generation, definitions, anchors, coverage and methodology before comparisons. Attribute claims versus observations. Publisher design is not deployed behavior; bytecode and observed state stay block-scoped. Unresolved evidence leaves the affected conclusion not established; a mirror is not independent corroboration.

Stop affected conclusions for unauthenticated identity/ABI, missing history, stale/incomparable prices, malformed results, exhausted bounds, incomplete enumeration, conflicting anchors or arithmetic anomalies. Report supported partial coverage and unavailable conclusions; no credentials, paid accounts, broader permissions, unbounded indexing or simulation to bridge gaps.

Answer first with the requested fact or specific gap. Default to at most one short relevant note and one or two source links/time anchors when needed; for the fixed reader use “RPC snapshot; publisher ABI.” Keep raw inputs, hashes, exact locators, provenance and derivations in the session or answer for requested detail, not installed resources or observation-history files. Surface material conflicts and unknowns, not a boilerplate limitations list. Failure is not zero; narrow success is not a security audit or proof of launch, solvency or complete history.
