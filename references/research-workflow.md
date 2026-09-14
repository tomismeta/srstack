# Read-only research workflow

For live status, identity and observational accounting. Design explanations need only the topic and cited records; [inspection](inspection.md) defines a public snapshot and [planning](planning.md) hypothetical comparisons. Apply [safety](safety.md) before external requests. Procedures use existing host tools, not invented APIs.

## 1. Define scope and evidence

Identify entity/generation, network, metric, denomination, owner/beneficiary, interval and historical/current scope. Derive available inputs from evidence; ask only for missing user-dependent definitions. Total is not circulating supply; treasury value is not spendable income; policy allocation is not payment.

Follow direct relevant topic/record paths. Load [contracts](contracts.md) and [entity index](../assets/entity-index.json) for identity, [source index](../assets/sources.json) only for unknown record locations, and [parameter index](../assets/parameters.json) for publisher-design values—not live state. Unknown/redacted values stay unknown, not calculator defaults or conventions.

Offline answers stop at source retrieval/review boundaries. Current claims need fresh evidence: UTC retrieval, original URL/provider, source timestamp and freshness limits. Distinguish publication, claimed event, retrieval and chain observation times; a freshly retrieved page can describe an old proposal.

## 2. Authenticate and discover

1. Establish network and identifier from publisher evidence suited to the role, then explorer/chain relationships. Names, tickers, logos, searches and unsolicited addresses are leads. Missing packaged identity does not prove no deployment.
2. Call `eth_chainId` and `eth_getBlockByNumber`; retain chain ID, block number/hash/time. Pin state to that block. Use supported hash selectors or recheck hashes when reorganizations matter; never assume finality.
3. Check `eth_getCode` there. Presence proves neither role, activation, ownership nor safety. Authenticate ABI/version and implementation; resolve proxies through evidence, not guessed slots/selectors/events/interfaces.
4. Discover resources through authenticated registries, factories, ownership, enumeration or decoded events. Re-read survivors; include relevant creations, closures, migrations and transfers, not just indexed records. Authenticate discovered relationships; current ownership differs from interval ownership. Discoveries belong in the answer, not rewritten catalogs.

Ambiguous chain, role, ABI or generation stops the affected conclusion. Report the missing link; do not probe guessed identities/interfaces.

## 3. Retrieve finite public observations

Choose already permitted sources by required capabilities, not directory order. Current state, historical logs and historical state are separate capabilities; a current call proves no archive support.

Bound interval, addresses/topics, pages, resources, batch sizes and retries to the question/provider. Only authenticated ABI `view`/`pure` reads, including every batch member. Resolve “latest” to a recorded block. Quotes need exact base/quote assets, venue/methodology, time and executable versus indicative/aggregated status.

Fetch finite authenticated log windows. Keep block hash, transaction hash and log index; deduplicate overlaps and handle removed/reorganized logs. Check pagination, truncation, provider limits and coverage; never skip failed windows silently. Opening balances/entitlements may require pre-interval history.

Keep raw amounts, authenticated decimals, requested/observed anchors and limits; symbols do not establish scale. Failed decoding, unavailable methods/history, rate limits, empty provider responses and incomplete enumeration are not zeros. Successful empty event queries prove no matches only within demonstrated filters/coverage.

## 4. Compute with explicit units

Use exact integer/rational arithmetic or documented decimal precision. Preserve raw scales; derive totals from common unrounded inputs and round for display. Conversions require explicit rates and valuation times. USD differs from stablecoin denomination; price freshness differs from state freshness.

### Supply and holdings

Define minted, burned, total, circulating, escrowed, staked, reserve-held or beneficial supply. Evidence exclusions; do not double-count underlying assets via receipt/LP tokens. Read authenticated balance/supply semantics at one block. Event-derived totals require complete relevant history, initial allocations, rebases and migrations; otherwise report only measured scope.

Establish reserve ownership and liabilities/encumbrances. Gross value, redeemable value and net backing differ. Incomplete coverage means partial holdings, not a portfolio total.

### Flows, principal, income and fees

Define opening/closing anchors and event inclusion (for example opening end-of-block balance, then events through closing block). Per asset:

`closing = opening + classified inflows − classified outflows + evidenced non-transfer adjustments`

Separate external deposits/withdrawals, internal transfers, income, purchases/sales and adjustments. Internal transfers cancel only within the consolidation boundary; retain gross records. Appreciation is valuation, not cash income. Evidence rebases/accrual rather than force transfer-only reconciliation.

For LP/strategy earnings, discover positions/ownership throughout the interval; establish deposits, removals, collections, transfers, opening/closing accrued entitlements and authenticated accounting semantics. Collections/withdrawals may mix principal, fees and pre-interval income. Gross collections, swap volume and position-value changes are not earned fees. If independently evidenced, reconcile period fee accrual as fee-only collections + closing uncollected fees − opening uncollected fees, adjusted for transferred entitlements. Missing components prevent an established-income claim.

Separate gross fees, costs, net receipts, uncollected entitlements, allocations and actual distributions. [Reserves](reserves.md) and [charters](charters.md) explain policy; genesis and ongoing routing differ and neither proves execution. Authenticate recipient, eligible base, interval and units before recipient-flow reconciliation.

Investigate residuals from common raw inputs; call a discrepancy rounding only after demonstrating its bound. Observational accounting is not scenario planning. Both planner modes require the visible first warning; no-conflict checks establish only partial agreement with packaged statements. Never present scenarios as observations.

## 5. Interpret, stop and report

Align entity/generation, definitions, anchors, coverage and methodology before comparisons. Attribute claims versus observations. Announcements may revise intended terms without changing deployed code; history/bytecode stays block-scoped. Preserve disagreement; newest is not automatically authoritative and a mirror is not corroboration.

Stop affected conclusions for unauthenticated identity/ABI, missing history, stale/incomparable prices, malformed results, exhausted bounds, incomplete enumeration, conflicting anchors or arithmetic anomalies. Report supported partial coverage and unavailable conclusions; no credentials, paid accounts, broader permissions, unbounded indexing or simulation to bridge gaps.

Report **answer; scope/units; snapshot/chain anchors; original source URLs/IDs and locators; raw inputs or reproducible derivation; coverage/conflicts; unresolved conclusion**. Failure is not zero; narrow success is not a security audit or proof of launch, solvency or complete history.
