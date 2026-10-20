# Stock liquidity, fees and public market evidence

A Reserve-seeded stock/USDG pool is underlying trading liquidity, not a launched token's curve or token/stock pool, and neither is legal ownership of the referenced company. The October 19, 2026 review combines publisher documentation, rendered public pages and attributed bounded contract research; these establish product descriptions and discovery leads, not complete backing, custody or realized income. Reuse [contract authentication](contracts.md), [public-read inspection](inspection.md) and the existing [wallet/preparation boundary](safety.md#preparation-and-wallet-boundary), rather than treating a public liquidity link as authority to connect or transact.

## Stock pools and identity

The publisher describes Reserve-owned and Reserve-seeded **stock/USDG** markets. Its October 14 announcement and October 19 documentation support these dated market/team associations:

| Publisher market | Team association | Identity limit |
| --- | --- | --- |
| SPCX/USDG | US | Stock-token ticker and issuer/exposure description are not legal share title. |
| BABA/USDG | China | Listing does not establish backing, custody or redemption rights. |
| SKHY/USDG | South Korea | Country classification does not establish holder rights or a local-market fee clock. |

These are publisher-supported pairs, not a runtime token router. Authenticate actual token addresses and decimals before amount reads. A launched token may trade against one of these stock assets, drawing on the underlying stock/USDG liquidity for conversions; newer [launchpad tokens](launchpad.md#identify-the-token-generation) may instead pair with WETH. Stock documentation's generalized “launchpad tokens only accept the stock” is stock-route copy, not a universal restriction on the newer generation.

Uniswap v4's shared **PoolManager address is not an individual pool**. A complete pool identity includes chain, PoolManager, the full ordered `PoolKey(currency0, currency1, fee, tickSpacing, hooks)` and derived PoolId. A position additionally needs its own position identity, owner, liquidity and range; pool TVL is not a wallet's LP position. A dynamic-fee flag in a PoolKey is not a literal static swap rate.

Reuse an already authenticated full PoolKey and its provenance, checking that it belongs to the target chain/PoolManager/hook, rather than starting a broad initialization scan for each fee question. Where identity is missing, prefer scoped publisher/registration evidence and logs bounded by authenticated creation/deployment evidence; incomplete coverage remains explicit. Hook registration alone does not prove PoolManager initialization or liquidity.

Use the [capability planning map](capabilities.md#planning-map) and [stock/markets inventory](interface-inventory-stock-markets.md) for actual interface coverage and layouts. These questions select evidence, not a mandatory call sequence:

| Question | Minimum relevant evidence and interpretation |
| --- | --- |
| What fee applies now? | `stock-pool-fees`: authenticated full pool identity, `pools` registration/class/pause state, `classDefined`, global pause state and `feeFor` for the hook callback sender at the observed block/time. A returned fee alone is not an executable swap. Keep successful observations and missing pools separate. |
| Why does the fee differ by pool or time? | `stock-pool-fees`: class fees, calendar/ramp and resume context, global/per-pool overrides and sender exemption at the same state anchor. A generic schedule is insufficient; the [reviewed inventory](interface-inventory-stock-markets.md#effective-fees-and-units) gives exact layouts. |
| What does my LP position earn? | `stock-pool-backing-and-income`: authenticated position/range/liquidity, fee accrual and collection flows, contribution/withdrawal history and relevant prices. Hook fee state alone cannot answer realized net income. |
| What does a market index show? | Optional publisher endpoints below: scope, source-specific classification, as-of fields, unresolved records and pagination. Index inventory is not an independent factory census. |
| Is the token backed or the pool safe? | `stock-pool-backing-and-income`: issuer/custodian/redemption evidence and contract/position-specific controls. Neither ticker, pool size nor hook ABI supplies these facts. |
| Does trading create pilot rewards? | `market-pilot-entitlement`: [pilot rules and conflicts](market-pilot.md), points coverage, custody/liabilities and actual settlement evidence. Fee or volume observations alone are not payout entitlement. |

## Fees and LP economics

**Units:** the October20 reviewed hook ABI/source uses Uniswap LP fees in **hundredths of a basis point**. Divide a raw fee by 100 for bps, by 10,000 for percent, or by 1,000,000 for the fractional rate. For example, raw **450 = 4.5 bps = 0.045%**, not 450 bps or 450%. This is a unit illustration, not a current pool default. Launchpad base/module BPS fields use their own declared scales; do not decode them with the stock-hook convention.

The [stock guide](https://www.standardreserve.xyz/docs/stock-tokens/) describes per-swap dynamic fees from US Eastern sessions with DST, holidays and closures, a 10% ceiling and a two-minute downward ramp. The separately inspected October20 `SessionFeeHook` / `MarketCalendar` source establishes the bounded mechanics: **sender exemption first; otherwise the maximum of active pool/global overrides; otherwise ramped class fees**. Decreases ramp down, increases apply immediately, and unpause can restart a decrease from the class's Closed fee. The ramp/calendar settings are mutable: constructor or published settings are not current defaults. Class-array/session order is **Regular=0, Extended=1, Overnight=2, Closed=3**; local schedule and ramp values use minutes, while override/closure/resume times use Unix seconds. See [calendar layouts](interface-inventory-stock-markets.md#calendar-identity-and-event-evidence) for DST and holiday conventions.

`feeFor(bytes32,address,uint256)` uses the **hook callback sender**, often a router/swap contract, not an assumed trader or beneficiary. A zero-address illustration is not a quote for all routes. It does not check registration, class definition or pauses: read `pools`, `classDefined` and `allPaused` alongside it. `beforeSwap` checks pauses before fee selection, so even an exempt sender cannot bypass a pause. A successful fee view is not a promise a swap succeeds.

The packaged [authenticated ABI](../assets/interfaces/stock-session-hook-2026-10-20.json) supports encoding/decoding even when the explorer cannot be fetched. Current fees still need authenticated identities and fresh, compatible chain/block/hash/time reads. Supplying an arbitrary timestamp to `feeFor` evaluates the configuration at the selected read block; it does **not** time-travel mutable class, exemption, override or calendar state. Use archive state for historical conclusions; future-time evaluations are conditional.

The [October 16 developer announcement](https://x.com/0xbeans/status/2111055118808555612) gave **30/60/150/300 bps** for regular/pre-post/overnight/weekend sessions. Retain that as historical: the October 19 contract catch-up records later class changes and reassignment of all three stock pools, superseding use of the old table as a current fallback. See `sr-stock-fee-change-2026-10-19` in [stock sources](../assets/sources/stock-pools.json) for the dated change evidence. Do not install the catch-up's observed replacement fee table as a default either. If fresh effective-fee reads are unavailable, the current fee is unknown; the general mechanism can still be explained.

Keep distinct:

- **Swap fee rate and assessed amount:** require units, trade basis and relevant execution context; a rate is not a received fee.
- **LP share:** depends on the actual position, active liquidity/range and applicable allocation, not all pool volume accruing to one LP.
- **Gross protocol revenue:** requires attributable protocol-owned positions and fee flows; public LP fees are not automatically all Reserve income.
- **Annualization:** the October 16 post annualized only 44 hours of observed fees. A short-window extrapolation or displayed pool APR is not guaranteed future APR, compounded yield or realized user income.
- **Realized user income:** distinguish principal flows, accrued versus collected fees, inventory/price changes, costs and net receipts. A complete net-income claim requires the matching flow and valuation scope, not a fee getter or UI percentage.

The rendered October 19 liquidity page displayed “Add liquidity” and LP fee-share language. The reacquired stock guide links the site's `/liquidity/markets/` tab; the earlier website report also identified an outbound Uniswap position-creation link. These are observed public UX, not a successfully exercised LP deposit/withdrawal, safe custody or entitlement proof. Do not transfer STANDARD's older TaxHook/POL fee splits or [founding-trading](launch-trading.md) economics to these stock hooks or to third-party launchpad fees.

## Public market evidence

[`https://markets.standardreserve.xyz`](https://markets.standardreserve.xyz) is an optional publisher index discovered from the official application, not an independent accounting oracle or bundled client. [Indexer provenance](../assets/sources/market-pilot.json), `sr-market-pilot-indexer-2026-10-19`, records the catch-up's bounded coverage:

| GET endpoint | October 19 coverage |
| --- | --- |
| `/v1/tokens` | Token inventory exercised in the catch-up. Listings/classifications are publisher-indexed observations, not exhaustive independent factory discovery. |
| `/v1/pilot/summary` | Summary exercised in the catch-up. Rule fields, totals and unresolved volume/swaps are source-specific observations, not proved applied accounting. |
| `/v1/tokens/<address>/trades?limit=25[&before=...]` | Frontend-discovered shape only; not exercised as part of that endpoint coverage. |
| `/v1/tokens/<address>/candles?window=...` | Frontend-discovered shape only. |
| `/v1/tokens/<address>/holders?limit=50` | Frontend-discovered shape only. |
| `/v1/pilot/leaderboard?limit=...[&country=...]` | Frontend-discovered shape only. |
| `/v1/pilot/wallets/<address>` | Frontend-discovered shape only. |

Brackets in the endpoint examples mean an optional query suffix, not literal URL characters. These are discovery leads, not verified stable API contracts; no adapter, client or automatic updater is included.

Preserve **`asOfBlock`, `asOfTime`, `stale`**, retrieval time, query parameters, cursor/page coverage and source-specific token/team/stage classifications. An absent as-of field is unknown, not “now”; `stale:false` is a publisher freshness assertion, not accounting certification. Retain `unresolvedVolumeUsd` and `unresolvedSwaps` wherever supplied rather than silently treating them as resolved or zero. Errors, malformed payloads, unavailable pages and missing fields are not zero records or zero holdings.

A partial inventory can support labelled observations about the records returned without proving all launches, trades, holders or current points were covered. Token name/ticker/image metadata may be user-supplied and is not official endorsement. Reconcile disagreements with authenticated factory/curve or pool evidence when the question depends on them; do not erase the indexer's distinct scope or treat its classification as a chain fact. Keep raw identities and freshness through table reformatting. Use the existing [collection guidance](collection-efficiency.md) for bounded discovery and reuse; current requests must not fall back to sample tokens, old counts or cached catch-up balances.

## Backing and control limits

A stock-token/USDG pool and Reserve seed liquidity do not establish issuer reserves, custody arrangements, legal stock ownership, redeemability, dividend/voting rights or a holder claim on the Reserve. Pool liquidity, LP position ownership, token backing and protocol treasury holdings require different evidence. A launched token paired with a stock token does not inherit the stock issuer's rights.

The stock hook's configurable classes, calendars, overrides, pauses and exemptions require role-specific authority evidence. The dated report records an October 19 ownership-transfer initiation that was still pending at its checkpoint; Ownable2Step initiation is not accepted ownership. Refresh relevant owner/pending-owner state for a current control question rather than making the checkpoint permanent. A Safe destination or threshold does not establish all signers, modules, guards or spending powers.

[Stock source records](../assets/sources/stock-pools.json) preserve the October19 documentation, identities, historical ABI inspection attribution, fee-change and announcement records. That acquisition's fresh explorer requests were denied; its unknown hook-interface coverage remains historical. The separate **October20** `sr-stock-hook-verified-abi-2026-10-20` records the successful address-specific reader acquisition of the full ABI/source. Its retained reader-parsed JSON is not original HTTP response bytes, and full interface coverage is not deployed-implementation certification or a live fee observation. The [family inventory](interface-inventory-stock-markets.md) gives current encoding coverage and remaining evidence limits. Missing RPC, identity, pool coverage or issuer evidence blocks only dependent conclusions, not supported descriptions or labelled observations.

No independent whole-portfolio valuation, stock-issuer audit, complete administrative history or realized LP-income reconciliation is established here. Keep stock-pool fees, [launchpad fees](launchpad.md#fees-and-creator-controls), [pilot funding](market-pilot.md#funding-and-distribution-evidence) and [charter distributions](charter-distributions.md) separate; none silently creates charter redemption rights or changes the older protocol fee split.
