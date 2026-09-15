# Inspect: public state, price and gross value

Answer the requested public metric at an identified boundary. Use packaged `scripts/snapshot.py` for bounded fixed-target Robinhood RPC state and shared `scripts/price.py` for the canonical-pool STANDARD quote and optional gross amount valuation. Neither is a general live backend. Read [safety](safety.md) and [execution](planning-execution.md) before use; load [contracts](contracts.md) for identity gaps and [research workflow](research-workflow.md) for historical discovery or accounting—not every reference by default.

Use only existing permitted public readers, clean unauthenticated browser rendering when needed, explorers/APIs and read-only chain facilities. The helpers supply fixed public RPC/API targets, not archive support, arbitrary market discovery or position enumeration. No installation, credentials, wallet access, downloaded-code execution, transaction preparation, token purchases, state-changing simulation or tracing workaround. Public addresses do not authorize discovery of private account data or other user addresses. No watchers, schedules or alerts; later inspection needs a new bounded request. Missing capabilities produce a concise gap, not fabricated results or broader access.

## 1. Scope only the requested observation

Establish entity/generation, network/environment, full public target and any charter identifier/ownership or beneficiary relationship; metric and exact unit; current snapshot or bounded historical interval/block; coverage (one charter is not every owner position); and valuation/quote asset if requested. Ask only for user-dependent scope absent from evidence.

Wallet tokens differ from issuance credits; charter counts differ from branch counts. Topic-linked source records describe packaged evidence, not current chain state. Use [source index](../assets/sources.json) only to locate an unknown source ID; [parameter index](../assets/parameters.json) only to locate a documented design parameter. No example-derived identity or economics. Current requests warrant fresh bounded reads, not rewritten catalogs or automatic source refresh outside scope.

**Fast routes:** “inspect price” or “current STANDARD price” → `price.py` with `{"schema_version":1}`. “What is this STANDARD amount worth now?” → the same helper with `standard_amount` as an unsigned plain decimal string. “What is my charter worth?” → ask only for a missing public charter ID, never a wallet or wallet scan; read that charter's fresh `charter_pending`, then pass its normalized STANDARD amount to `price.py`. A current-price/value request already authorizes these needed fresh reads under existing host permissions; do not ask a redundant price-read permission question. Preserve requested USD/ETH units; unavailable denominations are not zero or an invitation to substitute another currency.

Charter pending balances are charter-level accrued ledger quantities, not wallet token holdings. Describe the resulting mark as **gross indicative accrued-balance value** before withdrawal and trading costs, not net proceeds, charter/NFT resale value or earning capacity. Never automatically divide it by branch count. If the pending read fails, report the amount/value gap; do not value zero, an example or a stored balance. A zero-amount withdrawal-fee preview is not an amount-specific net-withdrawal calculation.

## 2. Authenticate before ABI reads

The [entity index](../assets/entity-index.json) routes the publisher-listed Robinhood addresses. Explorer publication checks and the publisher frontend ABI are separate evidence: missing explorer source does not prohibit the limited read path below, and a Similar Match infrastructure ABI does not authenticate protocol modules. `sr-publisher-read-interface` records the publisher ABI's origin and limits; it is not independently verified source/bytecode correspondence.

1. Establish original publisher attribution, chain/environment, generation and role. Retain source URLs and times internally.
2. Before helper execution, verify the script and the fixed entity/interface catalog hashes against the trusted installed root/manifest as described in [execution](planning-execution.md).
3. Confirm `eth_chainId`; select an explicit block and retain its number, hash, timestamp and UTC retrieval. Pin code, bindings and state to that boundary and recheck it for consistency. Do not assume finality.
4. Require code at each selected target and an authenticated interface: either established source/bytecode correspondence or the reviewed publisher-authenticated fixed ABI. The latter requires fixed targets, explicit `view`/`pure` mutability, known argument/return types and scales, strict decoding and required module-binding getters matching expected catalog addresses. A selector in bytecode alone proves neither ABI semantics nor source equivalence. Do not borrow another chain's ABI or guess proxy slots/interfaces.
5. Run the selected role's required binding getters even when their `profiles` lists are empty. A failed/mismatched binding suppresses that role, not an invented replacement address. Other valid roles may remain partial observations.
6. Read only the requested public charter ID; owner/branch/pending results are block-scoped observations, not authentication of the user or all their positions. Missing identity, interface, scale or required relationship stops the affected conclusion.

Keep attribution, source correspondence, observed owner/configuration, activation and audit coverage separate. Owner getters do not prove complete privilege structure, immutability or future settings.

## 3. Read the scoped state

Choose `protocol`, `charter` or `auctions` through schema-1 JSON stdin; `charter` requires integer `charter_id`. `detail` defaults to `summary`; `full` adds raw responses/call mapping. See [the exact CLI contract](planning-execution.md#snapshot-helper). Neither caller-selected addresses/selectors nor arbitrary endpoints/headers are accepted.

Use authenticated ABI `view`/`pure` `eth_call` at the identified block; wrappers and all nested/batched members must qualify. No mutating call merely because it will not broadcast; planner fields do not establish an ABI.

Bound addresses/topics, pages, resources, intervals, batches and retries. Discover through authenticated relationships; known positions are not a census. Historical `eth_getLogs` needs demonstrated coverage; current access proves neither history nor archive capability. Pin compatible reads to a common block, document exceptions and handle reorganizations per research workflow.

Retain raw values, authenticated decimals, units, derivations and anchors. Unknown semantics/scales block normalized quantities. Failed reads, redactions, missing history, unsupported methods, empty provider responses and incomplete enumeration are not zero. Displayed estimates remain attributed estimates. Balance changes are not income without flow accounting.

Collect only useful fields: possibly charter ID, owner/beneficiary, branches, issuance credits and evidenced lifecycle state. External branches/global budget need separately authenticated observations/accounting; do not assume planner fields exist on chain. Partial reserve holdings are not a portfolio total or solvency finding.

## 4. Anchor any price separately

Use `price.py` for current STANDARD prices, current gross amount/charter marks and chosen current-price projection inputs. It reads only the fixed canonical pool from the [Robinhood catalog](../assets/entities/robinhood.json), using DEX Screener's direct pair endpoint (`dexscreener-api`), not search, token-pair discovery or the legacy pair alias. See the [exact price contract](planning-execution.md#price-helper). Use its `standard_amount` valuation rather than ad hoc model/calculator multiplication: one response supplies both the quote and gross arithmetic.

Record exact base/quote identities and units, provider, indicative status, API retrieval time and requested amount. DEX Screener is provider-reported evidence, with no independent freshness or block assurance. `price_observed_at` is unknown (`null`); HTTP Date, pair creation and image timestamps are not quote times. A fresh API retrieval does not establish when the price was observed. Charter RPC block time and price API retrieval are different clocks; never describe their combined value as atomic or same-block.

No invented markets, unrelated-token quotes, unqualified stablecoin=USD assumptions, guaranteed liquidity or executable proceeds. Missing/invalid denominations are omitted with errors; show usable partial results in their actual units and explain unavailable requested values. If no usable quote remains, report token/ledger quantities without unsupported monetary value. Never use zero, cached observations or a provider switch to conceal failure.

Daily auction `currentPrice()` is only a returned curve value until start/pause/inventory observations support availability. It can keep decaying after sellout. `snapshot.py` omits normalized current prices when inactive, paused, sold out or status is unknown, while full evidence may retain raw getters; those are not purchasable quotes. `lastSalePrice()` is historical; derived closing price requires a last-sale day matching the current sold-out day. Auction observations are separate from `price.py`'s STANDARD market quote, and neither guarantees that a purchase would succeed.

## 5. Report observations and gaps

Lead with the requested values and units, or the specific unavailable answer. Prefer a few lines or one small table; do not repeat the same numbers in both. Add at most one short material note, such as **“RPC snapshot; publisher ABI.”**, and a short observation time when needed. Block numbers, hashes and long traces are opt-in. Expose partial failures briefly; do not label valid observations hypothetical.

Keep full addresses, raw amounts/scales, requested/observed chain and block number/hash/time, provider/retrieval, source IDs/locators, call mapping, derivations and per-field provenance internally or in requested full output. No mandatory trace dump. Narrow success establishes neither source equivalence, security, solvency, complete activity nor future issuance; missing reads/searches are not zero or universal absence.

Each `snapshot.py` invocation has its own block anchor. Separate protocol/auction/charter invocations may use different blocks; never describe them as atomic unless returned anchors actually match. `price.py` has API retrieval evidence, no chain block or known quote-observation timestamp, so a combined state/price answer is never a same-block snapshot. Retain the separate anchors internally and mention timing differences when material.

## 6. Explicit planning handoff only

A research request does not silently authorize planning, persistence or financial action. A current-state question does authorize the relevant bounded read, not a blanket refresh. If planning is requested, follow [planning](planning.md), schema 1 and explicit `documented`/`stress` mode. Answer first: label calculated results as estimates and independently supported facts as observations; no mandatory opening disclaimer for intake or blocked handoffs.

The engine accepts economics, not addresses, ABI, wallet data, provenance objects or paths. If projection price choice is unspecified, offer **current, hypothetical, or both** before fetching prices. Chosen current prices use the same `price.py` without a redundant permission prompt; supplied prices win, and complete offline/fictional inputs do not fetch. Follow [unit mapping](planning-inputs.md#price-choice-and-unit-mapping): ETH/STANDARD can propose `initial_token_price_eth`; USD requires an approved explicit conversion, never an implicit 1 ETH. Keep provenance and conversion scopes outside strict JSON. Confirm imported initial conditions and the full economics, including future multipliers, held-constant prices/growth, availability, costs, gas, fees/taxes/slippage and funding feasibility. The engine remains offline; no observation establishes future flatness, live economics from a design parameter or fictional defaults.

Mode differs from exit mode. Documented conflicts block numbers; stress requires explicit choice and retains conflicts, computational bounds and valid fixed rules. Retain fresh conformance/evidence internally and show only material blockers or unresolved assumptions unless detail is requested. Cap matches do not authenticate positions; frontend ranges do not prove on-chain policy. Scenario `summary` defaults; full accounting/history are opt-in, with history requiring full. Engine acceptance confers no freshness or authenticity. Report execution/errors concisely, never missing output as zero. No saving, overwrite, blanket source refresh, monitoring or financial action is implied.
