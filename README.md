# srstack

**Standard Reserve research and live inspection for AI agents.**

Inspect charters, auctions, orderbooks, protocol state and bounded history, or explain and model the published mechanics. This is an independent [Agent Skill](https://agentskills.io/specification), not an official Standard Reserve product. See [safety](references/safety.md#preparation-and-wallet-boundary) for execution boundaries.

Agent-agnostic, including Muse, Hermes and OpenClaw. Live helpers depend on permitted Python, filesystem and network access; explanations can work offline.

**Contract reads first wherever they are the most direct reliable evidence**, across protocol state, charters/positions, ownership, balances, permissions, treasury, auctions and orderbooks. Use events for executions that getters do not establish, market sources for market quotes and documents for policy; explanation-only questions need no live RPC.

**Version 0.3.0 — unreleased.** Includes v1.2 auctions, bounded orderbook reads, charter activity inspection, newest-first history with observed-round early stopping, conditional next-opening previews and proxy-aware RPC. No sales plus an unavailable next-round floor yields no numerical opening. S-Bill launch/position support still requires authenticated evidence.

**Dogfood scope:** integrity, synthetic CLI checks, host routing and live reads are separate results. Report PASS / FAIL / BLOCKED only for exercised paths. A provider denial is not a failed install.

**Coverage:** current v1.2 auction targets, isolated historical generations, separate round/cap-window context, POL Buyback and Incentives Vault. Orderbook pages are raw IDs, not a price/quantity/owner census; explicit charter IDs enable bid detail. No live snapshots are bundled.

**v1.2 migration:** current auction reads now use the replacement deployments. Charter timing is `charter_auction_round_seconds` from `auctionPeriod()`, replacing `charter_auction_day_seconds`. History `--generation current` means v1.2 for both auction kinds; use `license --generation v1.1` for the previous license deployment. Charter history now reports address-qualified `charter_generations` rather than a single `auction_address`. Older round IDs are not carried into the new deployment.

Current charter output also uses `charter_auction_current_round`, `charter_auction_round_cap`, `charter_auction_round_floor` and `charter_auction_last_sale_round`; these replace the corresponding `current_day`, `day_cap`, `day_floor` and `last_sale_day` suffixes without aliases. Authentic ABI method names remain unchanged.

## What you can ask

| Question | What srstack provides |
|---|---|
| “How do charter withdrawals work?” | Branch retirement, credit release, fees and unresolved mechanics |
| “What are the current issuance rate and buy/sell taxes?” | Fresh block-scoped protocol observations, not stored launch values |
| “How much supply was permanently removed, and why?” | Separate liquid-token burns from retired ledger value; totals do not attribute individual burn causes |
| “Are launch holding limits or the Pool Manager gate active?” | Fresh enabled/active flags and cap values; not a guarantee that a transaction will succeed |
| “What’s the current branch auction status?” | One fresh `snapshot.py auctions` read using the cataloged current license deployment: getter-reported status, remaining branches and price with [round context and interpretation limits](references/auctions.md#current-branch-auction-status-getters-first); no contract rediscovery or history indexing |
| “What will the next license round open at, and when?” | [Conditional policy preview and derived schedule](references/auctions.md#next-license-opening-documented-policy-estimate) from the same fresh auction snapshot. No sales and an unavailable next-round floor means **unknown price**, not an estimate using today's floor. Scheduled timing is not keeper execution. |
| “Show each round's opening, first, average and last sale.” / “Last 3 rounds?” | `history.py license --generation current`: contract reads first, then targeted logs of at most 10 blocks. Returns observed opening/first/weighted-average/last prices. Add `--last-rounds 3` for newest-first early stopping, not full-round accounting. Equal-state skipped intervals remain unsearched. [Coverage](references/auction-history.md#question-to-window). |
| “Can I bid for branches at my chosen price?” | [v1.2 limit-order guidance](references/updates.md#protocol-v12-announced-changes): FCFS best-attempt keeper execution, not guaranteed allocation. Queued orders and purchases are separate evidence. |
| “What can you read from the orderbook?” | `snapshot.py orderbook --start 0 --count 20`: raw IDs only, **not a price/quantity/owner listing**. Optional `--charter-ids N,M` reads independently known charter bids/fillability; no automatic page-to-charter join. |
| “Have charter auctions started, and how often?” | Announced v1.2 launch and one-charter branch-auction cadence, separated from fresh activation/inventory/price observations and the older whitepaper's daily design. The announced 5.5 ETH first opening is not a saved current price. |
| “What are the current treasury shares and team liability?” | Current/queued FeeSplitter state and vault controls, not holder yield |
| “What does the vault hold of this public reserve asset?” | Approval-gated raw holdings/pool metadata for that asset, not portfolio enumeration |
| “How much did buybacks spend and burn in this block window?” | ContractionVault `BuybackExecuted` event totals within checked coverage; POL buybacks have a separate mode reporting raw token output and destination, not burns |
| “How are my branches doing?” | Public charter ID → branch count, accrued STANDARD and current-rate daily equivalent in one compact read. A supplied public address can be used for scoped charter discovery; no wallet connection. |
| “When was my charter active; do I need to check in?” | `snapshot.py charter --id N --detail activity`: authenticated owner/activity/transfer/period reads. Raw clocks are not a verified deadline, dormancy verdict or last-check-in timestamp. [Interpretation](references/exits.md#inspect-one-charters-activity). |
| “How are my S-Bills doing?” | Use supplied public position details or a user-consented export. Authenticate the actual position-read surface before live claims; preview samples and marketing rates are never reported as the user's holdings. |
| “What is STANDARD trading at, or what is this amount worth?” | Latest reported canonical-pool USD/ETH prices and a gross indicative valuation |
| “Which contracts are listed, and is their source verified?” | Publisher-listed identities and explorer links; verification status requires a fresh explorer check |
| “What has the team announced?” | Fresh official-post research where the host can retrieve it; no bundled recap |
| “What does the Second Mandate mean, and are its market positions real?” | Source-linked manifesto explanation; sample illustrations are not observed positions, revenue or yield offers |

One skill, useful starting routes:

- **Research:** source-linked explanations, documented parameters and evidence gaps.
- **Inspect:** current protocol/charter/auction state, bounded orderbook pages and history, prices.
- **Analyse:** conditional accrual/time-to-target estimates, auction/fee models, forecasts, comparisons and plans with explicit inputs and assumptions.
- **Workflows:** user-requested reports, exports and bounded automation under host permissions.

Common questions have [direct inspection paths](references/inspection.md#common-question-paths). Default charter JSON contains only charter facts and its supported rate equivalent; explicitly select `--detail full` when combined charter, burn or launch-restriction context is requested at one block. Explanation-only questions go straight to packaged sources without an RPC call or financial questionnaire. STANDARD amounts do not trigger a price lookup unless monetary valuation is requested.

The installed skill stores identities, reviewed interfaces and source provenance—not snapshots of current auction status, prices, balances or ownership. Each current-state question performs live reads. Historical cutover metadata identifies which deployed contracts to inspect; it is not a saved current-state answer.

Research topics: [protocol](references/protocol.md) · [charters](references/charters.md) · [reserves](references/reserves.md) · [contracts](references/contracts.md) · [updates](references/updates.md) · [documents](references/documents.md) · [risks](references/risks.md).

These are routing instructions within one skill, not separately installed commands. `Use srstack` returns the research / inspect / analyse / workflows menu. `/srstack` works where the host registers an installed skill command; other command syntax varies by host.

## Requirements

| Capability | Host requirements | Network access |
|---|---|---|
| Explain packaged rules | Read the skill and its selected resources | None |
| Research announcements or explorer status | Permitted public web retrieval | Relevant official pages or explorer |
| Inspect current state | Trusted package and permitted Python 3.10+ execution | Selected Robinhood Chain RPC; official public endpoint by default |
| Inspect auction history | Trusted package and permitted Python 3.10+ execution; bounded block scope | Selected Robinhood Chain RPC with the required historical coverage |
| Read market price or gross balance value | Trusted package and permitted Python 3.10+ execution | Fixed public DEX Screener/GeckoTerminal pool endpoints; charter balances additionally use RPC |

All four fixed entrypoints—`snapshot.py`, `price.py`, `history.py` and `verify.py`—use only Python's standard library: no pip dependencies or wallet connector. RPC credentials are optional and supplied through host-managed environment secrets. They require the filesystem protections described in [execution](references/execution.md); unsupported hosts fail closed for those helpers. Other host-permitted tools may provide the requested capability. Dependency installation and reviewed maintenance require the ordinary approval flow, not permission bypass; missing capability means identify the prerequisite, not invent results.

### RPC reliability

For **orderbook and last-N history**, prefer a host-managed Alchemy endpoint or `SRSTACK_RPC_URL` provider with the required log/read coverage. The public default is a best-effort starting point for small auction snapshots, not a reliability promise. [Robinhood recommends Alchemy for production](https://docs.robinhood.com/chain/connecting/); confirm quota, batch/log and archive support for the actual workload.

The RPC helpers select `SRSTACK_RPC_URL` first, otherwise use `ALCHEMY_API_KEY` with `https://robinhood-mainnet.g.alchemy.com/v2/{API_KEY}`, otherwise use the credential-free default `https://rpc.mainnet.chain.robinhood.com/`. Supply either optional setting through host-managed environment/secrets, not CLI arguments or installed files. A custom endpoint supports HTTP or HTTPS, path/query components and URL Basic authentication; prefer HTTPS whenever credentials are involved. `verify.py` forwards both environment settings to its live child helpers. The helpers redact endpoint credentials from output and do not silently fail over. Robinhood labels the default public service rate-limited and **not recommended for production**; it is the zero-configuration path for occasional reads, not a provider restriction or the production reliability recommendation.

Keep provider keys in host-managed secrets, never installed skill files, prompts, command-line URLs or reported evidence. Check chain ID 4663 and a fresh head; keep dependent reads at one block and verify the block hash. Historical `eth_getLogs` availability does not imply historical `eth_call` state is retained. If a provider fails or denies access, report that result; do not silently merge providers, reuse stored state or bypass access controls.

Explorer links default to **[Robinhood Etherscan](https://robin.etherscan.io/)** for addresses, transactions and blocks. Alternate explorer URLs are retained only as provenance for evidence retrieved there, not as the default navigation destination.

## Install a reviewed release

**Current dogfood:** install a reviewed commit from `feature/v0.3.0`, not a nonexistent `v0.3.0` tag. The [installation runbook](references/installation.md#reviewed-installation) resolves a full commit before review, exports committed runtime bytes, and clean-replaces with rollback. If a specific pin was supplied, use it exactly.

### Quick test after installation

In a fresh host conversation, `Use srstack` should show **research / inspect / analyse / workflows**, without unsolicited reads. Packaged explanations should work offline without Python. Ask: “Assume 3,384 STANDARD pending, a fixed 15,179 target and 500 STANDARD/day net accrual: how long to the target?” Expect the 11,795 gap and a conditional 23.59-day estimate, not a forecasting refusal or a claim about actual future rates. Ask the [Second Mandate questions](#second-mandate-research): samples must not become holdings, reserve fees must not become holder entitlements, and proposals must not become deployed facts. Requested hypothetical models remain allowed. Signing/submitting must be declined without invoking a wallet.

From the reviewed, verified **installed root**, the default diagnostic is offline integrity verification. There is no `--offline` flag:

```sh
cd "${SKILL_PARENT:?Select the installed host root}/srstack" &&
python3 -B -I scripts/verify.py
```

Only if live access is intended and permitted, select a diagnostic:

```sh
python3 -B -I scripts/verify.py --price
python3 -B -I scripts/verify.py --charter 1 --price
```

Replace example ID `1` with the intended public charter ID. These diagnostics report **stage status and timing, not a price or monetary valuation**. They verify the entire package before running selected helpers; bare verification starts no child and makes no network request. Exit 0 means all selected stages are `ok`; partial, failed or skipped live stages exit 5. See [diagnostic statuses and exits](references/execution.md#package-and-smoke-diagnostic).

For actual live results, ask “Use srstack inspect protocol” or “Use srstack inspect charter 1”: expect a fresh block-scoped snapshot or a precise unavailable/partial result. For a charter's gross USD value, use its successful snapshot's `charter_pending` quantity unchanged with `scripts/price.py --amount-standard DECIMAL`, not the verifier's status. The [snapshot commands](#live-protocol-auction-and-charter-reads) and [price commands](#current-price-and-gross-accrued-balance-value) below exercise the real output paths. Offline operation never waives host execution approval.

Stage elapsed times measure local verification/helper execution, not host startup, model reasoning, discovery, tool-approval waits or answer rendering. Live network latency varies; no end-to-end runtime is promised. A successful local smoke does not certify host approvals, isolation, authenticity or financial correctness.

A live HTTP 401/403 identifies denial of that original request at its endpoint, not global chain/provider unavailability or failed installation. Preserve the helper's bounded original-response diagnostics. Do not evade that endpoint's access controls or a host denial. Independent public RPCs, explorers or APIs may supply fresh evidence under their own access rules; identify the new source and re-establish chain, block, interface and coverage as relevant. This is separate research, not an automatic helper fallback or proof that the original request succeeded. See [safety](references/safety.md#public-retrieval-and-calls).

## Examples

### Conversation starters

```text
Use srstack.
```

Expected: the research/inspect/analyse/workflows menu, without fetching live data.

```text
Use srstack to explain charter withdrawals.
Use only the packaged references and cite the source links.
```

Expected: a sourced explanation, including fees and evidence gaps.

### Second Mandate research

```text
Use srstack to explain the Second Mandate using packaged sources.
Are the manifesto's market positions actual holdings or sample illustrations?
Does the announced fee reinvestment establish revenue rights for charter holders?
```

Expected: distinguish announced strategy from deployed mechanics, identify sample positions, and explain that reserve-level fee reinvestment does not establish holder entitlements. If asked to model future returns or proposal effects, use labelled assumptions and formulas rather than treating samples as actual holdings or declining numerical analysis.

### Live protocol, auction and charter reads

```text
Use srstack inspect protocol. Show current issuance and buy/sell taxes.
Use srstack inspect protocol. Split permanent supply removal into token burns and retired ledger value, and show launch restrictions.
Use srstack inspect auctions. Are licenses available, and what price is actually usable?
What's the current branch auction status?
What will the next license round open at under the published policy, and when is its next scheduled boundary?
Show me the last 3 license rounds, including coverage limits and whether the latest round may still be in progress.
Show one bounded page of the branch orderbook. Do not infer charter IDs or owners from raw page IDs.
Use srstack inspect charter <public charter ID>. Show its branches and pending balance.
```

The reader checks the chain, block, code, module bindings and scalar decoding. Sold-out or disabled auctions do not produce purchasable quotes. A specific charter request also needs its public charter ID; it never needs a wallet connection.

“Branch auction” means the expansion-license auction. Its routine status path is `python3 -B -I scripts/snapshot.py auctions`: the reader already knows the reviewed deployment and getters. It does not crawl the website, rediscover contracts, scan past events or build an index. Read the current state once and answer with the availability path's status, reported remaining branches, current STANDARD price only when open, and observation time. A failed live read is unavailable, never an invitation to reuse a static snapshot.

Lazy rollover matters: compare the stored contract round with the elapsed round derived from the same block's timestamp, live anchor and live period. Both current v1.2 auctions use `auctionPeriod()`; the original charter's `AUCTION_DAY()` is not the replacement's timing interface. Neither is the separate license `capWindow()`. When rollover is pending, say “the availability path reports X branches available; stored counters belong to an earlier round,” not “X sold / Y remaining today.” Historical buyer/revenue reconstruction belongs to the history scanner, not these counters.

If challenged, inspect `started`, `paused`, `currentPrice`, `dayFloorPrice`, `dayCap`, `remainingToday`, `soldToday`, `lastSalePrice`, `lastSaleDay`, `currentDay`, `auctionAnchor` and the deployment's period getter at one block before scanning events. `snapshot.py auctions --detail full` supplies these supported direct reads and their round context; full output is evidence from that invocation, not an installed static snapshot.

Replace `<public charter ID>` with the ID to inspect.

| View | Selected observations |
|---|---|
| `protocol` | Issuance and epoch context, branch count, supply and permanent-burn decomposition, token restriction/launch flags, counter-based remaining budget, buy/sell tax and pool/emissions state |
| `auctions` | Current v1.2 license/charter activation, pause state, reported inventory, current prices and license open bid count; stored versus elapsed rounds, pending rollover, license documented-policy opening preview, derived schedules, separate charter-cap window and decay setting |
| `orderbook` | One `--start`/`--count` raw-ID page (count 1–100), global count and optional up to ten explicit `--charter-ids` bid/fillability reads; no inferred page-to-charter mapping, price normalization or wallet-order census |
| `treasury` | Current/queued fee allocation, team ETH liability, vault authority/pause, contraction-buyback controls, POL/incentives ownership and the vault's live STANDARD balance; optional approved-asset raw holdings and pool key |
| `charter` | Default: public owner, branches, pending and supported current-rate equivalent. Explicit `--detail full`: additional protocol context and raw evidence |

Each invocation uses one checked block. Separate example invocations are not one atomic combined snapshot; do not combine their values as if they share a block. Failed fields remain missing with errors; fatal failures return no snapshot. Results are not saved or reused as a fallback. These are selected publisher-ABI reads, not a complete contract audit.

Advanced users can request the same protocol snapshot from the reviewed installed root:

```sh
python3 -B -I scripts/snapshot.py protocol
python3 -B -I scripts/snapshot.py auctions
python3 -B -I scripts/snapshot.py charter --id 1
python3 -B -I scripts/snapshot.py treasury
```

The charter command requires an unsigned uint256 ID; replace `1` with the intended public ID. **Summary is compact in the helper's JSON output**, not just agent-side formatting; `--detail full` opts into raw evidence. No-argument JSON stdin is equally supported, for example `{"schema_version":1,"view":"charter","charter_id":1}`. Default answers show useful values first, with at most one short note such as **“RPC snapshot; publisher ABI.”**

### Bounded auction history

Auction history now defaults to **contract-state discovery first**, using authenticated anchor getters and historical hash-pinned calls to locate candidate purchase windows before requesting logs of at most **10 blocks**. This avoids an oversized first request on ten-block-limited providers. Equal sampled state cannot prove no intervening purchases: skipped intervals stay explicitly unsearched and prices remain observed-event accounting, not complete-round averages. First executed sale and authenticated `AuctionStarted` opening prices are included separately. Use `license` or `charter`, optional `--day N`, and an anchored lookback or explicit inclusive block bounds; see the [history contract](references/auction-history.md) for limits and explicit log-only collection.

```sh
python3 -B -I scripts/history.py license --lookback-blocks 1000000
python3 -B -I scripts/history.py license --generation current --last-rounds 3
python3 -B -I scripts/history.py charter --day 1 --from-block 1 --to-block 1000000
```

Choose the round, generation and block scope for the question; the examples do not assert where a round occurred. An auction day is a filter, not a 24-hour block estimate. License history preserves original, v1.1 and v1.2 emitters; charter history preserves original and v1.2 emitters. Repeated round identifiers never merge across addresses. Report scanned coverage and partial results, not complete-all-history. A last observed purchase alone does not prove sellout, and an open bid is not a completed purchase. Results go to stdout and are never saved as runtime observations.

For contraction buybacks use `python3 -B -I scripts/history.py buybacks --lookback-blocks 1000000`. For POL acquisitions use `python3 -B -I scripts/history.py pol-buybacks --lookback-blocks 1000000`. Neither accepts an auction-day filter. The first reports event-accounted ETH spent and STANDARD burned; the second reports event-accounted ETH input, raw token output and destination, without claiming token burns or an authenticated token denomination. Neither is receipt-reconciled asset movement or complete-all-history.

Treasury optionally accepts `--asset ADDRESS` only as a fixed vault-call argument; approval false/unavailable omits holdings and pool details. Reserve-token holdings and internal streamed counters with unestablished decimals remain raw units; queued policy is never substituted for current settings. The incentives vault's separately authenticated STANDARD balance is retained tokens, not burned supply.

### Current price and gross accrued-balance value

```text
Use srstack inspect price. Show STANDARD in USD and ETH.
What is 1000 STANDARD worth at the latest reported market price?
What is the accrued balance of public charter <public charter ID> worth in USD now?
Use srstack inspect price. Cross-check DEX Screener against GeckoTerminal.
Use GeckoTerminal for the current STANDARD price.
```

Current-value questions use the shared price reader automatically; there is no prerequisite `inspect price` step. A charter USD question needs **one charter snapshot and one price-helper invocation**, not an extra protocol snapshot or default cross-check. Pass the successful `charter_pending` quantity unchanged to `scripts/price.py --amount-standard DECIMAL`; report its `valuation.gross_usd`, or that USD is unavailable. Ask only for a missing public ID, not a wallet. This is a gross market mark of a STANDARD-denominated ledger balance—not wallet tokens, net withdrawal proceeds or a branch/NFT resale price. It does not value future earning capacity.

By default, the reader queries DEX Screener for the exact canonical ETH/STANDARD pool. If that source is unavailable, it can use GeckoTerminal and explicitly label the fallback and reason. Identity/schema violations and host/provider access denials do not trigger fallback. A valid partial response stays with its provider rather than filling a missing currency from another source. Chain, token, quote asset and pool identity are checked for both providers; any amount valuation is local and never sent to them.

An explicit provider choice disables automatic fallback. A requested cross-check fetches the other fixed provider and reports its separate prices, evidence and percentage differences; it does not average prices, pick the higher value or change the selected valuation source. Each invocation makes at most two requests. Ordinary price questions do not fetch both providers unnecessarily.

These provider and arithmetic rules describe the bundled helper, not the limits of research. Other sources, market discovery, currencies, cross-source statistics, conditional calculations and user-supplied inputs are permitted with explicit identities, units, times, formulas and assumptions. Public addresses can be inspected without proof of ownership. Private files, authenticated sessions and outputs follow the user's scope and host permissions; see [safety](references/safety.md) and [supplemental reads](references/inspection.md#supplemental-public-reads).

From the reviewed installed root:

```sh
python3 -B -I scripts/price.py --quote
python3 -B -I scripts/price.py --amount-standard 1000
python3 -B -I scripts/price.py --quote --cross-check
python3 -B -I scripts/price.py --source geckoterminal --amount-standard 1000
```

`source` is `auto` (default), `dexscreener` or `geckoterminal`; `cross_check` is an optional boolean, defaulting to false. The optional amount is an unsigned decimal **string**, not a JSON number. Quotes and gross values are decimal strings. Failed fields remain missing, and a labelled fallback never becomes a cached or invented value.

The snapshot and price helpers also accept no-argument JSON stdin; `--help` and the [execution contract](references/execution.md) describe strict input handling. CLI mode does not read stdin or relax approval/integrity checks. Use `--amount-standard` alone for a valuation, not together with `--quote`. Amounts in CLI arguments may appear in process listings or host logs; stdin does not promise transcript privacy.

These are **provider-reported indicative prices**. Neither consumed pool API supplies a quote-observation timestamp: retrieval/cache age is not quote age, and pool creation time is not price freshness. Charter state, the selected price and any cross-check have separate observation boundaries, not one atomic snapshot. Gross values exclude withdrawal fees, trading taxes, LP fees, slippage and gas.

## Contract coverage

The [contract catalog](assets/entities/robinhood.json) contains **14 publisher-listed identities on Robinhood Chain (4663)**. The fixed [publisher read interface](assets/interfaces/robinhood-reads.json) supports selected live getter reads from **nine**:

| Contract | Questions supported by fresh reads |
|---|---|
| **$STANDARD** | What are total supply, ceiling, permanent token burns and retired ledger value? Are launch holding limits and the Pool Manager gate enabled/active? `totalSupply()` is not necessarily circulating supply. |
| **Central Bank** | What are the issuance rate, multiplier, stream rate, branch count and epoch? What budget remains according to the issuance counters? |
| **Charter NFT** | Who owns public charter X? Combined with Central Bank reads, how many branches and pending credits does it have? |
| **Trading Hook** | What are current buy/sell taxes? Is an override or launch schedule active? Is the pool initialized, and is an ownership handoff pending? |
| **Expansion License Auction** | Is it started or paused? How much inventory remains? Is there a usable current price, and what is the auction duration? |
| **Charter Auction** | Is the v1.2 auction started or paused? Is inventory available, and what are the usable ETH price and observed round period? |
| **Fee Splitter** | What are current/queued team and POL shares, team ETH liability, wallet and pending ownership? |
| **Expansion Vault** | Is it paused, who controls it, and is the requested reserve asset approved? If approved, what are its raw holdings and pool key? |
| **Contraction Vault** | What are the timing, configured/effective pool and TWAP limits, configured vault percentage and ETH depth? Bounded history separately accounts for `BuybackExecuted` events. |

The other five have **no direct getter profile**: Founding Sale, Liquidity Manager, Address Registry, Uniswap v4 Pool Manager and Multicall. Registry and Pool Manager identities/code also participate in the treasury authentication graph. Their addresses and explorer links are cataloged; this does not establish complete holdings, permissions or implementation correspondence.

Use the fixed helpers where they fit and [authenticated supplemental reads](references/inspection.md#supplemental-public-reads) for gaps. Ordinary research does not modify installed catalogs.

**Publisher-listed addresses and publisher ABIs do not establish source correspondence.** Selected STANDARD and Trading Hook interfaces and accounting/restriction semantics have additional source-review provenance; that review does not verify the other modules or establish current deployment state. The package bundles no contract source and stores no current explorer verdicts. Current verification status requires fresh retrieval. Getter observations do not establish complete administrator powers, upgradeability, audit correspondence or exploit resistance. Source dates identify reference provenance, not live-state freshness.

## Coverage and footprint

The package covers the 16-section whitepaper, contract identities, publisher ABI definitions and the [Second Mandate manifesto](references/updates.md#second-mandate-liquidity-for-tokenized-stocks) as announced strategic direction. It stores no changing-state snapshots, recap metrics or explorer verification verdicts. Current balances, rates, supply, inventory, prices, activation, verification status and latest announcements require fresh retrieval; unavailable data stays unavailable.

For current protocol questions, request only the relevant [inspection](references/inspection.md). Current stream rates, remaining-budget accounting, sale taxes, LP fees and unavailable auctions have different meanings; none establishes future earnings or executable net proceeds.

The package uses selected references and indexed records rather than loading the whole corpus for every question. The reference indexes own current inventory counts; disk size is not per-question token cost, and selective loading depends on the host.

Packaged research needs a resource reader. Bundled readers use **Python 3.10+ and its standard library**, environment-selected RPC endpoints, fixed price-provider paths and supported filesystem primitives. Other host-permitted tools, reviewed dependencies and custom code can support additional requested workflows without modifying these helpers. No wallet signer, telemetry, scheduler or self-update process is bundled; host capabilities must actually exist before claiming an operation was performed.

## Safety and verification limits

Answers lead with content. Estimates get a short label; observations get a brief source note where needed. Detailed provenance and assumptions are available on request, not repeated as small print.

The helpers retain fixed targets, strict decoding, finite budgets and integrity checks; they write no files and make no financial transactions. Ready-to-sign calldata, transaction deep links and filled unsigned objects require an **explicit preparation request**. Explanation/inspection alone does not authorize them. Signing and submission remain excluded. The full rule lives in [safety](references/safety.md#preparation-and-wallet-boundary).

The readers do **not themselves** implement liquidity-depth analysis, amount-specific withdrawal quotes, gas estimation or strategy/settlement models. Use appropriate supplemental tools or explicit calculations for those requests, preserving evidence and assumptions. No result is guaranteed sale proceeds. A helper's missing feature is not a skill-wide prohibition.

Skill instructions do not enforce host isolation, and estimates are not guaranteed returns.

## Repository validation

These commands run from the **repository root**, not the installed skill folder:

```sh
python3 -B maintenance/package.py verify
python3 -B maintenance/check-snapshot.py
python3 -B maintenance/check-price.py
python3 -B maintenance/check-history.py
python3 -B maintenance/check-history-state.py
python3 -B maintenance/check-history-accounting.py
python3 -B maintenance/check-interface.py
python3 -B maintenance/check-verify.py
python3 -B maintenance/check-package.py
python3 -B maintenance/package.py archive
```

The checks use Python's standard library and local Git; they do not call explorers, connect wallets or use model/API credentials. CI runs Linux with Python 3.10 and 3.14, plus macOS with Python 3.14, using read-only repository permissions and commit-pinned Actions. GitHub checkout and Python provisioning require network access; the validation commands themselves are offline. CI verifies the committed manifest rather than regenerating it, and checks deterministic ZIP output. It does not upload artifacts, tag, publish releases or monitor contracts.

After deliberate runtime changes, regenerate the manifest with `python3 -B maintenance/package.py build`, then run the checks above. The archive `dist/srstack-0.3.0.zip` contains only the runtime package; building it does not publish a release or certify it. Maintenance tooling and CI files are repository-only; their execution requires a deliberate maintenance request, trusted code and normal host permissions.

**Agent acceptance replays:** repository-only `maintenance/agent-acceptance.json` defines synthetic questions, required/forbidden outcomes and a separate run-record format. Load the candidate skill in a fresh, normally permissioned session and replay each case as supplied evidence, not live state. Record host/model, loaded revision and manifest, actual tools/actions, response and criterion-level results outside the installed runtime. Use no real wallet capabilities or credentials; do not add extra refusal instructions that predetermine the result. Report blocked and unrun cases explicitly. These specifications are not passing results: offline CI does not run a model, and a replay does not certify host isolation.

**Independent interface vectors:** `check-interface.py` exercises selected literal calldata, return words and event layouts independently of the catalog-driven fixture encoders. This is targeted layout coverage, not exhaustive selector recomputation, contract-source/deployment equivalence or financial-semantic verification.

## Feedback and license

Report reproducible problems through [GitHub issues](https://github.com/tomismeta/srstack/issues), including the host/version, package commit, actual loaded path and redacted reproduction. Never upload wallet credentials, private RPC URLs or private conversation history.

Original srstack code, summaries and instructions are [MIT-licensed](LICENSE). Third-party documents, posts, media, trademarks and protocol code retain their owners' rights and are excluded from that grant. Source links and quotations do not transfer those rights or imply affiliation.
