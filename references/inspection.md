# Inspect: public state, price and gross value

Answer the requested public metric at an identified boundary. Use packaged `scripts/snapshot.py` for bounded fixed-target Robinhood RPC state and `scripts/price.py` for the canonical-pool STANDARD quote and optional gross amount valuation. Neither is a general live backend. Read [safety](safety.md) and [execution](execution.md) before use; load [contracts](contracts.md) for identity gaps and [research workflow](research-workflow.md) for historical discovery or accounting—not every reference by default.

Use only existing permitted public readers, clean unauthenticated browser rendering when needed, explorers/APIs and read-only chain facilities. The helpers supply fixed public RPC/API targets, not archive support, arbitrary market discovery or position enumeration. No installation, credentials, wallet access, downloaded-code execution, transaction preparation, token purchases, state-changing simulation or tracing workaround. Public addresses do not authorize discovery of private account data or other user addresses. No watchers, schedules or alerts; later inspection needs a new bounded request. Missing capabilities produce a concise gap, not fabricated results or broader access.

## 1. Scope only the requested observation

Establish entity/generation, network/environment, full public target and any charter identifier/ownership or beneficiary relationship; metric and exact unit; current snapshot or bounded historical interval/block; coverage (one charter is not every owner position); and valuation/quote asset if requested. Ask only for user-dependent scope absent from evidence.

Wallet tokens differ from issuance credits; charter counts differ from branch counts. Topic-linked source records describe packaged evidence, not current chain state. Use [source index](../assets/sources.json) only to locate an unknown source ID; [parameter index](../assets/parameters.json) only to locate a documented design parameter. No example-derived identity or economics. Current requests warrant fresh bounded reads, not rewritten catalogs or automatic source refresh outside scope.

### Common question paths

| Requested answer | Minimal existing path | Answer fields and limit |
|---|---|---|
| Permanent supply removed now, split into token burns and ledger retirement | One `protocol` snapshot | `token_burned_forever`, `token_ledger_retired`, derived `permanent_removed`; cumulative cap reduction, not buybacks today |
| Holding cap or Pool Manager gate active now | One `protocol` snapshot | `launch_holding_cap`, enabled/active flags, gate flag and `launch_schedule_active`; no transaction-success guarantee |
| Current Hook owner and pending handoff | One `protocol` snapshot | `trading_hook_owner`, `hook_pending_owner`; zero pending address means no pending recipient, not a history of completed transfers |
| “Show charter 1” / broad public-charter overview, or explicitly combined accrual/burn/restriction questions | One `charter` snapshot | Charter branches/accrued ledger balance plus clearly labelled protocol-wide permanent removal and cap/gate context; ask only for a missing public charter ID, not a wallet |
| Current epoch/stream context | One `protocol` snapshot | Epoch start/end, emissions status and stream rate; do not infer settlement completion or promise uninterrupted accrual |

These are routes through existing views, not new workflows or helper inputs. Use `detail: "summary"` unless raw evidence is requested. For a combined charter question covered above, do not also fetch `protocol`; return all requested supported fields from its one block anchor. Add `price.py` only when a price or monetary valuation is requested, not for STANDARD-denominated amounts.

For a broad “show/inspect charter N” request, default to a compact overview: charter ID, branch count, accrued STANDARD and available current-stream daily equivalent; then protocol-wide permanent removal (token burns versus ledger retirement) and holding-cap enabled/active plus Pool Manager gate status. These fields are already in the one charter snapshot. Keep protocol-wide figures distinct from that charter's balance and label daily extrapolation as non-guaranteed. Report unavailable requested fields without replacing them with zero. Narrow requests such as “only its balance” stay narrow; do not add prices, ownership research or a second snapshot unless requested.

For explanation-only questions, read [supply/epoch policy](protocol-policy.md), [launch restrictions](launch-trading.md#enabled-versus-active-restrictions) or [migration/upgrade distinctions](contracts.md#source-reviewed-mechanics-versus-publisher-abi-leads), without helper execution or an unrelated source refresh. Cumulative burn getters cannot answer daily buyback attribution; use the bounded [accounting research path](research-workflow.md) or state the missing historical evidence. A current snapshot is not a substitute for that history.

**Fast routes:** “inspect price” or “current STANDARD price” → `price.py` with `{"schema_version":1}`. “What is this STANDARD amount worth now?” → the same helper with `standard_amount` as an unsigned plain decimal string. “What is my charter worth?” → ask only for a missing public charter ID, never a wallet or wallet scan; read that charter's fresh `charter_pending`, then pass its normalized STANDARD amount to `price.py`. A current-price/value request already authorizes these needed fresh reads under existing host permissions; do not ask a redundant price-read permission question. Preserve requested USD/ETH units; unavailable denominations are not zero or an invitation to substitute another currency.

“Cross-check the current STANDARD price” adds `"cross_check":true`; “Use GeckoTerminal for the current STANDARD price” adds `"source":"geckoterminal"`. `"source":"dexscreener"` explicitly selects DEX Screener; the default `"auto"` uses DEX Screener with the bounded availability fallback below. Do not cross-check by default or accept arbitrary provider URLs.

The no-stdin equivalents are `price.py --quote`, `price.py --amount-standard DECIMAL`, and optional `--source auto|dexscreener|geckoterminal` or `--cross-check`. `--quote` and `--amount-standard` conflict; use the amount form for valuation. No flags retains JSON stdin. For a charter USD question, use one charter snapshot and one amount-valuing price invocation; report `valuation.gross_usd` only if available. A diagnostic `verify.py --charter ID --price` exercises that path but emits statuses/timings rather than the financial answer.

Charter pending balances are charter-level accrued ledger quantities, not wallet token holdings. Describe the resulting mark as **gross indicative accrued-balance value** before withdrawal and trading costs, not net proceeds, charter/NFT resale value or earning capacity. Never automatically divide it by branch count. If the pending read fails, report the amount/value gap; do not value zero, an example or a stored balance. A zero-amount withdrawal-fee preview is not an amount-specific net-withdrawal calculation.

## 2. Authenticate before ABI reads

The [entity index](../assets/entity-index.json) routes the publisher-listed Robinhood addresses. Explorer publication checks and the publisher frontend ABI are separate evidence: missing explorer source does not prohibit the limited read path below, and a Similar Match infrastructure ABI does not authenticate protocol modules. `sr-publisher-read-interface` records the publisher ABI's origin and limits; it is not independently verified source/bytecode correspondence.

1. Establish original publisher attribution, chain/environment, generation and role. Retain source URLs and times internally.
2. Before helper execution, verify the script and the fixed entity/interface catalog hashes against the trusted installed root/manifest as described in [execution](execution.md).
3. Confirm `eth_chainId`; select an explicit block and retain its number, hash, timestamp and UTC retrieval. Pin code, bindings and state to that boundary and recheck it for consistency. Do not assume finality.
4. Require code at each selected target and an authenticated interface: either established source/bytecode correspondence or the reviewed publisher-authenticated fixed ABI. The latter requires fixed targets, explicit `view`/`pure` mutability, known argument/return types and scales, strict decoding and required module-binding getters matching expected catalog addresses. A selector in bytecode alone proves neither ABI semantics nor source equivalence. Do not borrow another chain's ABI or guess proxy slots/interfaces.
5. Run the selected role's required binding getters even when their `profiles` lists are empty. A failed/mismatched binding suppresses that role, not an invented replacement address. Other valid roles may remain partial observations.
6. Read only the requested public charter ID; owner/branch/pending results are block-scoped observations, not authentication of the user or all their positions. Missing identity, interface, scale or required relationship stops the affected conclusion.

Keep attribution, source correspondence, observed owner/configuration, activation and audit coverage separate. Owner getters do not prove complete privilege structure, immutability or future settings.

## 3. Read the scoped state

Choose `protocol`, `charter` or `auctions` through schema-1 JSON stdin or explicit CLI mode: `snapshot.py protocol`, `snapshot.py auctions`, or `snapshot.py charter --id UINT256`. Stdin `charter` requires integer `charter_id`; CLI requires the unsigned public ID. `detail` / `--detail` defaults to `summary`; `full` adds raw responses/call mapping. Explicit CLI mode never reads stdin. See [the exact CLI contract](execution.md#snapshot-helper). Neither caller-selected addresses/selectors nor arbitrary endpoints/headers are accepted.

Use authenticated ABI `view`/`pure` `eth_call` at the identified block; wrappers and all nested/batched members must qualify. No mutating call merely because it will not broadcast; economic labels do not establish an ABI.

Bound addresses/topics, pages, resources, intervals, batches and retries. Discover through authenticated relationships; known positions are not a census. Historical `eth_getLogs` needs demonstrated coverage; current access proves neither history nor archive capability. Pin compatible reads to a common block, document exceptions and handle reorganizations per research workflow.

Retain raw values, authenticated decimals, units, derivations and anchors. Unknown semantics/scales block normalized quantities. Failed reads, redactions, missing history, unsupported methods, empty provider responses and incomplete enumeration are not zero. Displayed estimates remain attributed estimates. Balance changes are not income without flow accounting.

Collect only useful fields: possibly charter ID, owner/beneficiary, branches, issuance credits and evidenced lifecycle state. Derived branch counts/global budget need compatible authenticated observations and explicit accounting. Partial reserve holdings are not a portfolio total or solvency finding.

### Units and financial interpretation

| Observation | Meaning and boundary |
|---|---|
| Amounts and prices | Preserve authenticated raw scales and normalized units. STANDARD ledger credits are not wallet tokens; branch counts are integers. `ETH/STANDARD` and `USD/STANDARD` are different prices, never interchangeable. No implicit USD=ETH, 1 ETH or stablecoin=USD conversion; unavailable denominations remain unavailable. |
| `charter_branches`, `charter_pending`, `charter_owner` | State for the requested public charter ID, not proof that the user owns it or a census of their positions. Pending is the whole charter's accrued ledger amount, not per-branch earnings or acquisition cost. A failed read is not a zero balance. |
| `total_branches` | Global branch count, including the selected charter if it exists in that snapshot. Subtract `charter_branches` only for an existing included charter with compatible same-block readings; never subtract a hypothetical new position. One observation supplies no growth rate. |
| `base_issuance_per_day`, `multiplier`, `stream_rate_per_second` | Base issuance is unscaled STANDARD/day. Policy scaling applies the multiplier once, not again to an already-scaled rate. The stream rate includes recycling and is not a substitute for base issuance. Emissions status and owner-configured values describe the observation, not guaranteed future issuance. A daily-equivalent stream amount is not a forecast. |
| `remaining_gross_budget` | Counter-based `ISSUANCE_BUDGET() - cumulativeIssued()` using the publisher's mapping, requiring successful compatible readings and a nonnegative difference. It does not establish that every pending/unsettled accrual is included. Original issuance budget, outstanding credits, permanent cap reduction and `maxSupply - totalSupply` are different quantities. |
| Auction observations | Availability requires start, pause and inventory evidence. Inactive, paused, sold-out or unknown status means no purchasable quote—not a free license. A last sale is historical; a current auction or whitelist price does not establish an existing position's acquisition cost. Founding entry is outside this reader. |
| `buy_tax_percent`, `sell_tax_percent` | `currentTaxBps(true)` and `currentTaxBps(false)`, respectively, with basis points divided by 100 for percent. These are current directional tax observations, not future rates or net sale proceeds. LP fees, slippage, gas, tax basis/order and liquidity remain separate; do not double-count a source-described charge. `pool_initialized` is neither a market quote nor a liquidity guarantee. |
| `zero_amount_withdrawal_fee_percent` | A zero-amount preview, not an amount-specific withdrawal quote or fixed future resolution fee. It does not establish commitment timing, settlement ordering or available liquidity. Missing pressure, timing or availability is not zero. |

Addresses and configuration getters supply neither transaction gas usage nor executable acquisition, withdrawal or sale amounts. These interpretations support bounded observations only; no new calculator, transaction simulation or economic defaults follow from them.

### Supply, restrictions and control context

The `protocol` and `charter` profiles include these additive observations. They retain the same block-scoped evidence and failure rules; they are context, not permission to act.

| Fields | Meaning and boundary |
|---|---|
| `token_burned_forever`, `token_ledger_retired` | STANDARD quantities with 18 decimals: permanent token burns and permanent ledger retirement, respectively. `permanent_removed = token_hard_cap - token_max_supply` is their combined cap reduction, not a buyback total. |
| `launch_holding_cap` | STANDARD quantity with 18 decimals. A configured cap does not establish whether it applies now or whether a particular transfer would succeed. |
| `launch_holding_cap_enabled`, `launch_holding_cap_active` | Separate boolean observations: administrative enablement versus the source-defined effective launch-cap condition. Do not substitute one for the other. |
| `pool_manager_gate_enabled` | Boolean PoolManager transfer-gate setting, not a complete transferability or trading-availability verdict. |
| `standard_registry`, `standard_pool_manager` | Observed addresses, not checked catalog bindings, additional callable roles or authorization to follow arbitrary targets. A successful read does not establish that either address matches the publisher-listed identity. |
| `launch_schedule_active` | Hook boolean launch-schedule condition, distinct from effective tax rates and token cap enablement. |
| `hook_pending_owner` | Proposed two-step ownership recipient; `trading_hook_owner` remains the current owner. A nonzero pending owner is not a completed handoff. |

If Hook code or its required bindings are unavailable, the charter view is partial: omit the affected Hook fields, retain independently valid charter and token observations, and report the relevant gaps. Do not turn a missing Hook observation into a failed charter balance or an inferred false flag.

The reviewed [`Standard.sol` source](https://sourcify.dev/server/v2/contract/4663/0x88ad8DdF1E3898412146a534538d418c6F8A9062?fields=sources,abi) defines `maxSupply = HARD_CAP - burnedForever - ledgerRetired`. `burn`/`burnFrom` reduce liquid supply and the ceiling; CentralBank-only `convertFrom` burns liquid tokens without lowering the ceiling, while CentralBank-only `retire` lowers the ceiling without moving token balances. Thus transfer-to-zero event sums are not permanent burns, and `maxSupply - totalSupply` is arithmetic ceiling headroom, not remaining issuance budget or freely mintable supply. Getter totals do not attribute removals to buybacks, LP taxes or voluntary burns. Token source mechanics do not verify the separate CentralBank's call paths, ledger obligations or settlement behavior.

In that source, launch-cap activity requires enablement plus a nonzero Registry TAX_HOOK whose `launchScheduleActive()` is true. The cap check runs on transfers **from PoolManager**, checking recipient balance and specified protocol exemptions; do not infer that every LP withdrawal, router or intermediate custodian is exempt, or that every transfer is capped. Ordinary wallet transfers and mints do not enter that branch. The PoolManager gate uses Hook-authorized transient transfer budgets and is separate from the destination blocklist. Disabling it does not disable the blocklist or tax Hook. The blocklist restricts transfers **into** blocked venues, not symmetrically out of them. The reader accepts no address-blocklist input and does not enumerate blocked venues or expose transient budgets as lasting allowances.

The reviewed [`TaxHook.sol` source](https://sourcify.dev/server/v2/contract/4663/0xF1eE073811B14359D850825E48d200483200eDcd?fields=sources,abi) makes the launch schedule active before pool initialization unless overridden, and inactive after its duration or permanent override. That condition gates non-POL liquidity additions; a tax-floor observation alone is not a substitute. Token restriction setters consult `CentralBank.owner()` in the reviewed token source; this does not prove complete CentralBank or Registry authority. These are source-reviewed semantics, not saved deployment-verification verdicts, current switch states or guarantees of transaction success. Re-establish requested deployment correspondence separately; a dependency bundled with these sources does not verify its own deployed module.

For epoch context, retain `epoch_start`, `epoch_end`, emissions status and stream rate together. The publisher's [current-conditions explanation](https://www.standardreserve.xyz/app/protocol/live/) says accrual stops at epoch end until rollover. Passing the boundary does not establish that settlement occurred; the helper does not derive a settlement-pending verdict, execute rollover or verify CentralBank settlement implementation. A daily-equivalent stream extrapolation is not a promise of uninterrupted accrual.

## 4. Anchor any price separately

Use `price.py` for current STANDARD prices and current gross amount/charter marks. It reads only the fixed canonical pool from the [Robinhood catalog](../assets/entities/robinhood.json), using DEX Screener (`dexscreener-api`) by default and a labelled GeckoTerminal (`geckoterminal-api`) fallback for availability failures only. Explicit provider selection disables automatic switching; an optional requested cross-check observes the other provider separately. There is no search, token-pair discovery or legacy-pair-alias fallback. See the [exact price contract](execution.md#price-helper). Use its `standard_amount` valuation rather than ad hoc calculator multiplication: a single selected-provider response supplies both quote denominations and gross arithmetic. Never average sources, choose the higher quote or fill a missing denomination from the cross-check.

Record exact base/quote identities and units, selected provider, indicative status, API retrieval time and requested amount. Both providers report indicative evidence with no independent freshness or block assurance. Each successful provider observation has its own `retrieved_at`; `price_observed_at` is unknown (`null`). HTTP Date, cache age, pool/pair creation, image, trade and candle timestamps are not quote times. A fresh API retrieval does not establish when the price was observed. Charter RPC block time and price API retrieval are different clocks; never describe their combined value or a cross-check as atomic or same-block. Cross-check agreement is not an independent-truth guarantee; GeckoTerminal and CoinGecko are the same provider family.

No invented markets, unrelated-token quotes, unqualified stablecoin=USD assumptions, guaranteed liquidity or executable proceeds. Missing/invalid denominations are omitted with errors; a usable partial primary result stays selected. Show usable partial results in their actual units and explain unavailable requested values. If no usable quote remains, report token/ledger quantities without unsupported monetary value. Never use zero or cached observations to conceal failure. Automatic fallback is limited to availability/transient failures, never host permission denial, HTTP 401/403, malformed/oversized data or identity mismatch. Disclose `fallback`, its reason and `errors.primary_source`; a fallback result is partial. For requested cross-checks show material `disagreement_percent` differences and secondary failures without changing the selected quote or valuation.

Daily auction `currentPrice()` is only a returned curve value until start/pause/inventory observations support availability. It can keep decaying after sellout. `snapshot.py` omits normalized current prices when inactive, paused, sold out or status is unknown, while full evidence may retain raw getters; those are not purchasable quotes. `lastSalePrice()` is historical; derived closing price requires a last-sale day matching the current sold-out day. Auction observations are separate from `price.py`'s STANDARD market quote, and neither guarantees that a purchase would succeed.

## 5. Report observations and gaps

Lead with the requested values and units, or the specific unavailable answer. Prefer a few lines or one small table; do not repeat the same numbers in both. Add at most one short material note, such as **“RPC snapshot; publisher ABI.”**, and a short observation time when needed. Block numbers, hashes and long traces are opt-in. Expose partial failures briefly; do not label valid observations hypothetical.

Keep full addresses, raw amounts/scales, requested/observed chain and block number/hash/time, provider/retrieval, source IDs/locators, call mapping, derivations and per-field provenance internally or in requested full output. No mandatory trace dump. Narrow success establishes neither source equivalence, security, solvency, complete activity nor future issuance; missing reads/searches are not zero or universal absence.

Each `snapshot.py` invocation has its own block anchor. Separate protocol/auction/charter invocations may use different blocks; never describe them as atomic unless returned anchors actually match. `price.py` has API retrieval evidence, no chain block or known quote-observation timestamp, so a combined state/price answer is never a same-block snapshot. Retain the separate anchors internally and mention timing differences when material.

## 6. Research and inspection only

A current-state question authorizes its relevant bounded read under existing host permissions, not a blanket refresh, persistence or financial action. Explain documented mechanisms and qualitative tradeoffs when useful; do not collect assumptions for strategy comparisons or produce forecasts, settlement simulations, future cash flows or liquidity-return simulations. Current prices, stream rates, taxes and published bounds do not establish future behavior.

The [Second Mandate](updates.md#second-mandate-liquidity-for-tokenized-stocks) is announced strategy, not deployed-state or return evidence. Its sample reserve positions, APY boost and returned-fee figures cannot establish income or holder revenue rights. Use [research workflow](research-workflow.md) for bounded historical accounting; unsupported conclusions remain gaps rather than hypothetical numerical substitutes.
