# Question-driven interface guide

**Reviewed 2026-09-27.** This is a question-driven summary, not the complete data inventory, a question whitelist, call sequence, deployment router or execution allowlist. The [full reviewed inventory](interface-inventory.md) now includes all identified protocol-role definitions in the complete publisher module, with explicit role gaps; [capabilities](capabilities.md) distinguishes available reads from scoped absences and unknowns. Authenticate the chain, emitting/called address, generation and block under [contracts](contracts.md#authenticate-the-requested-role). Other authenticated interfaces remain usable. No signing or submission is authorized here.

## Dated provenance

The official [application](https://www.standardreserve.xyz/app/) linked the complete [publisher module](https://www.standardreserve.xyz/assets/mountApp-z6PyBslD.js), reviewed as data without executing downloaded JavaScript: **860946 UTF-8 bytes**, SHA-256 `8e2178e9e11adc78288afeb0a95bf1c62e7ac118ba08986b3033c2d740cdbd31`. [Source records](../assets/sources/live-interface.json) `sr-question-interface-2026-09-27` and `sr-core-accrual-correspondence-2026-09-27` retain literal hashes, generation binding locators and the implementation-evidence limit. Earlier dated purchase/event and STANDARD/TaxHook source records remain independently scoped evidence, not superseded live state.

Scope keys below denote **reviewed roles/generations**, never address aliases:

| Key | Publisher ABI evidence and generation |
| --- | --- |
| K / N | Core CentralBank `Ne` / CharterNFT `Rn`; calls explicitly bind these literals to their roles. |
| S / H | STANDARD `Vs` / TaxHook `As`; relevant source mechanics additionally supported by `sr-standard-source-interface` / `sr-tax-hook-source-interface`. |
| L0 / C0 | Original license `jc` / charter `Ci`; historical role binding `VP` and original-generation records. |
| L11 | v1.1 license: `peripheryV11:GP` provenance and `b_` adapter remove named original definitions and add literal period/window declarations. |
| L12 / C12 | v1.2 license `vw` / charter `h_`; `peripheryV12:YP` provenance, with separate license/charter bindings. |
| L* / C* | Only layouts actually compared identical across L0/L11/L12 or C0/C12. Shared layout does **not** prove shared economic implementation. |

The reviewed v1.1 mapping replaces the **license** auction; it does not identify a separate v1.1 charter replacement. C0 is the charter interface retained through that publisher generation. The source's current-target override is not evidence that historical queries should use the current address. Historical addresses and activation/creation facts remain in dated source records, not this guide's call tables.

Deltas: `AUCTION_DAY()` is original; `auctionPeriod()` is L11/L12/C12. Original per-day license-cap methods are replaced by window methods in L11/L12. Order views/events below are L12 only. `DECAY_HALF_LIFE_MAX()` is removed from the newer license and charter ABIs; no guessed replacement is supplied. `dayAnchorTime()` is absent from the reviewed complete auction ABIs: the authenticated schedule input is `auctionAnchor()`.

## Question map

Choose the evidence needed for the question; these are examples, not mandatory steps.

| Question | Entries | Remaining distinction or gap |
| --- | --- | --- |
| How many branches, whose charter, how much pending? | [Core state](#core-state): `totalBranches`, `branchCountOf`, `ownerOf`, `pendingOf`, `charters` | Unsold inventory is separate; current owner is not historical buyer; pending is not verified earned funding. |
| What could accrue over an interval? | [Accrual inputs](#accrual-inputs), epoch/branch events below | Full accumulator/checkpoint/rounding and deployment correspondence remain unestablished; see [accrual evidence](research-workflow.md#accrual-evidence). |
| Is this an earned-only budget? | [Ledger/ownership events](#ledger-and-ownership-events), purchase events, anchored balances and checkpoints | Complete deposit/spend/withdrawal/transfer history and origin-consumption rules are needed; mixed origins may remain indeterminate. See [earned-only accounting](research-workflow.md#earned-only-projections-and-reinvestment). |
| What can be bought, at what price and when? | [Separate auction families](#auction-state), [license allowance/orders](#allowance-and-orders), `MAX_BRANCHES` and family-specific funding | A new ETH-priced charter is not a STANDARD-funded branch-license expansion. Inventory, allowance, capacity, ownership, pause and funds are independent; see [purchase constraints](research-workflow.md#fixed-price-and-windowed-purchases). |
| When can this charter buy one branch license from accrued STANDARD, using historical license sales? | [Inventory/next-window gate](auctions.md#current-license-availability-and-next-opportunity), `pendingOf`, charter constraints, [historical executions](auction-history.md), [empirical pace](research-workflow.md#empirical-pending-delta-pace) and [dilution scenarios](research-workflow.md#dilution-scenarios) | Sold-out is not buyable now. Pending is not earned-origin proof; historical prints are not the live ask. Separate policy opening, repeat-demand and still-unsold scenarios; clip to evidenced epoch/issuance limits. |
| What orders exist or filled? | `openBidCount`, `openBids`, `bids`, `fillable`, bid/purchase events | Raw page IDs need authenticated interpretation; bidder need not be current owner. Limit, current ask and settled price differ. |
| What actually sold or changed? | [Auction events](#auction-events), [history](auction-history.md) | Receipt/canonicality/coverage and historically effective settings are required; no-sale average is undefined. |
| Is the token restriction enabled, active, or applicable? | [Restrictions](#restrictions) | Enabled, resolved active and the separate gate are not interchangeable; flags do not prove a particular transfer succeeds. |

## Encoding and decoding

Tables give **full canonical signatures**; argument names appear separately in ABI order. A function selector is the first four bytes of **Ethereum Keccak-256** of the UTF-8 signature; an event topic0 is all 32 bytes. Return types, argument names and `indexed` are not hashed. Use an Ethereum ABI library or authenticated `web3_sha3` over the signature's UTF-8 hex. NIST `SHA3-256` (including Python `hashlib.sha3_256`) is **not** Ethereum Keccak. Derivation checks: `transfer(address,uint256)` → `0xa9059cbb`; `Transfer(address,address,uint256)` → `0xddf252ad1be2c89b69c2b068fc378daa952ba7f163c4a11628f55a4df523b3ef`.

Call data is selector followed by ABI arguments. For these static inputs, each occupies a 32-byte word: unsigned integers/bools zero-padded, addresses right-aligned; `int256` is signed two's-complement. Outputs have **no selector**. A flat multiple-return tuple such as `charters(uint256)` is three consecutive words `(branchCount,storedPending,rewardDebt)`; `quote(uint256)` is two, and `bids(uint256)` is `(address bidder,uint256 count,uint256 maxUnitPrice)`, not an offset to another tuple. Preserve exact integers; apply evidenced scales only for presentation.

`openBids(uint256,uint256)` returns one **dynamic** `uint256[]`: word0 is a byte offset from the beginning of return data (normally `0x20`); at that offset is the element count, followed by that many 32-byte IDs. The offset is not the first ID, and neither the offset nor length is a charter ID. Respect offsets/bounds rather than taking every word as an element. ABI parameter names explicitly identify `bids`/`fillable` inputs as `charterId`; `openBids` names its output only `ids`. A successful `bids(rawId)` call does not authenticate the join, page ordering, completeness or stable pagination. Existing publisher order reads use already-known charter IDs, not a proven raw-page mapping.

All listed events are nonanonymous. Indexed fields occupy topic1 onward in listed order; nonindexed fields occupy consecutive 32-byte data words in listed order. The two `Transfer(address,address,uint256)` layouts have **the same topic0 but different indexing**: NFT tokenId is topic3; ERC20 value is data word0. Authenticate emitter/role before decoding. Empty data is valid only where shown. Filter/log existence alone is not receipt success or a complete history claim.

**Use full event declarations, not signature-only strings, to build a decoder.** A canonical signature supplies topic0 but deliberately omits names and `indexed`. Every [inventory entry](interface-inventory.md#data-layout-and-event-decoding) supplies the complete `abi`, an explicit `declaration`, and a structural `event_layout`. These examples expose the location distinction directly:

```solidity
event LicensesPurchased(uint256 indexed charterId, uint256 indexed day, uint256 count, uint256 unitPrice)
event CharterPurchased(uint256 indexed charterId, address indexed buyer, uint256 indexed day, uint256 price)
event CheckedIn(address indexed wallet)
event Transfer(address indexed from, address indexed to, uint256 indexed tokenId) // CharterNFT
event Transfer(address indexed from, address indexed to, uint256 value) // STANDARD
```

For `LicensesPurchased`, topics 1/2 contain charterId/day and data contains count/unitPrice. For `CharterPurchased`, topics 1/2/3 contain charterId/buyer/day and data contains only price. `CheckedIn` has one indexed wallet and **empty data**. Passing a signature-only declaration to a decoder can incorrectly expect topic fields in data. Keep the authenticated emitter/role and full indexed layout with the log.

## Units and semantic limits

- **Encoding evidence is not economic implementation evidence.** Complete publisher ABI literals authenticate types and bounded public-read decoding. Source-linked runtime correspondence, dependencies, checkpoints, rounding and effective historical settings require separate proof. The 2026-09-27 core runtime/metadata investigation did not retrieve the matching CentralBank implementation; no accrual formula is certified here.
- **Publisher denomination evidence:** license prices, quote values, bid limits, pending/deposit displays use STANDARD with 18 decimal places; charter prices use ETH with 18 decimal places (wei). The bundle's `s8 → Ct(value,18) → Wd` formatting chain and license/charter labels establish displayed scales; `Yy`/`Hu` additionally trace bid limits. This corrects the earlier bid-limit *display-scale* gap, not escrow/refund/fill semantics. STANDARD `decimals()` separately authenticates token scale. Do not copy the frontend's conversion to floating-point for financial arithmetic.
- **Counts/IDs** are unscaled integers. `MAX_BRANCHES` is a capacity input, not a balance. Round/window IDs, charter IDs and raw order-page IDs are different domains even when all are `uint256`. `startMultiplier` is multiplied directly as an integer in publisher pricing; it is not `multiplierWad`.
- **Clock/display evidence:** publisher `yr` and `XC` use block Unix seconds, `auctionAnchor`, period and cap window; time display multiplies timestamps by 1000 and splits durations by 3600/60. This supports units and the publisher's scheduled-window interpretation, not Solidity reset/lazy-roll behavior. Getter names containing `Day` are not proof of a 24h duration. Missing effective historical settings block exact past windows. See [purchase/time semantics](research-workflow.md#fixed-price-and-windowed-purchases) and [auction history](auction-history.md).
- **Accrual:** publisher `re → Ct(value,18)` displays pending as STANDARD18; `EO/Pf` displays the frontend-modeled charter rate as STANDARD18/second, and `z1` displays `multiplierWad` at 18-decimal scale. This does **not** establish the exact components/units of the `currentStreamRatePerSecond()` getter or Solidity accrual. `accPerBranch`, `rewardDebt`, `issuanceStreamed`, `recycleStreamed` remain raw internal values where scale/rounding is unproved. Pending, spendable ledger, wallet tokens and net withdrawable amounts are separate. A preview fee is not a withdrawal-success guarantee. See [accrual evidence](research-workflow.md#accrual-evidence).
- **Events/accounting:** publisher event-denomination evidence supports license STANDARD consideration and charter ETH price; core ledger events expose distinct amount/cost/gross/net/bounty fields, not independently reconciled transfers. `feeWad` is a WAD-labelled field; authenticate its arithmetic use rather than treating a fee fraction as a token amount. `ParamQueued`/`ParamApplied` use opaque `bytes32` keys; no key-to-policy mapping is invented. Apply [ledger accounting](research-workflow.md#earned-only-projections-and-reinvestment) and [history rules](auction-history.md), including canonical deduplication and no double-counting supporting logs.
- **Limits deliberately retained:** no core source/bytecode equivalence; no independently proved accrual eligibility/rounding or mixed-origin consumption order; no proven allowance reset implementation, FCFS, escrow/refunds, keeper permissions, expiry or guaranteed fill; no universal authorization/transfer-success claim; no complete historical coverage. No saved balances, prices, rates, ownership or active deployment defaults.

## Core state

All functions in the state/input sections are `view`. Parenthesized returns below describe ABI output order, not an extra encoded wrapper. K/N/H administrative `owner()` differs from N `ownerOf(tokenId)`.

| Canonical signature · selector | Argument names → return layout | Scope; qualification |
| --- | --- | --- |
| `totalBranches()` · `0x95c90089` | `—` → `(uint256)` | K; branch count, not unsold licenses |
| `branchCountOf(uint256)` · `0xe1b8a032` | `charterId` → `(uint256)` | K; selected charter branch count |
| `pendingOf(uint256)` · `0x7e7feaa7` | `charterId` → `(uint256)` | K; reported pending ledger; not earned-origin proof |
| `charters(uint256)` · `0xd27211a6` | `charterId` → `(uint256 branchCount, uint256 storedPending, uint256 rewardDebt)` | K; stored checkpoint tuple; accumulator scaling unverified |
| `MAX_BRANCHES()` · `0xe5301bf6` | `—` → `(uint256)` | K; capacity input; authenticate per-charter enforcement |
| `previewResolutionFeeWad(uint256)` · `0x01e275a7` | `gross` → `(uint256)` | K; fee preview input/output; not a complete withdrawal quote |
| `ownerOf(uint256)` · `0x6352211e` | `tokenId` → `(address)` | N; current-at-block owner, not sale-time buyer |
| `lastTransferred(uint256)` · `0x9bc34afe` | `tokenId` → `(uint256 timestamp)` | N; publisher timestamp field; reset/grace semantics unverified |
| `transfersEnabled()` · `0xbef97c87` | `—` → `(bool)` | N |
| `owner()` · `0x8da5cb5b` | `—` → `(address)` | K/N/H/L*/C*; module administrator, not charter owner |
| `pendingOwner()` · `0xe30c3978` | `—` → `(address)` | K/N/H/L*/C*; proposed handoff; acceptance is separate |
| `balanceOf(address)` · `0x70a08231` | `account` → `(uint256)` | S; wallet token balance, separate from pending ledger |
| `decimals()` · `0x313ce567` | `—` → `(uint8)` | S; uint8 scale observation |
| `allowance(address,address)` · `0xdd62ed3e` | `owner, spender` → `(uint256)` | S; token spending approval, not license window allowance |

## Accrual inputs

Combine only authenticated semantics at a common anchor; queued values are not active inputs. These fields identify the evidence needed, not a universal earnings formula.

| Canonical signature · selector | Argument names → return layout | Scope; qualification |
| --- | --- | --- |
| `emissionsStarted()` · `0x5adf0021` | `—` → `(bool)` | K |
| `currentStreamRatePerSecond()` · `0x708a0dd0` | `—` → `(uint256)` | K; raw reported stream; exact components/units unverified, not per-charter earnings |
| `issuanceRate()` · `0x3c9ae2ba` | `—` → `(uint256)` | K |
| `recycleRate()` · `0xb55795e3` | `—` → `(uint256)` | K |
| `accPerBranch()` · `0x100513c6` | `—` → `(uint256)` | K; raw accumulator; denominator/scale/rounding unverified |
| `lastAccrual()` · `0x7b3baab4` | `—` → `(uint256)` | K; checkpoint time input, not a complete checkpoint algorithm |
| `epochNumber()` · `0xf4145a83` | `—` → `(uint256)` | K |
| `epochStart()` · `0x15e5a1e5` | `—` → `(uint256)` | K |
| `epochEnd()` · `0x4bb6b58f` | `—` → `(uint256)` | K |
| `issuanceEnd()` · `0x79b5fd86` | `—` → `(uint256)` | K |
| `epochDays()` · `0x63652bd1` | `—` → `(uint256)` | K |
| `baseIssuancePerDay()` · `0x17388786` | `—` → `(uint256)` | K |
| `multiplierWad()` · `0x47481b0b` | `—` → `(uint256)` | K |
| `issuanceStreamed()` · `0x2751708f` | `—` → `(uint256)` | K; raw internal ledger scale unverified |
| `recycleStreamed()` · `0x73a7cd78` | `—` → `(uint256)` | K; raw internal ledger scale unverified |
| `queuedEpochDays()` · `0x41b3e64b` | `—` → `(uint256 value, bool pending)` | K; pending flag distinguishes proposed from active |
| `queuedBaseIssuancePerDay()` · `0xa3cdd9d4` | `—` → `(uint256 value, bool pending)` | K; pending flag distinguishes proposed from active |

### Optional observation series

For a requested pace/dilution investigation, preserve `currentStreamRatePerSecond()`, `totalBranches()` and the selected charter's `pendingOf()` at the **same identified block**, with its header timestamp. Retain exact raw units and the charter ID. These three values form a compact joint series, not a sufficient proof of earnings or a required preflight for unrelated questions. Add branch count, epoch/issuance boundaries and covered flow history only as needed for the proposed interpretation. Keep observations in an authorized external record, never in installed defaults; do not start unsolicited polling or a standing watch.

The stream's changing drivers remain an explicit research question. Issuance schedules, fee/recycling flows, component stops and administrative changes are possible hypotheses to investigate—not explanations established by a name or a two-point trend. Pin relevant components, settings, events and implementation evidence before attributing a change. `rawStream × 86400` remains raw-unit-per-day arithmetic unless its denomination and components are authenticated or explicitly assumed in a scenario.

Under an expressly assumed pro-rata model, falling aggregate stream and rising eligible branch count both reduce per-branch pace. A changed relevant stream/denominator observation requires re-anchoring a claim about current pace; an older anchored scenario remains a valid historical scenario, not an automatically refreshed forecast. [Empirical pending deltas](research-workflow.md#empirical-pending-delta-pace) and [two-series scenarios](research-workflow.md#dilution-scenarios) provide labelled ways to proceed without certifying Solidity behavior.

## Auction state

**CHARTER AUCTION and BRANCH-LICENSE AUCTION are separate families.** Resolve the intended family from context; ask only if it remains ambiguous. Each observation is scoped by family, chain, generation, address and block. Proven identical encoding is shared below for compactness, **not** schedules or economics.

| Dimension | Branch-license auction: L0/L11/L12 | Charter auction: C0/C12 |
| --- | --- | --- |
| Role | Add purchased branches/licenses to an existing charter. | Acquire a new charter. |
| Schedule | Own `auctionAnchor`; L0 `AUCTION_DAY`, L11/L12 `auctionPeriod`. Its allowance `capWindow` is separate again. | Own `auctionAnchor`; C0 `AUCTION_DAY`, C12 `auctionPeriod`. No license allowance is imported. |
| Inventory | Own `licensesPerDay`, `dayCap`, `soldToday`, `remainingToday`; counts are licenses, not existing branches. | Own `chartersPerDay`, `dayCap`, `soldToday`, `remainingToday`; counts are charters, not licenses. |
| Prices/floor | Own `currentPrice`, day prices, `lastSalePrice`, `startMultiplier`, half-life and `floorPaybackDays`; publisher STANDARD18 denomination. | Own `currentPrice`, day prices, `lastSalePrice`, `startMultiplier`, half-life and `charterReservePrice`; ETH wei. |
| Funding/constraints | Publisher STANDARD ledger funding; authenticate usable pending, license window allowance, branch capacity and owner/eligibility. Wallet token approval/deposit is a distinct flow. | ETH funding; authenticate payable value, price, refund/fees and charter-specific eligibility. Earned STANDARD is not ETH unless a verified conversion is explicitly modeled. |
| Purchase event | `LicensesPurchased(charterId,day,count,unitPrice)`; gross consideration is `count × unitPrice`. | `CharterPurchased(charterId,buyer,day,price)`; one event identifies one charter and its reported ETH sale price. |

No implicit shared 12h schedule, 2×/3× multiplier, floor, cap, inventory or payment asset follows from matching getter names. Read the chosen family's settings independently. Scheduled windows, allowance windows and rolling 24h horizons are distinct.

For L* price fields use publisher STANDARD18 denomination; for C* use ETH wei. Inventory and price-function output do not by themselves establish a purchasable quote. Stored round/counters may describe a materialized round; do not silently replace them with frontend-projected rollover state.

| Canonical signature · selector | Argument names → return layout | Scope; qualification |
| --- | --- | --- |
| `started()` · `0x1f2698ab` | `—` → `(bool)` | L*/C* |
| `paused()` · `0x5c975abb` | `—` → `(bool)` | L*/C* |
| `auctionAnchor()` · `0xf08fb30f` | `—` → `(uint256)` | L*/C*; publisher schedule timestamp; not each roll log time |
| `currentDay()` · `0x5c9302c9` | `—` → `(uint256)` | L*/C*; stored round ID; not a human calendar day |
| `currentPrice()` · `0x9d1b464a` | `—` → `(uint256)` | L*/C*; price-function output, not executable quote |
| `dayStartPrice()` · `0x28db9dd5` | `—` → `(uint256)` | L*/C* |
| `dayFloorPrice()` · `0x55d92de0` | `—` → `(uint256)` | L*/C* |
| `dayHalfLife()` · `0x7b314af7` | `—` → `(uint256)` | L*/C* |
| `dayCap()` · `0xfea8c07c` | `—` → `(uint256)` | L*/C* |
| `soldToday()` · `0xa08c6922` | `—` → `(uint256)` | L*/C* |
| `remainingToday()` · `0xfc3c5515` | `—` → `(uint256)` | L*/C*; reported inventory; not total open branches |
| `lastSaleDay()` · `0x5bb3ae5c` | `—` → `(uint256)` | L*/C* |
| `lastSalePrice()` · `0x86f5960f` | `—` → `(uint256)` | L*/C*; getter observation, not receipt-verified sale |
| `decayHalfLife()` · `0x9813048a` | `—` → `(uint256)` | L*/C* |
| `startMultiplier()` · `0x6d9c3033` | `—` → `(uint256)` | L*/C*; publisher uses integer multiplier, not WAD |
| `licensesPerDay()` · `0x92453404` | `—` → `(uint256)` | L*; configured per-round supply; retained name is not 24h volume |
| `floorPaybackDays()` · `0x56fa6aae` | `—` → `(uint256)` | L*; publisher floor-model input; not guaranteed investment payback |
| `quote(uint256)` · `0xed1bd76c` | `count` → `(uint256 unitPrice, uint256 total)` | L*; count input; unit price and total are not a fill guarantee |
| `chartersPerDay()` · `0xf5aa1276` | `—` → `(uint256)` | C*; configured per-round supply |
| `charterReservePrice()` · `0xffd741f9` | `—` → `(uint256)` | C*; ETH-denominated reserve price |
| `AUCTION_DAY()` · `0xb2b2b29c` | `—` → `(uint256)` | L0/C0; original-generation duration; do not substitute 24h |
| `auctionPeriod()` · `0x0cccfc58` | `—` → `(uint256)` | L11/L12/C12; generation-specific duration; do not hardcode 12h |

## Allowance and orders

Keep allowance-window usage separate from round inventory and branch capacity. A duration read does not alone prove reset alignment; publisher display uses the anchor, but implementation remains a separate claim.

| Canonical signature · selector | Argument names → return layout | Scope; qualification |
| --- | --- | --- |
| `MAX_PER_CHARTER_PER_DAY()` · `0x7e1db70f` | `—` → `(uint256)` | L0 |
| `purchasedOnDay(uint256,uint256)` · `0xfeaf3a72` | `charterId, day` → `(uint256)` | L0; charterId and auction day, original ABI only |
| `capWindow()` · `0xe5de0416` | `—` → `(uint256)` | L11/L12; allowance duration, separate from auctionPeriod |
| `capWindowIndex()` · `0x030adf57` | `—` → `(uint256)` | L11/L12; reported allowance-window ID |
| `MAX_PER_CHARTER_PER_WINDOW()` · `0x3a379145` | `—` → `(uint256)` | L11/L12 |
| `purchasedInWindow(uint256,uint256)` · `0xf66181f4` | `charterId, window` → `(uint256)` | L11/L12; charterId and window ID, not arbitrary rolling 24h |
| `remainingForCharter(uint256)` · `0xd80fc366` | `charterId` → `(uint256)` | L11/L12; reported charter allowance, not funds affordability |
| `openBidCount()` · `0x0e337f95` | `—` → `(uint256)` | L12; global count, not my orders |
| `openBids(uint256,uint256)` · `0x3b87f7bd` | `start, count` → `(uint256[] ids)` | L12; dynamic raw ID array; ID-to-charter interpretation unresolved |
| `bids(uint256)` · `0x4423c5f1` | `charterId` → `(address bidder, uint256 count, uint256 maxUnitPrice)` | L12; charterId input explicitly authenticated; limit is not executed price |
| `fillable(uint256)` · `0x4f071557` | `charterId` → `(bool)` | L12; point-in-time bool, not promised keeper fill |

### Current license quote and orderbook

For “can I buy now?”, first establish the relevant license generation's effective inventory/round and binding charter constraints under [current availability](auctions.md#current-license-availability-and-next-opportunity). A sold-out round is closed to purchases: `currentPrice()`/`quote(count)` may still return curve output, but that is not a buyable ask. A price below pending does not undo zero inventory. Keep a historical exhausted round separate from a possibly replenished effective window.

Where inventory remains, authenticated same-block `currentPrice()` and `quote(count)` provide the auction's price-function/quote output; they do not certify eligibility, funding, final execution or future price. A historical fill is a different comparator. Do not enumerate the orderbook merely to obtain this quote, and do not turn an affordability question into unsolicited bid/keeper advice.

When the user actually asks for the book, `openBidCount()` and bounded `openBids(start,count)` pages expose reported count and raw IDs. Apply the dynamic-array layout above and report page coverage. Join a raw ID to `bids(charterId)` only with independent evidence of that mapping; otherwise leave the join unresolved, or read a separately authenticated charter ID. A successful numeric lookup is not mapping proof. `fillable(charterId)` is a point-in-time flag for an authenticated input, not guaranteed execution or a way to discover the ask.

Report bidder, quantity and `maxUnitPrice` only for evidenced joins. Highest bid is not the executable ask; a limit is not a fill price. Receipt-verified `LicensesPurchased.unitPrice` establishes the reported execution price. Output a block-pinned, coverage-qualified quote/book snapshot or the precise unavailable claim—such as “no authenticated current executable ask”—without converting unknown IDs, funding or availability into a fill guarantee.

## Restrictions

The dated STANDARD source says active holding cap additionally resolves Registry TAX_HOOK and its launch schedule; enabled is not active. The dated Hook source says schedule active is false after override, true if start is zero, otherwise true only before start plus duration. The gate is independent. Refresh deployment correspondence and the resolved Hook relationship; do not synthesize active from an unrelated Hook. See the two source records linked above.

| Canonical signature · selector | Argument names → return layout | Scope; qualification |
| --- | --- | --- |
| `launchHoldingCapEnabled()` · `0x7f196059` | `—` → `(bool)` | S; configuration switch, distinct from active |
| `launchHoldingCapActive()` · `0x0b204113` | `—` → `(bool)` | S; source-reviewed resolved restriction result |
| `LAUNCH_HOLDING_CAP()` · `0x361d0f10` | `—` → `(uint256)` | S; STANDARD18 cap amount |
| `poolManagerGateEnabled()` · `0x52451a9c` | `—` → `(bool)` | S; independent gate, not universal transfer success |
| `launchScheduleActive()` · `0x2bb11c41` | `—` → `(bool)` | H; source-reviewed schedule flag, not inferred from current tax rate |
| `taxOverridden()` · `0xdd2365c8` | `—` → `(bool)` | H |
| `taxDecayStart()` · `0x70cdbb24` | `—` → `(uint256)` | H |
| `taxDecayDuration()` · `0x45e9dc6c` | `—` → `(uint256)` | H |
| `taxHalfLife()` · `0xdd037d05` | `—` → `(uint256)` | H |
| `currentTaxBps(bool)` · `0xa578d578` | `isBuy` → `(uint256)` | H; isBuy=true buy; false sell; basis points |

## Transaction inputs

For decoding historical inputs or host-authorized unsigned preparation only, **not signing/submission**. All below are `nonpayable` except `buyCharter`, which is `payable`. Empty return layouts are shown explicitly. Permission, value, approvals, refunds and successful execution are not established by an ABI; event accounting remains separate from submitted limits or transaction value.

| Canonical signature · selector | Argument names → return layout | Scope; qualification |
| --- | --- | --- |
| `deposit(uint256,uint256)` · `0xe2bbb158` | `charterId, amount` → `(no return)` | K |
| `withdraw(uint256,uint256,uint256)` · `0xa41fe49f` | `charterId, count, maxFeeWad` → `(no return)` | K |
| `openBranches(uint256,uint256,uint256)` · `0xe5f06261` | `charterId, count, cost` → `(no return)` | K |
| `revoke(uint256)` · `0x20c5429b` | `charterId` → `(no return)` | K |
| `buyLicenses(uint256,uint256,uint256)` · `0x6d11c8ec` | `charterId, count, maxUnitPrice` → `(no return)` | L* |
| `buyCharter(uint256)` · `0x655a8852` | `maxPrice` → `(uint256 id)` | C* |
| `placeBid(uint256,uint256,uint256)` · `0x5e62be25` | `charterId, count, maxUnitPrice` → `(no return)` | L12 |
| `cancelBid(uint256)` · `0x9703ef35` | `charterId` → `(no return)` | L12 |
| `fill(uint256)` · `0x3fda5389` | `charterId` → `(no return)` | L12 |
| `pruneBid(uint256)` · `0xd580289b` | `charterId` → `(no return)` | L12 |

## Ledger and ownership events

K purchase/deposit/withdrawal events, N ownership changes and S token/ceiling events are different ledgers. Withdrawals/retirements/transfers can alter future eligibility and ownership attribution; event names alone do not prove an accumulator update rule. No complete earned-origin budget follows from observing only some of them.

| Canonical signature · topic0 | Indexed topics after topic0 | Data words in order | Scope; qualification |
| --- | --- | --- | --- |
| `CharterCreated(uint256,address)`<br>`0xa07694e6f3d67919253eb27a138a6aa6b5e10c316a4be927b34b93b97942d2c5` | `uint256 charterId, address to` | `empty` | K |
| `BranchesOpened(uint256,uint256,uint256)`<br>`0xfca0d4c142a1e3085d891c92cde8193ccd316ff4ba9bb3f6b439136681115856` | `uint256 charterId` | `uint256 count, uint256 cost` | K; cost is total ledger consideration; do not add again to purchase consideration |
| `Deposited(uint256,address,uint256)`<br>`0x1599c0fcf897af5babc2bfcf707f5dc050f841b044d97c3251ecec35b9abf80b` | `uint256 charterId, address from` | `uint256 amount` | K; external ledger inflow, not earned emissions |
| `Withdrawn(uint256,address,uint256,uint256,uint256,uint256)`<br>`0x34b356a06378218b842d641adfef56661747ff542e604819d252280127354123` | `uint256 charterId, address to` | `uint256 branchesDestroyed, uint256 gross, uint256 feeWad, uint256 net` | K; branchesDestroyed is quantity; gross/net/fee are distinct |
| `Revoked(uint256,address,address,uint256,uint256,uint256)`<br>`0x5b0e4c8ef83b965c0909af73beae99d4f828ad85638330683305c9f010d4ad78` | `uint256 charterId, address owner, address informant` | `uint256 gross, uint256 bounty, uint256 ownerNet` | K; gross/bounty/ownerNet; authenticate branch retirement/recipient effects |
| `EmissionsStarted(uint256,uint256,uint256)`<br>`0xa5070e99edd98e4038d988d53032ab30c5ab97ca9dbe3f4e1dc5013e9eb16cf4` | `uint256 genesisTime, uint256 firstEpochEnd` | `uint256 foundingMinted` | K |
| `EpochSettled(uint256,int256,uint256)`<br>`0x2d8f8db7fbfa12fe7bf24542012ebba583e95870e8bcd9e170829fb8817fda12` | `uint256 epoch` | `int256 netFlow, uint256 multiplierWad` | K |
| `FeesRecycled(uint256,uint256)`<br>`0xee894dd54fd65a2c69a3247565cfcf3f64c9e468076fe25a53b9510e2b22fb44` | `uint256 epoch` | `uint256 amount` | K |
| `IssuanceDistributed(uint256,uint256)`<br>`0x2042733f30f10cce285e8815ec0b038aac71e397bffa1c75879d7f19087307fe` | `uint256 epoch` | `uint256 amount` | K |
| `ParamQueued(bytes32,uint256)`<br>`0x6744f301e3b4719cfc5e0cb3052c6b55620d7365a5f402f6873d1ab664a6a9e4` | `bytes32 param` | `uint256 value` | K; param key meaning/effective policy requires evidence |
| `ParamApplied(bytes32,uint256)`<br>`0x05a58552de4812137f36bf3cb999e5874ee36b1470a3f6fef12f39d56fce60de` | `bytes32 param` | `uint256 value` | K; key-to-setting mapping required; queue event is not activation |
| `Transfer(address,address,uint256)`<br>`0xddf252ad1be2c89b69c2b068fc378daa952ba7f163c4a11628f55a4df523b3ef` | `address from, address to, uint256 tokenId` | `empty` | N; tokenId is indexed topic3; owner-at-event, including zero-address transitions |
| `Transfer(address,address,uint256)`<br>`0xddf252ad1be2c89b69c2b068fc378daa952ba7f163c4a11628f55a4df523b3ef` | `address from, address to` | `uint256 value` | S; value is data word0; same topic0 as NFT Transfer, different indexing |
| `BurnedForever(address,uint256,uint256)`<br>`0x19ca53334e436c3b55a7161dc5b0d70a5f814b5098baf60ac6fb41a85582ea3d` | `address from` | `uint256 amount, uint256 newMaxSupply` | S; source-reviewed ceiling reduction; not every zero-address transfer |
| `LedgerRetired(uint256,uint256)`<br>`0x518e3c9b8c7465a08beed0ced51ff01865ae7cf9bf3e8de0b692e66bc63bb0d7` | `none` | `uint256 amount, uint256 newMaxSupply` | S; source-reviewed ceiling reduction without token balance movement |
| `OwnershipTransferStarted(address,address)`<br>`0x38d16b8cac22d99fc7c124b9cd0de2d3fa1faef420bfe791d8c362d765e22700` | `address previousOwner, address newOwner` | `empty` | K/N/H/L*/C* |
| `OwnershipTransferred(address,address)`<br>`0x8be0079c531659141344cd1fd0a4f28419497f9722a3daafe3b4186f6b6457e0` | `address previousOwner, address newOwner` | `empty` | K/N/H/L*/C* |

## Auction events

Layouts below are compared across the indicated generations; round identity remains `(family, chain, emitting address, day)`. `DayRolled` supplies no scheduled opening/closing timestamp. No reviewed dedicated `AuctionEnded` or `SoldOut` event is supplied; infer neither from the last sale alone. Configuration logs require historically effective application semantics; these ABIs contain no period/cap-window change event to invent. Multiple purchase/supporting/bid logs in one receipt are not multiple independent purchases. Direct-to-auction transaction lists can miss internally invoked purchases: verify the actual emitting logs and coverage rather than filtering only by transaction destination.

### Branch-license auction events

L* prices/consideration below use publisher STANDARD18 ledger denomination; caps/counts are licenses. Keep this history separate from charter sales even where roll/configuration topic0 matches.

| Canonical signature · topic0 | Indexed topics after topic0 | Data words in order | Scope; qualification |
| --- | --- | --- | --- |
| `AuctionStarted(uint256,uint256)`<br>`0xf8910119ddbef5440c54532457dfe8250a10ed39e583292818f44724b9e1344c` | `uint256 day` | `uint256 startPrice` | L* |
| `DayRolled(uint256,uint256,uint256,uint256)`<br>`0xfe150722db0c02a69373b1d32f7d153b415b253b5bce66b95e7b1f5d9ce65c3f` | `uint256 day` | `uint256 startPrice, uint256 floorPrice, uint256 cap` | L*; no timestamp, duration, or end reason |
| `LicensesPurchased(uint256,uint256,uint256,uint256)`<br>`0x01862d9110233f6709760be3b1cc45660f4b8b0698777de996e5a7d262638fb5` | `uint256 charterId, uint256 day` | `uint256 count, uint256 unitPrice` | L*; count × unitPrice is consideration, not tx value |
| `DecayHalfLifeSet(uint256)`<br>`0x3491d4ab69d4f73c3d81521a7c13c6f4299f2216ed9b9cc044949888cf5824f2` | `none` | `uint256 halfLife` | L* |
| `FloorPaybackDaysSet(uint256)`<br>`0x691f93bd194840bb74533b5aed16bbd924ff2bc0ec442c57dd485756bca7f809` | `none` | `uint256 dayCount` | L* |
| `LicensesPerDaySet(uint256)`<br>`0xffd007b9d15a275ab5c27e6639f90191a9e16b633d8452c70b199dd4366dc6b7` | `none` | `uint256 count` | L* |
| `GuardianPaused(address)`<br>`0xd5354f32595d4786b7a234166bc1e34f4ee58f9e9d534b0fc5abd8e122f25fd5` | `address guardian` | `empty` | L* |
| `GuardianUnpaused()`<br>`0x984d636c2614e303400b04f078fb33065fa357cbc6859737a5e4528627f4fa18` | `none` | `empty` | L* |
| `SupplyControllerSet(address)`<br>`0x915d8b94cdcbf4fa1b4c768b15f63b99aee21096b9d04fe1938f45833036106d` | `none` | `address controller` | L*; controller is nonindexed |
| `BidPlaced(uint256,address,uint256,uint256)`<br>`0x51db8e23b3f4479b162fd48823b8402895442b8f6cfd94f66239391881ec7b6f` | `uint256 charterId, address bidder` | `uint256 count, uint256 maxUnitPrice` | L12; count/limit are intent, not acquisition |
| `BidCancelled(uint256)`<br>`0xc1546e394b1975212fe013e7e6995653585f44e568c407d1157483f7d4b94581` | `uint256 charterId` | `empty` | L12 |
| `BidFilled(uint256,address,uint256,uint256)`<br>`0xfc74031ca18ead273f75fa7c82fab7aa771bc7ea6f3f183f7ed7c816d80fed5d` | `uint256 charterId, address filler` | `uint256 count, uint256 unitPrice` | L12; do not count accompanying purchase/BranchesOpened logs again |

### Charter auction events

C* prices below are ETH wei; caps/counts are charters. Neither this event family nor its inventory is an existing charter's branch-license allowance.

| Canonical signature · topic0 | Indexed topics after topic0 | Data words in order | Scope; qualification |
| --- | --- | --- | --- |
| `AuctionStarted(uint256,uint256)`<br>`0xf8910119ddbef5440c54532457dfe8250a10ed39e583292818f44724b9e1344c` | `uint256 day` | `uint256 startPrice` | C* |
| `DayRolled(uint256,uint256,uint256,uint256)`<br>`0xfe150722db0c02a69373b1d32f7d153b415b253b5bce66b95e7b1f5d9ce65c3f` | `uint256 day` | `uint256 startPrice, uint256 floorPrice, uint256 cap` | C*; no timestamp, duration, or end reason |
| `DecayHalfLifeSet(uint256)`<br>`0x3491d4ab69d4f73c3d81521a7c13c6f4299f2216ed9b9cc044949888cf5824f2` | `none` | `uint256 halfLife` | C* |
| `GuardianPaused(address)`<br>`0xd5354f32595d4786b7a234166bc1e34f4ee58f9e9d534b0fc5abd8e122f25fd5` | `address guardian` | `empty` | C* |
| `GuardianUnpaused()`<br>`0x984d636c2614e303400b04f078fb33065fa357cbc6859737a5e4528627f4fa18` | `none` | `empty` | C* |
| `SupplyControllerSet(address)`<br>`0x915d8b94cdcbf4fa1b4c768b15f63b99aee21096b9d04fe1938f45833036106d` | `none` | `address controller` | C*; controller is nonindexed |
| `CharterPurchased(uint256,address,uint256,uint256)`<br>`0x1c54748c22f6bf384e0cf9a6a4dfbc630c9ac343ba8a88a5769508bd2da18e50` | `uint256 charterId, address buyer, uint256 day` | `uint256 price` | C*; event sale price, not necessarily tx value |
| `ChartersPerDaySet(uint256)`<br>`0xd167d4300749433637c8f34275bc6ed626442d364ccf305e5e78ea908a5b4a59` | `none` | `uint256 count` | C* |
| `ReservePriceSet(uint256)`<br>`0xe4515db87ec3838c9a257222c26dda14c6bf63f5d49ad14460bf6558e6463085` | `none` | `uint256 price` | C* |
