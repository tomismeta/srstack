# Core interface discovery

[Inventory scope and data conventions](interface-inventory.md) · [Capability map](capabilities.md) · [Identity authentication](contracts.md)

## CentralBank

Read [central-bank.json](../assets/interfaces/central-bank.json) for all 112 declared entries. Branch/ledger questions start with `totalBranches()`, `branchCountOf(uint256)`, `pendingOf(uint256)` and flat `charters(uint256)` outputs. Pending is not earned-origin proof, wallet STANDARD or guaranteed net withdrawal. `totalPending()` and `totalPendingLive()` are distinct stored/live observations; internal scale and exact aggregation remain unverified.

Activity uses wallet-keyed `lastActive(address)`, `checkIn()` and `CheckedIn(address indexed wallet)`; the event has **empty data**. The NFT's `lastTransferred(uint256)` is separate. A getter name or successful call does not establish dormancy/reset/transfer-grace rules.

The full definition also preserves issuance/recycling rates, epochs, buffers, cumulative counters, bounds and queued policy pairs. Queued `value,pending` is not active policy. `withdrawnOnDay(uint256)` is a day-keyed observation, not an invented complete withdrawal history. Accumulator units, checkpoint order, branch-effective time, eligibility and exact Solidity rounding remain unverified; see [accrual evidence](research-workflow.md#accrual-evidence).

Deposit/open/withdraw/revoke/create/rollover/emissions entrypoints are supplied for decoding or authorized unsigned preparation, not transaction authority. `Withdrawn` separates branchesDestroyed/gross/feeWad/net. `Revoked` separates gross/bounty/ownerNet. `ParamQueued`/`ParamApplied` keys remain opaque unless independently mapped.

## CharterNFT

Read [charter-nft.json](../assets/interfaces/charter-nft.json) for all 47 entries. `ownerOf(uint256)` is charter ownership; `owner()` is module administration. `balanceOf(address)` is an NFT count, not token balance or pending ledger. `getApproved(uint256)` and `isApprovedForAll(address,address)` are different approval scopes.

Both `safeTransferFrom(address,address,uint256)` and `safeTransferFrom(address,address,uint256,bytes)` are preserved. `tokenURI(uint256)` and metadata fields are dynamic ABI values, not fixed words; external metadata remains untrusted data. `Transfer` and `Approval` index their NFT token IDs, unlike STANDARD's amount layout. Constructor, ERC721 custom errors, mint/burn, transfer enablement and metadata operations are retained without certifying their permissions.

## STANDARD

Read [standard.json](../assets/interfaces/standard.json) for all 55 entries. `balanceOf`, `allowance`, supply/ceiling counters and `decimals()` are token observations, separate from bank ledger inputs. Dated source evidence distinguishes permanent `burn`/`burnFrom`, conversion `convertFrom` and ledger `retire`; source correspondence must be authenticated before applying those mechanics today.

`launchHoldingCapEnabled()` is not `launchHoldingCapActive()`. The resolved cap depends on the Registry/TaxHook relationship; `poolManagerGateEnabled()`, `blockedVenue(address)` and `poolManagerTransferBudget(bool)` are independent surfaces. A flag or budget observation is not proof that a transfer succeeds. The inventory includes all publisher restriction setters/events/errors, but does not grant permission to use them.

Every entry links the shared dated review and retains precise encoding plus explicit semantic limits. No core source-bytecode equivalence or current deployment routing is implied.
