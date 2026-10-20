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

Use the [capability planning map](capabilities.md#planning-map) and [stock/markets inventory](interface-inventory-stock-markets.md) for actual interface coverage and layouts. These questions select evidence, not a mandatory call sequence:

| Question | Minimum relevant evidence and interpretation |
| --- | --- |
| What fee applies now? | `stock-pool-fees`: full pool identity, relevant hook class/session/configuration and effective-fee evidence for the supplied sender and block/time. Keep successful observations and missing pools separate. |
| Why does the fee differ by pool or time? | `stock-pool-fees`: class assignment and session fees, calendar/ramp context, applicable global/per-pool overrides and exemptions at the same observation anchor. A generic schedule is insufficient. |
| What does my LP position earn? | `stock-pool-backing-and-income`: authenticated position/range/liquidity, fee accrual and collection flows, contribution/withdrawal history and relevant prices. Hook fee state alone cannot answer realized net income. |
| What does a market index show? | Optional publisher endpoints below: scope, source-specific classification, as-of fields, unresolved records and pagination. Index inventory is not an independent factory census. |
| Is the token backed or the pool safe? | `stock-pool-backing-and-income`: issuer/custodian/redemption evidence and contract/position-specific controls. Neither ticker, pool size nor hook ABI supplies these facts. |
| Does trading create pilot rewards? | `market-pilot-entitlement`: [pilot rules and conflicts](market-pilot.md), points coverage, custody/liabilities and actual settlement evidence. Fee or volume observations alone are not payout entitlement. |

## Fees and LP economics

**Units:** the dated contract research identifies Uniswap hook fees as **hundredths of a basis point**. Divide a raw fee by 100 for bps, by 10,000 for percent, or by 1,000,000 for the fractional rate. For example, raw **450 = 4.5 bps = 0.045%**, not 450 bps or 450%. This is a unit illustration, not a current pool default. Launchpad base/module BPS fields use their own declared scales; do not decode them with the stock-hook convention.

The [stock guide](https://www.standardreserve.xyz/docs/stock-tokens/) describes per-swap dynamic fees computed from block time, US Eastern sessions with DST, NYSE holidays, early closes and configurable unscheduled closures. It describes regular, extended, overnight and closed sessions; fee classes with their own four rates; a published 10% ceiling; and a two-minute ramp on decreases while increases apply immediately. These are dated publisher mechanics, not a universal current rate table. Per-pool/global overrides, exemptions and sender-specific rules matter alongside the session/class configuration. A quote for a zero-address sender is not a quote for every router or user.

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

[Stock source records](../assets/sources/stock-pools.json): `sr-stock-pool-docs-2026-10-19`, `sr-stock-pool-identities-2026-10-19`, `sr-stock-hook-verified-abi-2026-10-19`, `sr-stock-fee-change-2026-10-19`, `sr-stock-fee-announcement-2026-10-19`. Fresh root-linked documentation was inspected as data. The contract report attributes earlier explorer source and pinned reads; fresh explorer acquisition was denied, so that historical inspection is not newly recovered source/ABI proof. The [family inventory](interface-inventory-stock-markets.md) states actual available encoding coverage and explicit gaps. Missing hook ABI or issuer evidence blocks only conclusions depending on it, not supported descriptions or labelled market observations.

No independent whole-portfolio valuation, stock-issuer audit, complete administrative history or realized LP-income reconciliation is established here. Keep stock-pool fees, [launchpad fees](launchpad.md#fees-and-creator-controls), [pilot funding](market-pilot.md#funding-and-distribution-evidence) and [charter distributions](charter-distributions.md) separate; none silently creates charter redemption rights or changes the older protocol fee split.
