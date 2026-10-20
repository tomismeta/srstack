# Charter distribution interfaces

**Reviewed 2026-10-19.** Stimulus, top-up, burned-charter compensation and two launch-token drop generations are separate roles and beneficiaries, not recurring issuance or universal holder rights. The [review](../assets/interfaces/reviews.json) retains every entry in each selected publisher array, but full source-definition and deployed-implementation coverage are **false**. See [economic distinctions](charter-distributions.md), [capabilities](capabilities.md), [identity authentication](contracts.md#authenticate-the-requested-role) and [wallet boundaries](safety.md#preparation-and-wallet-boundary).

## Roles and coverage

The root-linked main module supplies the selected declarations and role-use callsites; [charter sources](../assets/sources/charter-distributions.json) and [launchpad sources](../assets/sources/launchpad.json) retain fingerprints and publication/review scopes. Fresh explorer access was denied. Historical creation, dependency and ownership-handover observations are attributed research, not a new explorer or implementation certificate. Bindings date to the review, not an assumed activation time.

| Role / generation | Selected array and exact main-body range | Retained entries |
| --- | --- | --- |
| [charter-drop-2026-10-19](../assets/interfaces/charter-drop-2026-10-19.json) | `D2` / `[613821,614072)` | 2 functions, 0 events, 1 errors |
| [branch-claim-2026-10-11](../assets/interfaces/branch-claim-2026-10-11.json) | `FO` / `[653553,654971)` | 19 functions, 4 events, 4 errors |
| [branch-top-up-2026-10-11](../assets/interfaces/branch-top-up-2026-10-11.json) | `f5` / `[652585,653545)` | 12 functions, 4 events, 4 errors |
| [charter-refund-claim-2026-10-15](../assets/interfaces/charter-refund-claim-2026-10-15.json) | `bb` / `[668941,669629)` | 11 functions, 1 events, 3 errors |
| [charter-drop-2026-10-14](../assets/interfaces/charter-drop-2026-10-14.json) | `fn` / `[633783,634702)` | 9 functions, 0 events, 29 errors |

Each exact fragment identifies the main-body parent SHA-256 and byte range in the interface JSON; role-binding and callsite fragments are separate. Dated addresses are [discovery evidence](../assets/entities/contracts.json), not runtime targets. No constructor/fallback/receive layout is supplied by these selected arrays; no absence claim about deployed code follows.

Capability scope is separate: `charter-distribution-state` covers selected stimulus/top-up/refund and earlier-drop reads; `launchpad-drop-snapshot-state` exposes the newer aggregate tuple; `launchpad-drop-entitlement` is unknown because its per-charter claim/closed-count interface was not acquired. See the [planning map](capabilities.md#planning-map).

## Every selected function

Amounts use the authenticated distribution asset’s raw units. Discover `token()` and decimals where exposed; launch-token drops publish 18 decimals, but this does not establish every distribution’s asset. Branch counts, charter IDs and snapshot block numbers are unscaled integers; timestamps are Unix seconds. `perBranch` is token units per counted branch, not an issuance multiplier. Key namespace is chain + distribution contract + account/charter/token as declared.

### `charter-drop-2026-10-19`

| Signature | Mutability / bounded interpretation |
| --- | --- |
| `drops(address)` | `view` — Read the token-keyed drop snapshot/accounting record. Earlier generation returns eight flat values; URC5 returns nine including mode. Neither is a current-wallet entitlement by itself. |
| `snapshot(address)` | `nonpayable` — Document snapshot advancement, not immediate payout; completion and frozen branch eligibility require separate state evidence. |

### `branch-claim-2026-10-11`

| Signature | Mutability / bounded interpretation |
| --- | --- |
| `token()` | `view` — Read the distribution asset address; authenticate its decimals rather than assuming STANDARD, USDG or a dollar peg. |
| `charterNFT()` | `view` — Read the linked charter NFT identity; token ownership alone does not replace historical eligibility. |
| `bank()` | `view` — Read the linked Bank identity; claim allocation is not ordinary recurring Bank accrual. |
| `refund()` | `view` — Read the configured refund destination, not a beneficiary’s refund amount. |
| `deadline()` | `view` — Read the claim deadline timestamp; sealed/loading/claimed state remains independently relevant. |
| `ownerBranchCap()` | `view` — Read the stimulus per-owner branch cap; do not invent the separate historical top-up calculation. |
| `isSealed()` | `view` — Read the allocation sealing flag; unsealed/loading state is not a zero-entitlement result. |
| `totalBranches()` | `view` — Read the distribution’s counted-branch aggregate, not the Bank’s current branch supply. |
| `perBranch()` | `view` — Read the allocation amount per counted branch, not a recurring issuance multiplier. |
| `totalClaimed()` | `view` — Read the distribution’s claimed token accounting aggregate, not a current wallet balance, fiat valuation or independently proved funding source. |
| `totalAllocated()` | `view` — Read the distribution’s allocated token accounting aggregate, not a current wallet balance, fiat valuation or independently proved funding source. |
| `entries(uint256)` | `view` — Read the role-specific entry: branch claim uses loaded/claimed/branches keyed by charter ID; burn compensation uses claimed/amount keyed by historical account. |
| `countedFor(address)` | `view` — Read counted branches for the specified historical owner; not current holdings or claim amount. |
| `claimable(uint256)` | `view` — Read the contract’s scoped entitlement preview using its exact account/charter/token keys; unavailable/reverting reads are unknown, not zero. |
| `counted(uint256)` | `view` — Read counted branches for the specified charter; not a token balance. |
| `loaded(uint256)` | `view` — Read whether that charter entry has been loaded; missing state and transport failures are not false. |
| `claimed(uint256)` | `view` — Read the role-specific claimed flag for the exact charter/account key; it does not establish original eligibility alone. |
| `claim(uint256[])` | `nonpayable` — Document the role-specific explicit claim transaction; a preview or successful simulation is not settled transfer evidence. |
| `sweep()` | `nonpayable` — Document the explicit recovery transaction; deadline, recipient and authorization require separate evidence. |

### `branch-top-up-2026-10-11`

| Signature | Mutability / bounded interpretation |
| --- | --- |
| `token()` | `view` — Read the distribution asset address; authenticate its decimals rather than assuming STANDARD, USDG or a dollar peg. |
| `charterNFT()` | `view` — Read the linked charter NFT identity; token ownership alone does not replace historical eligibility. |
| `refund()` | `view` — Read the configured refund destination, not a beneficiary’s refund amount. |
| `deadline()` | `view` — Read the claim deadline timestamp; sealed/loading/claimed state remains independently relevant. |
| `isSealed()` | `view` — Read the allocation sealing flag; unsealed/loading state is not a zero-entitlement result. |
| `totalAllocated()` | `view` — Read the distribution’s allocated token accounting aggregate, not a current wallet balance, fiat valuation or independently proved funding source. |
| `totalClaimed()` | `view` — Read the distribution’s claimed token accounting aggregate, not a current wallet balance, fiat valuation or independently proved funding source. |
| `allocation(uint256)` | `view` — Read the top-up allocation for a charter ID; not an automatically recurring or universal holder benefit. |
| `claimable(uint256)` | `view` — Read the contract’s scoped entitlement preview using its exact account/charter/token keys; unavailable/reverting reads are unknown, not zero. |
| `unclaimed()` | `view` — Read the distribution’s remaining allocation accounting; not an independently reconstructed custody balance. |
| `claim(uint256[])` | `nonpayable` — Document the role-specific explicit claim transaction; a preview or successful simulation is not settled transfer evidence. |
| `sweep()` | `nonpayable` — Document the explicit recovery transaction; deadline, recipient and authorization require separate evidence. |

### `charter-refund-claim-2026-10-15`

| Signature | Mutability / bounded interpretation |
| --- | --- |
| `token()` | `view` — Read the distribution asset address; authenticate its decimals rather than assuming STANDARD, USDG or a dollar peg. |
| `refund()` | `view` — Read the configured refund destination, not a beneficiary’s refund amount. |
| `deadline()` | `view` — Read the claim deadline timestamp; sealed/loading/claimed state remains independently relevant. |
| `isSealed()` | `view` — Read the allocation sealing flag; unsealed/loading state is not a zero-entitlement result. |
| `totalOwed()` | `view` — Read the distribution’s owed token accounting aggregate, not a current wallet balance, fiat valuation or independently proved funding source. |
| `totalClaimed()` | `view` — Read the distribution’s claimed token accounting aggregate, not a current wallet balance, fiat valuation or independently proved funding source. |
| `entries(address)` | `view` — Read the role-specific entry: branch claim uses loaded/claimed/branches keyed by charter ID; burn compensation uses claimed/amount keyed by historical account. |
| `claimable(address)` | `view` — Read the contract’s scoped entitlement preview using its exact account/charter/token keys; unavailable/reverting reads are unknown, not zero. |
| `owed(address)` | `view` — Read the burn-compensation amount owed to the specified account; no restoration of burned charters is implied. |
| `claimed(address)` | `view` — Read the role-specific claimed flag for the exact charter/account key; it does not establish original eligibility alone. |
| `claim()` | `nonpayable` — Document the role-specific explicit claim transaction; a preview or successful simulation is not settled transfer evidence. |

### `charter-drop-2026-10-14`

| Signature | Mutability / bounded interpretation |
| --- | --- |
| `drops(address)` | `view` — Read the token-keyed drop snapshot/accounting record. Earlier generation returns eight flat values; URC5 returns nine including mode. Neither is a current-wallet entitlement by itself. |
| `frozenBranches(address,uint256)` | `view` — Read frozen branches for this token/charter snapshot, not today’s Bank branch count. |
| `claimedBranches(address,uint256)` | `view` — Read already-claimed branches for this token/charter allocation; distinguish branch counts from token amounts. |
| `claimable(address,uint256)` | `view` — Read the contract’s scoped entitlement preview using its exact account/charter/token keys; unavailable/reverting reads are unknown, not zero. |
| `ownerNotes(uint256)` | `view` — Read the recorded owner and note time for a charter; this is historical attribution, not proof of today’s ownership or final entitlement. |
| `charterNFT()` | `view` — Read the linked charter NFT identity; token ownership alone does not replace historical eligibility. |
| `claim(address,uint256)` | `nonpayable` — Document the role-specific explicit claim transaction; a preview or successful simulation is not settled transfer evidence. |
| `claimMany(address[],uint256[])` | `nonpayable` — Document batch token/charter claims with parallel arrays; receipt/asset evidence is required for actual settlement. |
| `noteOwner(uint256)` | `nonpayable` — Document recording a charter owner note; do not treat an unsubmitted transaction as historical beneficiary evidence. |

## Important decoder distinctions

- Stimulus `entries(uint256)` returns **bool loaded, bool claimed, uint240 branches** keyed by charter. Compensation `entries(address)` returns **bool claimed, uint248 amount** keyed by historical account. Neither substitutes today’s charter owner for the historical beneficiary.
- Earlier `drops(address)` returns **eight flat values**: amount, perBranch, registeredAt, lastId, nextId, branches, claimed, recovered. New `drops(address)` returns **nine**, adding `uint8 mode`. Both use the same selector; return layout cannot be selected by selector alone.
- New primary `D2` supplies snapshot state and the nonpayable `snapshot(address)` call, not a complete new-generation claim interface. The common `fn` array is used for common frontend reads, but its eight-output `drops` layout must not be unioned with `D2`. Authenticate any additional claim/closed-count/mode interface separately. Snapshot progress and frozen eligibility differ from current Bank branches; allocated tokens are not automatically spendable.
- `ownerNotes` records historical owner/time; `isSealed`, loading, deadline, already-claimed and entitlement amount are independent inputs. A malformed, unavailable or reverting read is unknown, not zero. Preview URL/sample amounts and a visible claim button are not entitlement evidence.

## Exact selected event layouts

The declarations below retain indexed bits. Topic0 is the event signature hash, followed only by indexed fields. Unindexed fields are ABI data; consult JSON `event_layout`, not a signature-only decoder. No event is invented for a role whose selected array lacks it.

### `branch-claim-2026-10-11` events

```solidity
event Loaded(uint256 charters, uint256 branches, uint256 snapshotBlock)
event Sealed(uint256 totalBranches, uint256 perBranch, uint256 funded)
event Claimed(uint256 indexed charterId, address indexed owner, uint256 branches, uint256 amount)
event Swept(address indexed to, uint256 amount)
```

### `branch-top-up-2026-10-11` events

```solidity
event AllocationsLoaded(uint256 count, uint256 total, uint256 snapshotBlock)
event Sealed(uint256 totalAllocated)
event Claimed(uint256 indexed charterId, address indexed owner, uint256 amount)
event Swept(address indexed to, uint256 amount)
```

### `charter-refund-claim-2026-10-15` events

```solidity
event Claimed(address indexed account, uint256 amount)
```

Stimulus and top-up `Claimed` declarations share indexed charterId/owner but differ in data: stimulus includes branches and amount; top-up only amount. Compensation indexes account and puts amount in data. Sealing/loading records describe accounting and snapshot blocks, not independently proved team-fee or POL-surplus provenance. Successful receipts and reconciled token transfers establish settlement separately.

## Selected errors and limits

- `charter-drop-2026-10-19`: `NoProgress()`.
- `branch-claim-2026-10-11`: `NotSealed()`, `ClaimClosed()`, `NotCharterOwner(uint256)`, `NothingToClaim()`.
- `branch-top-up-2026-10-11`: `NotSealed()`, `ClaimClosed()`, `NotCharterOwner(uint256)`, `NothingToClaim()`.
- `charter-refund-claim-2026-10-15`: `NotSealed()`, `ClaimClosed()`, `NothingToClaim()`.
- `charter-drop-2026-10-14`: `CurveGraduated()`, `CharterDropDisabled()`, `CreatorBuyClosed()`, `EmptyNameOrSymbol()`, `EthTransferFailed()`, `ExceedsRemainingSupply()`, `ExcessiveInput()`, `InsufficientOutput()`, `InsufficientReserve()`, `InsufficientStockOut()`, `InvalidCharterDrop()`, `InvalidCreatorTax()`, `InvalidRecipient()`, `LaunchesPaused()`, `MetadataTooLong()`, `NoRoute()`, `NotFeeRecipient()`, `PairAssetDisabled()`, `PartialFill()`, `SnipeOptOutDisabled()`, `TransfersDisabled()`, `UnknownCurve()`, `WrongEthAmount()`, `ZeroAddress()`, `NotCharterOwner()`, `OwnerUnknown()`, `NoteTooSoon()`, `NothingToClaim()`, `SnapshotIncomplete()`.

Error names identify declared diagnostics, not all triggering paths or complete authorization. `NoProgress()` does not prove snapshot completion; it requires context. Historical refund ownership-transfer initiation is not acceptance. No claim listing restores burned charters, removes dormancy, creates automatic insurance or authorizes preparing/submitting a claim. Funding and distribution-mode interpretation remain in the [canonical topic](charter-distributions.md).
