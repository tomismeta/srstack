# Stock-market interface evidence and gaps

**Reviewed 2026-10-19.** The publisher identifies a stock SessionFeeHook and a market-pilot reward Safe, but this acquisition obtained **no ABI for either role**. Both have dated [bindings](../assets/entities/contracts.json) under [review `publisher-ecosystem-2026-10-19`](../assets/interfaces/reviews.json), `interface_status: "unknown"` and empty interface IDs. No empty interface file, guessed selector or explorer review substitutes for missing evidence. See [stock liquidity](liquidity-markets.md), [market pilot](market-pilot.md), [capabilities](capabilities.md), [identity authentication](contracts.md#authenticate-the-requested-role) and [wallet boundaries](safety.md#preparation-and-wallet-boundary).

## Role scope

| Dated binding | Evidence and exact gap |
| --- | --- |
| `stock-session-hook-2026-10-14` / `stock-pools-2026-10-14` | Publisher stock-hook identity; both fresh explorer metadata and ABI requests were denied. No selected role-specific hook array was acquired. Session/class, effective-fee, global/pool override, exemption, administrator and event layouts remain unreviewed. |
| `market-pilot-reward-safe-2026-10-14` / `pilot-2026-10-14` | Publisher reward custody identity with historical Safe-proxy attribution, not a dedicated reward-distributor implementation. No address-authenticated Safe ABI was acquired. Thresholds, signer/module policy, payout automation and funding are not established here. |

The source chains are [stock-pool records](../assets/sources/stock-pools.json) and [pilot records](../assets/sources/market-pilot.json). Creation and pending-Safe handover observations are attributed historical research, not newly reacquired explorer evidence or accepted ownership. Reuse the existing shared PoolManager and administrative-Safe evidence; a singleton address is neither a full PoolKey/PoolId nor an LP position.

## Effective fees and units

`stock-pool-fees` is **unknown from the installed interfaces**. The neighboring [launchpad factories](interface-inventory-launchpad.md) establish a different product's launched-token/stock associations and configuration only; the machine row cites them as related identity context, **not as implementing SessionFeeHook reads**. Do not copy STANDARD TaxHook or launch-hook selectors, permissions or economics into the stock hook.

A current answer needs the actual stock/USDG PoolKey, pool class, relevant global/pool overrides and exemptions, sender and time at an authenticated block, using a separately authenticated hook interface. Numeric Uniswap hook fees are **hundredths of one basis point**: `450` means `4.5 bps`, not `450 bps` or `450%`. A dynamic-fee flag/sentinel in a PoolKey is not a numeric effective rate. Launch-module/base-fee BPS use a different scale. No current fee table is installed: the October16 schedule is historical after the October19 changes, and failed reads stay unknown.

## Income, points and settlement

`stock-pool-backing-and-income` remains unknown: a hook fee cannot prove issuer backing, legal share ownership, reserve custody, LP share, realized user income or an entire portfolio. Separate position ownership, fee growth, receipts, balances, complete relevant flows and issuer/legal evidence. Gross fee revenue and short-interval annualization are not realized LP yield.

`market-pilot-entitlement` also remains unknown from the reviewed factory/Config fee context. Preserve offchain-rule conflicts, mixed reward assets, liabilities and actual settlement evidence. A Safe address or one zero asset balance proves neither complete funding nor insolvency. The optional HTTP index described in [public market evidence](liquidity-markets.md#public-market-evidence) is discovery/source evidence, not an ABI-backed capability or a bundled client. No event/error layouts are claimed for either missing role.
