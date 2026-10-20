# Stock-market interfaces and evidence limits

**Stock-hook review 2026-10-20.** The [SessionFeeHook interface](../assets/interfaces/stock-session-hook-2026-10-20.json) retains the complete 93-entry explorer ABI: 53 functions, 21 events, 18 errors and one constructor. [Review `explorer-stock-hook-2026-10-20`](../assets/interfaces/reviews.json) ties publisher identity to the address-specific explorer ABI and inspected `SessionFeeHook` / `MarketCalendar` source. The retained acquisition is reader-parsed/pretty-printed JSON, not original HTTP response bytes; its representation, decoded source and canonical ABI fingerprints have distinct scopes. Full interface coverage is **not deployed-implementation certification**, current state or a whole-program audit. See [stock liquidity](liquidity-markets.md), [capabilities](capabilities.md#planning-map) and [authentication](contracts.md).

## Role scope

| Binding / generation | Reviewed evidence and limit |
| --- | --- |
| `stock-session-hook-2026-10-20` / `stock-pools-2026-10-14` | New dated binding to the same publisher-attributed hook, linked to the new explorer review/interface. Full ABI and bounded source mechanics support fee-read planning; fresh identity/code and chain state still govern current answers. |
| `stock-session-hook-2026-10-14` / `stock-pools-2026-10-14` | Preserved historical October19 identity-only binding/review. That acquisition's explorer requests were denied and no selected hook ABI was acquired; its unknown interface status is historical, not the scope of the October20 review. |
| `market-pilot-reward-safe-2026-10-14` / `pilot-2026-10-14` | Publisher reward custody identity with historical Safe-proxy attribution, not a dedicated reward-distributor implementation. No address-authenticated Safe ABI was acquired. Thresholds, signer/module policy, payout automation and funding are not established here. |

The source chains are [stock-pool records](../assets/sources/stock-pools.json), including `sr-stock-hook-verified-abi-2026-10-20`, and [pilot records](../assets/sources/market-pilot.json). Creation and pending-Safe handover observations remain attributed historical research, not accepted ownership. Reuse the existing shared PoolManager and administrative-Safe evidence; a singleton address is neither a full PoolKey/PoolId nor an LP position.

In the existing binding schema, `interface_status: "complete_publisher_definition"` denotes complete coverage of the recorded interface definition, not the identity of its publisher. For the October20 hook binding that definition is the explorer-returned ABI; `review_id`, `source_ids` and the source chain establish explorer versus publisher provenance. The label does not certify deployed implementation.

## Effective fees and units

`stock-pool-fees` is **available for authenticated hook reads**, not a bundled client or a promise of swap execution. Use the packaged ABI when explorer retrieval is unavailable; failure to refetch an already-reviewed ABI is not itself missing encoding evidence. Missing current RPC, identity or pool coverage still limits the corresponding answer. Do not copy STANDARD TaxHook or launch-hook selectors, permissions or economics into this role.

| Read / layout | Meaning and required context |
| --- | --- |
| `poolManager()`; `pools(bytes32)` | Match the authenticated PoolManager and full ordered `PoolKey(currency0,currency1,fee,tickSpacing,hooks)`. `pools` returns one static tuple: `registered`, `paused`, `classId`, `resumedAt`, nested `override_(fee,expiry)`. An unregistered/default tuple is not a zero-fee supported market. |
| `classDefined(uint8)`; `classFees(uint8)` | Confirm the pool's class is defined; decode the fixed `uint24[4]` in source-backed session order: **0 Regular, 1 Extended, 2 Overnight, 3 Closed**. A default array alone is not a valid class. |
| `allPaused()`; `allResumedAt()` | Global swap gate and last global resume timestamp; combine with pool pause/resume state. `feeFor` does not enforce registration, class definition or pauses. |
| `feeFor(bytes32,address,uint256)` | Returns `(uint24 fee,uint8 session)` for the supplied PoolId, **hook callback sender** and Unix timestamp. The sender may be a router/swap contract, not the trader, beneficiary or `tx.origin`. Record the route assumption; do not substitute a wallet silently. |
| `feeExempt(address)`; `globalOverride()` | Sender exemption and global `(uint24 fee,uint64 expiry)`; compare with the pool override at the same state anchor. |
| `currentSession()`; `sessionAt(uint256)`; `sessionStart(uint256)` | Current or supplied-time session and UTC session-start seconds. The source's `sessionStart` search is bounded to seven days; it is not a complete historical calendar reconstruction. |
| `sessionTimes()`; `weeklyClosure()`; `dstMode()`; `openRamp()` | Mutable calendar/ramp configuration; layout and scales below. |
| `closures()`; `localDay(uint256)`; `holiday(uint32)`; `utcOffset(uint256)` | Dynamic array of `(uint64 start,uint64 end)` closures, Eastern holiday key, holiday flag and UTC-offset seconds. Include adjacent-day holiday context when explaining the session. |
| `owner()`; `pendingOwner()`; `operator()`; `initializer(address)` | Distinct structure owner, pending handover, anomaly operator and initialization permission. A pending owner is not accepted ownership. |

Numeric fees are **hundredths of one basis point**: divide by 100 for bps, 10,000 for percent, or 1,000,000 for the fractional rate. As an arithmetic illustration only, `450 = 4.5 bps = 0.045%`. PoolKey's dynamic-fee flag and the callback's override flag are not fee amounts. Launch-module/base-fee BPS have a different scale. No current fee table is installed; October16's schedule is historical after October19's class reassignment.

The inspected `feeFor` precedence is **sender exemption → maximum of active pool/global overrides → ramped class fee**. Active means the supplied timestamp is strictly before expiry; an override bypasses the class ramp. Without an override, a decrease interpolates down from the previous session fee over `openRamp` minutes with integer division; increases apply immediately. A later pool/global resume within the ramp uses the class's Closed fee as the prior fee. `beforeSwap` checks pool/global pauses first, then uses `feeFor` with `block.timestamp` and returns the override-flagged rate. Exemption does not bypass pauses. A returned fee/session alone proves neither a registered/defined market nor that the swap succeeds.

Pin related reads to a compatible chain/block number, hash and timestamp. Supplying a past/future `timestamp` to `feeFor` or `sessionAt` evaluates **the mutable configuration at the eth_call state block**, not the state that historically existed or will exist at that timestamp. Historical questions require the appropriate archive state and coverage; future-time evaluation is conditional, not a guaranteed future fee.

## Calendar, identity and event evidence

`MarketCalendar` establishes these decoding conventions; constructor settings are not current defaults:

- `sessionTimes()` returns `extendedOpen, regularOpen, regularClose, extendedClose`, all **minutes past Eastern local midnight**, not UTC timestamps. `openRamp()` is minutes. Schedule validation excludes edges in the ambiguous/skipped DST interval from 01:00 inclusive to 03:00 exclusive.
- `weeklyClosure()` returns `startDay, startMinute, endDay, endMinute`: weekday **0 Sunday through 6 Saturday**, local-midnight minutes, a recurring half-open `[start,end)` interval that wraps across the week when needed; equal week-minute endpoints disable it.
- `dstMode()` enum is **0 Auto, 1 Standard, 2 Daylight**. Auto applies US DST boundaries; forced modes retain their selected offset. `utcOffset(timestamp)` returns positive seconds **subtracted** from UTC to obtain Eastern wall time, not signed hours.
- `closures()` intervals and override/resume times are absolute Unix/UTC seconds. Closures are half-open `[start,end)`; holiday keys are Eastern calendar days since 1970-01-01. The calendar checks weekly/absolute closure and the day's holiday, plus the next day's holiday after extended close and the previous day's holiday before regular open. A pool's country label does not select a different clock.

Reuse a previously authenticated **full PoolKey**, validating its chain, PoolManager, hook and derived PoolId against the target observation, instead of repeating broad PoolManager initialization scans. If identity evidence is missing, use scoped publisher/registration evidence and bounded logs from authenticated creation/deployment bounds; report coverage and unresolved identities. `PoolRegistered(bytes32,(address,address,uint24,int24,address),uint8)` indexes the PoolId and carries the full key/class in data. Registration is not proof of PoolManager initialization or liquidity. A missing result from incomplete logs is not a nonexistent pool or zero fee.

The ABI also preserves `PoolClassSet`, `ClassFeesSet`, override/pause/calendar/exemption events and ownership handovers with exact indexed layouts. Relevant declared diagnostics include `PoolNotRegistered`, `ClassUndefined`, `PoolIsPaused`, `NotPoolManager`, `NotInitializer`, `WrongHook` and `NotDynamicFee`; their presence does not mean the fee view checks them all. Inspect emitter, canonical receipt and exact ABI layout before attributing a state change. No new log crawler or mandatory read wizard is implied.

## Income, points and settlement

`stock-pool-backing-and-income` remains unknown: a hook fee cannot prove issuer backing, legal share ownership, reserve custody, LP share, realized user income or an entire portfolio. Separate position ownership, fee growth, receipts, balances, complete relevant flows and issuer/legal evidence. Gross fee revenue and short-interval annualization are not realized LP yield.

`market-pilot-entitlement` also remains unknown from the reviewed factory/Config fee context. Preserve offchain-rule conflicts, mixed reward assets, liabilities and actual settlement evidence. A Safe address or one zero asset balance proves neither complete funding nor insolvency. The optional HTTP index described in [public market evidence](liquidity-markets.md#public-market-evidence) is discovery/source evidence, not an ABI-backed capability or a bundled client. No Safe event/error layouts are claimed here.
