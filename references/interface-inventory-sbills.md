# S-Bills launch interface

**Reviewed 2026-10-02; generation `launch-2026-10-01`.** This dated generation identifies deployment provenance, not a Solidity version. The [interface data](../assets/interfaces/sbills-launch-2026-10-01.json) preserves every entry in the selected frontend array: **36 functions, two events and 12 errors**, plus the source-only `Bill` declaration. Both source-definition-complete and deployed-implementation-complete are **false**. Full administration, constructors and lifecycle coverage remain unknown. See [S-Bills concepts](sbills.md), [capabilities](capabilities.md) and [identity records](../assets/entities/contracts.json).

## Acquisition and attribution

The [official staking page](https://www.standardreserve.xyz/app/staking/) links [mountApp-CRx6ba2l.js](https://www.standardreserve.xyz/assets/mountApp-CRx6ba2l.js), whose dependency map names [StakePage-UZsAeyx4.js](https://www.standardreserve.xyz/assets/StakePage-UZsAeyx4.js). Complete HTTP bodies were retrieved as data; downloaded JavaScript was never executed. The main module's `WP.sbills` binds the launch address; the chunk's `un`/`pn` use `X` with `contracts.sbills`.

| Artifact | UTF-8 bytes | SHA-256 |
| --- | ---: | --- |
| Staking HTML | 6652 | `d1083521e1199654ed10d221d4c61aaf5e49e26239eb393e04680f6436ab468a` |
| Main module | 863138 | `8921717a644cb4e67499a42e180767ac64dea88949da2afbc15bd7b32947633c` |
| Staking chunk | 37814 | `ef30d95dcbdde92c9f2ef443f892b80e89991a80df904796b11c323ab7403160` |
| `X=Ze([...])` declaration array | 2831 | `7ddd8d09e620b41176d8306ca0f9d4b63aed25f736576734eae09f0a01188d26` |

The exact array occupies zero-based half-open UTF-8 byte range `[29000,31831)` **in the staking chunk**, not the main module. JSON-compatible string literals were decoded without evaluation, then transcribed with an anchored declaration grammar. All 51 declarations are accounted for: one struct and 50 ABI entries. [Review `publisher-sbills-2026-10-02`](../assets/interfaces/reviews.json) records coverage and canonical ABI digest. [Source records](../assets/sources/sbills.json) preserve the page-to-chunk chain, exact role-binding fragment, creation/successful-deposit evidence and dated pinned observations; none are current configuration defaults. The September27 review and IDs remain unchanged.

Completed security reviews, confirmed by the developer, are **user-reported developer confirmation** (`sr-sbills-security-review-confirmation-2026-10-02`). No public report, reviewer, reviewed commit or source/runtime correspondence is invented. This does not change signing/submission boundaries.

## Units and state

Token amounts use publisher STANDARD18 denomination; corroborate `token()` and token decimals for the deployment. Rates are **WAD term fractions**, not token amounts or annual rates: `1e18 = 100% per term`. BPS fields use `10000 = 100%`. Timestamps and `term()` use seconds. Annualization needs an explicit convention and evidenced term; booked bills use their own `termStart`/`maturity`, not today's configuration.

Bill IDs are integers namespaced by **chain + contract + ID**; zero is valid. Do not collapse `active` and `settled`. Frontend bonus-accumulator and exit-pressure arithmetic is implementation guidance only, not verified Solidity rounding. Prefer same-block contract quotes for payout previews. Publisher sample-book fallback (`i?.book??Gt`) and local floating-point curve calculations must not supply live defaults when reads fail.

## Every selected function

All entries below are `view` except the four explicitly documented transactions. Exact input/output names, widths, selectors and qualifications live in the JSON alongside each entry.

| Canonical signature | Result / bounded purpose |
| --- | --- |
| `token()` | `address`: underlying token, not the Bank ledger. |
| `startTime()` | `uint64`: program Unix-time anchor for frontend exit-day indexing. |
| `term()` | `uint256`: configured seconds for new activity, not an existing bill's maturity. |
| `rate()` | `uint256`: stored WAD term-rate checkpoint. |
| `rateUpdatedAt()` | `uint64`: checkpoint Unix seconds. |
| `drifting()` | `bool`: reported drift state. |
| `driftPerSecond()` | `uint256`: WAD term-rate fraction per second; exact deployed arithmetic unproved. |
| `impactScale()` | `uint256`: STANDARD18 entry-amount impact input, not a capacity limit. |
| `floor()` | `uint256`: WAD term-rate floor. |
| `ceiling()` | `uint256`: WAD term-rate ceiling. |
| `totalPrincipal()` | `uint256`: STANDARD18 aggregate principal accounting. |
| `lockedPrincipal()` | `uint256`: STANDARD18 locked aggregate, distinct from total principal. |
| `bonusPerPrincipal()` | `uint256`: frontend WAD bonus accumulator interpretation; exact checkpoints unproved. |
| `exitFloorBps()` | `uint256`: BPS lower fee input, not Bank resolution fee. |
| `exitCapBps()` | `uint256`: BPS upper fee input, not the actual bill quote. |
| `exitWindowDays()` | `uint256`: number of program-relative 86400-second buckets in the frontend model. |
| `exitPressureFloor()` | `uint256`: STANDARD18 denominator-floor input in the frontend exit model. |
| `exitedOnDay(uint256)` | `uint256`: STANDARD18 exited amount for a program-relative day; not a maturity cohort getter. |
| `totalCap()` | `uint256`: STANDARD18 aggregate cap, not remaining capacity alone. |
| `walletCap()` | `uint256`: STANDARD18 wallet cap; compare pinned `principalOf`. |
| `minDeposit()` | `uint256`: STANDARD18 minimum amount; other constraints remain. |
| `paused()` | `bool`: reported pause flag; exact affected paths/authority unknown. |
| `closed()` | `bool`: reported closure flag; not proof all bills settled. |
| `budget()` | `uint256`: STANDARD18 premium budget, not holder principal or guaranteed yield. |
| `currentRate()` | `uint256`: current WAD term rate, distinct from stored rate and amount quote. |
| `principalOf(address)` | `uint256`: wallet STANDARD18 principal; not wallet token balance or bill count. |
| `bills(uint256)` | Eight flat outputs in order: `address owner, bool settled, bool active, uint128 principal, uint128 premium, uint64 termStart, uint64 maturity, uint256 bonusDebt`. |
| `billCount(address)` | `uint256`: owner-scoped count; no assumed global or active-only count. |
| `billsOf(address,uint256,uint256)` | `uint256[] ids`: owner/start/count page; dynamic offset and array length are not IDs. |
| `quote(uint256)` | `uint256 ratePaid, uint256 premium, uint256 rateAfter`: WAD, STANDARD18, WAD. |
| `quoteExit(uint256)` | `uint256 feeBps, uint256 fee, uint256 vested, uint256 forfeitedBonus, uint256 payout`: BPS then STANDARD18; forfeitures are not added to payout. |
| `quoteRedeem(uint256)` | `uint256 principal, uint256 premium, uint256 bonus, uint256 payout`: STANDARD18 previews, not executed settlement. |
| `deposit(uint256,uint256)` | **Nonpayable transaction**: amount STANDARD18 and minRate WAD; returns `uint256 id`. Frontend uses underlying token allowance. |
| `redeem(uint256)` | **Nonpayable transaction**: explicit bill redemption; no return values. Maturity does not execute it. |
| `exitEarly(uint256,uint256)` | **Nonpayable transaction**: bill ID and maxFeeBps protection; no return values. |
| `roll(uint256,uint256)` | **Nonpayable transaction**: bill ID and minRate WAD; no return values. Explicit manual roll, not auto-renewal. |

`quote(uint256)` has selector **`0xed1bd76c`** in both license and S-Bills interfaces. The license result has **two words**, the S-Bills result **three**. A selector alone cannot choose a decoder. `bills` is eight flat outputs, not an offset to the source-only `Bill` struct; its struct declaration is preserved and expanded in the interface data.

## Exact selected event layouts

```solidity
event Deposited(uint256 indexed id, address indexed owner, uint256 principal, uint256 premium, uint256 ratePaid, uint64 maturity)
event Exited(uint256 indexed id, address indexed owner, uint256 principal, uint256 fee, uint256 vestedForfeited, uint256 bonusForfeited)
```

Both are nonanonymous: topic0 is the event signature hash, topic1 the bill ID and topic2 owner. Each has four static ABI data words in listed order. Deposited reports booked principal/premium, WAD ratePaid and maturity seconds. Exited reports STANDARD18 principal/fee/forfeitures. Authenticate emitter, canonical log identity and receipt success; reconcile token flows for realized payout. No `Redeemed` or `Rolled` event is invented, and these two declarations do not establish complete lifecycle coverage.

For a calendar-day cohort, use stored `bills(id).maturity` in timezone-explicit `[start,end)` (state UTC when defaulted). Wallet pages are wallet-scoped. A global complete count requires authenticated full ID discovery, bounded Deposited coverage and pinned per-ID state with rollover/reuse/settlement reconciled; the frontend's 30-day indexer view is insufficient. Otherwise label an observed subset. See [cohort guidance](sbills.md) and [calculation recipes](calculations.md).

## Every selected error

All twelve have no arguments. Interpret these as name-derived guards, not proof of exact paths or authorization: `BelowMinDeposit()` (minimum), `WalletCapExceeded()` (wallet cap), `TotalCapExceeded()` (aggregate cap), `InsufficientBudget()` (premium budget), `NotBillOwner()` (ownership), `BillInactive()` (activity), `NotMatured()` / `AlreadyMatured()` (timing), `ClosedForBusiness()` (entry closure), `RateBelowMin()` (entry-rate protection), `FeeAboveMax()` (exit-fee protection), and `ContractPaused()` (pause).

No selected constructor, fallback or receive declaration appears. Because the interface is partial, that is not a claim that deployed code lacks these or any other entry. Administrative powers, reward funding paths and source/compiler correspondence remain open research questions.
