# Auction and buyback history: bounded event helper

Use `snapshot.py auctions` for current auction price, supply and round context; use `history.py` only for requested historical observations. The helper prints freshly fetched results to stdout, never saves a current-state fallback, signs or submits transactions. [Safety](safety.md) governs artifact approval: how-to prose remains allowed, but calldata, transaction deep links and filled unsigned transaction artifacts require an **explicit user request**.

Purchase history is not orderbook history: bids, cancellations, unfilled orders and failed keeper attempts are not purchases. A purchase log alone does not establish an order, funding route or execution fairness. For other events, receipts or historical state, use bounded [supplemental public reads](inspection.md#supplemental-public-reads), preserving separate coverage and provenance.

## Question to window

| Question | Minimal path |
|---|---|
| Last N license rounds | `history.py license --generation current --last-rounds N`. Report latest observed address-qualified rounds, including an in-progress round, with observed roll prices/cap and last observed purchase price. Stop at N observed groups per deployed selected generation; older scope remains explicitly unsearched. |
| Current / previous round purchases | Read `snapshot.py auctions` once if necessary to identify generation and elapsed round, not lazy stored `currentDay()`. “Previous” means the preceding elapsed round; round zero has no predecessor. Resolve evidenced finite bounds, then use `--day ROUND --from-block FIRST --to-block LAST`. |
| Last round with purchases | Scan a finite recent window; select the latest checked purchase by event position, not the largest numeric day across generations. Say “last observed in this window.” |
| Performance over dates | Resolve dates/timezone to `[start, end)` (UTC if unspecified, disclosed); find the first canonical block at/after start and the block before end. Scan those inclusive bounds without `--day`. Report window totals, not complete-round totals. |

Resolve timestamps with a bounded index checked against canonical RPC headers or a bounded header binary search under one pinned head; verify neighboring boundary headers. Never convert hours to guessed block counts. Cap future endpoints at the observed head and label “through observation.” An empty interval needs no scan. Without interval-specific round timing evidence, choose a finite search window and label results **observed purchases in that window**.

For a round-price question, produce `generation / round | observed opening | first observed sale | quantity-weighted observed average | last observed sale | observed quantity`, plus checked bounds and gaps. Opening comes from `AuctionStarted.startPrice` or a recorded `DayRolled.startPrice`, never the first purchase or a policy estimate. Keep live cap/status/ask separately anchored; an open round's average/last sale can move. Omit last-N early stopping when the question needs earlier purchases in the selected window. Unknown observations stay unknown; conflicting openings remain separate. Unsearched intervals prevent a complete-round average claim but do not prevent a useful observed-events table.

## Run a bounded scan

Run from the installed skill root with the reviewed Python 3 runtime. Replace uppercase placeholders with evidenced decimal integers, not guessed blocks or round IDs.

```sh
python3 -B -I scripts/history.py license --generation current --last-rounds 3
python3 -B -I scripts/history.py license --day ROUND --from-block FIRST --to-block LAST
python3 -B -I scripts/history.py charter --from-block FIRST --to-block LAST
python3 -B -I scripts/history.py buybacks --from-block FIRST --to-block LAST
python3 -B -I scripts/history.py pol-buybacks --from-block FIRST --to-block LAST
```

- `--last-rounds N` accepts 1–1000, is auction-only and mutually exclusive with `--day`. It scans newest-first and stops **after committing a whole checked chunk** once every selected generation deployed by the anchor has at least N observed address/round groups. It selects at most N per generation by newest observed event position, not numeric day. It does not finish the oldest selected round: earlier events from that or another selected round may be in the deliberately unsearched prefix. Quantities and prices are checked-window observations, not full-round totals or final closes. If no older deployed scope remains, the helper can finish the header-only precreation prefix instead.
- If N is unavailable, scanning continues only within the finite requested bounds and existing budgets. A young deployment may have fewer than N observed groups; only postcreation logs are queried. `shortfall` describes checked observations, not proof that missing rounds never existed outside those bounds. No cross-generation backfill, synthetic rows or automatic wider scan occurs.
- `--generation current|legacy|all` selects v1.2, original or all auction deployments; default `all`. License also accepts `v1.1`. Shared day IDs never merge across addresses. Not-yet-deployed generations do not hold up the N-round threshold. Generation names are catalog identities, not live Registry guarantees.
- `--day N` filters the emitted round ID, not a UTC date, and does not narrow the log query or prove a lifetime. Without last-N, day-filtered, unfiltered and buyback scans remain oldest-first. Buybacks reject both round-selection flags.
- Default bounds are a **1,000,000-block** lookback ending at one fresh head, clamped at genesis. Optional `--anchor-block B` pins the inclusive upper endpoint; `--lookback-blocks N` changes the span. Alternatively use both `--from-block A --to-block B`; do not combine this form with anchor/lookback flags. Historical anchors need not be fresh. No silent range widening occurs.
- Auctions default to `--discovery state`: read `started`, `currentDay`, `soldToday`, `lastSaleDay` and `lastSalePrice` at the anchor first, then recursively compare historical endpoint state to locate candidate event windows. Calls use EIP-1898 canonical block hashes; the provider must support historical state and hash-pinned `eth_call`. `--chunk-blocks N` defaults/maxes at **10** in this mode, so no oversized log request is sent first. No automatic retry or downgrade follows an archive failure.
- Equal endpoint state is **not proof of no intervening activity**: deployed reset/monotonicity semantics remain unverified. Such intervals enter `coverage.unsearched`, never `completed`; the report is partial. State probes are cached only within the invocation and their headers are rechecked. Old-generation getters use retained publisher ABI evidence, not guessed storage slots.
- Explicit `--discovery logs` performs exhaustive bounded log-window scanning without state discovery; buybacks retain this event-accounting mode. Its chunk default/maximum is **10,000**; select `--chunk-blocks 10` for a known ten-block provider cap. This is an explicit method choice, not automatic fallback after a denial.
- `--max-chunks N` defaults to **100**, maximum **500**, counting actual log windows, not discarded candidate intervals. `--detail summary|full` defaults to summary; full adds decoded checked events under `evidence.decoded_events`, limited to selected round keys. Only charter purchases include a buyer field.

RPC selection is `SRSTACK_RPC_URL` > `ALCHEMY_API_KEY` > official public default. Robinhood's [connection guidance](https://docs.robinhood.com/chain/connecting/) recommends production providers/archive access for substantial historical use. See [provider configuration](execution.md#rpc-provider-guidance) for credentials and supported endpoint forms. This helper does not retry, switch providers or resume automatically after a denial; [safety](safety.md) applies to separate research.

Hard ceilings: **5,000,000 requested blocks**, **4,096 individual RPC requests**, **64 MiB total response budget**, **1 MiB per response**, **10,000 returned logs**, **2,048 headers/window**, **1,000 observed address/round pairs**, **180 seconds overall**, and the shared transport's **10-second request deadline**. At least **2,000 logs/window** is conservatively saturated/incomplete. Live HTTP requests are spaced at least **0.5 seconds** apart within the same deadline; a 429 still stops. Limits are shared across emitters. Creation splits consume log-chunk slots; the consolidated precreation prefix does not.

## Read the result

Auction output has `schema_version: 1`, `status`, `auction`, `rounds`, `coverage`, `errors` and `evidence`. Treasury modes instead have `kind` and `buybacks` or `pol_buybacks`. Exit **0** means the requested observed-row selection or bounded scan passed the helper's checks; **4** means partial/unavailable history; **2** means invalid input. **`status: "ok"` does not imply the entire requested range was searched**, complete rounds, independent provider completeness or finality.

### Coverage and stopping

- `coverage.requested` is the original inclusive range. `completed` contains chronological, non-overlapping checked windows, emitter addresses, matched-event counts and checked-header digests. `scan_order` records traversal direction. Each window commits atomically for all applicable emitters.
- `missing` is failed/unavailable scan scope; `unsearched` contains the deliberately skipped prefix after N and/or intervals with equal sampled endpoint state. Either can hide purchases or opening events. `stop_reason` is `last_rounds_observed`, `state_candidates_scanned`, `requested_range_scanned` or `error`. `requested_range_complete` is false with errors, missing or unsearched scope; even true means only a checked bounded scan.
- Last-N stopping alone can return `status: "ok"` with an unsearched prefix. Equal-state skipped intervals always make the result partial and add `state_discovery_intervals_unsearched` to row gaps. Budget/error stops and observed-round shortfalls remain partial. `complete_round` remains false; never label an observed subset's average as a full-round average.
- `round_selection` reports requested count per generation, observed/selected counts and shortfalls. Undeployed generations have `status: "not_deployed_at_anchor"` and no shortfall; they are not observed zero-sale rounds. These counts describe this invocation's finite checked observations only.
- Window `scan_status: "logs_checked"` means a checked log query. `"no_deployed_emitters"` is a catalog-proven precreation prefix checked via boundary headers and anchor, with no log query or nonexistent-contract code check.
- `errors` identifies setup, window or final-anchor failure. Transport failures retain bounded original diagnostics. Ordinary failure preserves committed windows; reorg evidence invalidates all of them. A final-anchor failure alone retains earlier per-window checks but makes the result partial.
- `evidence` identifies the redacted endpoint, chain, catalog hashes, anchor/code, deployment boundaries, generation provenance, retrieval time, budgets and usage. `state_discovery` includes raw per-address anchor getter observations, canonical-hash pinning and discovery limits; these do not establish lazy-roll semantics or a final close. `usage.log_chunks` counts attempted log windows including failures, not state probes or precreation checks.

### Auction observations

`(chain_id, address, day)` is the round key; `day` is an exact decimal string. `purchase_quantity` sums license counts or one per charter purchase, independently of event count. `consideration` reports exact raw/scaled totals in **18-decimal STANDARD** for licenses or **ETH wei / 18 decimals** for charters. License consideration is `count × unitPrice`; charter consideration is emitted `price`, not transaction value or a maximum input. `quantity_weighted_average_raw` is an exact reduced numerator/denominator fraction. No purchases means a null average; never average round averages or mix denominations.

`observed_rolls` retains `DayRolled` block/time/transaction and reported start/floor/cap; `observed_activations` retains `AuctionStarted` block/time/transaction and its `reported_start_price`. Price objects have asset, decimals, raw integer and scaled decimal. `first_observed_purchase` and `last_observed_purchase` both retain checked observations and executed `unit_price`. An emitted opening-price parameter is distinct from the first observed executed sale price; neither establishes a scheduled opening or proves the scan includes the round's first sale. These are event parameters and executed prices, not current quotes or verified final closes. `reported_round_cap` requires consistent same-round roll observations. Activation or unrelated supply-setting events cannot supply it.

`scheduled_opening` and `time_to_sellout` stay null, `complete_round` false and `sellout` `"not_established"`. A lazy roll's timestamp is not scheduled opening; purchase time is not opening either. No reviewed `AuctionEnded` or `SoldOut` event exists. Historical duration, effective configuration, cap changes and opening/expiry semantics need interval-specific evidence, not today's getters. Distinguish v1.1's 12-hour round from its separate 24-hour charter cap window; see [auction policy and generation differences](auctions.md).

Sellout requires coverage from an evidenced opening, the historically applied cap and effective changes, plus a non-duplicated exhaustion purchase. Time to sellout additionally requires evidenced endpoints. Partial quantity equal to today's cap proves neither. Receipt reconciliation may corroborate license consideration with authenticated same-execution `BranchesOpened` evidence, without counting that amount twice. Event accounting alone does not prove ERC20 movement, funding route, burn routing or holder income.

### Buyback event accounting

`buybacks` uses Contraction Vault `BuybackExecuted(uint256,uint256)` only. It sums `ethSpent` as ETH and `tokensBurned` as 18-decimal STANDARD under `eth_spent` and `standard_burned`, each with exact `total_raw` and scaled `total`. At the scan anchor it checks fixed `ContractionVault.standard()`, STANDARD code and `decimals() == 18`; failure stops before logs. This anchor binding does not establish continuity throughout earlier history. Counts/totals are event accounting, not all protocol burns or reconciled token movement.

`pol-buybacks` uses the separate `BuybackExecuted(uint256,uint256,address)` layout. `eth_in` sums ETH `ethIn`; `tokens_out.total_raw` sums raw `tokensOut`, with asset, decimals and scaled total **null**. `reported_destinations` groups emitted destinations and raw outputs; these are not proven transfers, permanent bindings or income. There is no `standard_burned` field, denomination override or invented token getter. The provenance is explorer-decoded/receipt-corroborated event evidence, not a complete POL ABI.

Both modes expose event counts and first/last observations. `observation_status` distinguishes observed events, checked-window no matches and unavailable data; POL also identifies checked precreation scope as `no_deployed_emitters`. Checked empty windows yield observed zero, not all-history absence. No committed coverage yields null counts/totals (and POL destinations), not zero. Their `requested_range_complete` remains false on errors or missing coverage. Programmatic selections use `{"schema_version":1,"kind":"buybacks"|"pol-buybacks",...bounds}`; auctions use `auction: "license"|"charter"`, not both fields.

## Authenticate the requested generation

The [auction catalog](../assets/interfaces/auction-events.json), [treasury catalog](../assets/interfaces/treasury-events.json) and [source provenance](../assets/sources/live-interface.json) carry exact identities, ABIs and historical evidence. Do not substitute the founding sale, another chain or a successor address. V1.1 license creation is block **69178086**; its observed activation/Registry replacement is **69222157**. V1.2 creation is **73428552** for license and **73428767** for charter; announced activation **73474626** is not a creation cutoff. POL creation is **69178088**.

Scans split at authenticated creation, **not activation or Registry cutover**, retaining initialization and prior-generation emissions. Applicable emitters share one address-array query and anchor code checks. Source recovery follows [contracts guidance](contracts.md#recover-a-stale-frontend-source-link); interface/publisher binding is not proof of bytecode equivalence.

## Retrieve a finite, auditable window

After [trusted-runtime preflight](execution.md#trusted-runtime-preflight), the helper descriptor-loads the reviewed sibling snapshot routines, validates chain **4663**, fixed catalog fingerprints and entity addresses, then pins one anchor. Queries use ascending inclusive bounds, fixed emitters and their authenticated topic-zero filters. Strict decoding checks field sizes, supported types, address padding, positions, hashes, duplicates and removed logs.

The helper checks canonical headers for event blocks/window boundaries, rechecks headers plus anchor before committing each window, and rechecks the final anchor. State discovery also rechecks all probed historical headers. Reorg observations invalidate all committed windows. State discovery subdivides candidate intervals before any log query; it never retries a failed query or switches providers. A successful provider response can silently omit logs; neither consistency checks nor equal sampled state independently prove completeness.

For stronger historical conclusions, retain separately authenticated, pinned state/receipts and calculation evidence under [safety](safety.md). Archive failures cannot be replaced with `latest`. Report supported observations and the exact missing evidence rather than fictional round recaps; hypothetical models must remain explicitly separate from reconstructed history.
