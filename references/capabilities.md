# Question-to-capability guide

Prefer a direct answerable read to rebuilding an index. This is optional planning knowledge, not a mandatory workflow, question whitelist or execution router. Read the relevant row and interface; do not preload every ABI or treat dated contract bindings as current targets. A supplied hypothetical question may need no contract access.

The [contract inventory](contracts.md) identifies roles/generations and dated leads. The [interface index](interface-inventory.md) enumerates complete reviewed source definitions and explicit partial fragments. [Capability records](../assets/interfaces/capabilities.json) bind every row below to exact interface IDs, function signatures and shared review IDs. This edition cites `publisher-protocol-interfaces-2026-09-27` in the [review registry](../assets/interfaces/reviews.json); each referenced interface/entry retains that freshness context, source fingerprints and coverage. It is an interface-review date, not a live-state observation or independent implementation certificate.

## Read the status precisely

- **Available:** the cited reviewed publisher interface exposes the named read. Authenticate deployment, block, units and semantics before interpreting the result.
- **Not exposed:** the stated capability is absent from the identified complete reviewed source definitions. This is not proof that no other deployed interface, historical-state query or future generation can answer it.
- **Unknown:** interface coverage or economic/implementation evidence is insufficient. Missing evidence is not a negative capability and does not forbid further authorized research.

## Planning map

The record ID is a lookup key in the capability records, not a command or address alias. Detailed layouts and explanations are in the linked interface data; selected encoding examples remain in the [interface guide](interface-guide.md).

| Question / record ID | Status and reviewed scope | Smallest useful evidence; what it does not prove |
| --- | --- | --- |
| Open branches or charter pending / `branches-and-pending` | Available: [CentralBank](../assets/interfaces/central-bank.json) | `totalBranches`, `branchCountOf`, `pendingOf`, `charters` at the selected block. Pending is not proved earned, spendable or withdrawable; branches are not unsold licenses. |
| Charter owner / `charter-ownership` | Available: [CharterNFT](../assets/interfaces/charter-nft.json) | `ownerOf` at the selected block; module owner and historical buyer are different. Ownership transitions need relevant NFT logs or archive-state corroboration. |
| Current license availability / `current-license-status` | Available: [original](../assets/interfaces/license-auction-original.json), [v1.1](../assets/interfaces/license-auction-v1-1.json), [v1.2](../assets/interfaces/license-auction-v1-2.json) | Relevant inventory, round and quote getters; reconcile effective timing and materialized storage. Zero inventory makes residual curve output not a buyable ask. Check independent charter/funding constraints. |
| Current new-charter state / `current-charter-status` | Available: [original](../assets/interfaces/charter-auction-original.json), [v1.2](../assets/interfaces/charter-auction-v1-2.json) | Its own inventory, price and configured supply, in publisher ETH units. Do not borrow license allowance, timing or payment rules. |
| Original charter/day usage / `original-charter-day-usage` | Available: [original license](../assets/interfaces/license-auction-original.json) | `purchasedOnDay(charterId,day)` is a keyed usage candidate. Authenticate retention and meaning; this is not an aggregate round-price series. |
| Newer charter/window usage / `window-usage-and-allowance` | Available: [v1.1](../assets/interfaces/license-auction-v1-1.json), [v1.2](../assets/interfaces/license-auction-v1-2.json) | `purchasedInWindow(charterId,window)` and `remainingForCharter`. An allowance window is not automatically an auction day or rolling 24 hours. |
| Arbitrary past round sold totals and sale-price series / `historical-aggregate-day-series` | Not exposed: the five complete reviewed auction source definitions | No `daySold(uint256)` or `dayPrice(uint256)`; current/materialized-day fields are not a historical series. Use scoped emitter logs; archive state can corroborate counters/configuration. The keyed charter-usage getters above still exist. |
| `dayAnchorTime()` / `auction-anchor-not-day-anchor` | Not exposed: the same five auction definitions | Use evidenced `auctionAnchor()` plus original `AUCTION_DAY()` or newer `auctionPeriod()`. Do not probe guessed selectors or substitute a fixed duration. |
| v1.2 bids / `orders-and-fillability` | Available: [v1.2 license](../assets/interfaces/license-auction-v1-2.json) | Count/pages, charter-keyed bids and fillability. Page-ID-to-charter mapping remains unproved; limits and fillability are not executed prices or promised fills. |
| Earned-only funding and future accrual / `earned-origin-and-accrual` | Unknown semantics: [CentralBank](../assets/interfaces/central-bank.json) | Pending/rate getter layouts exist. Origin attribution and checkpoint/scaling/eligibility mechanics need evidence. A labelled empirical ledger pace or explicit scenario can still be useful. |
| Wallet tokens and scale / `token-balance-and-scale` | Available: [STANDARD](../assets/interfaces/standard.json) | `balanceOf`, `decimals`, token `allowance`; not pending ledger, license allowance, fiat value or transfer-success proof. |
| Enabled versus active launch restrictions / `launch-restriction-state` | Available: [STANDARD](../assets/interfaces/standard.json), [TaxHook](../assets/interfaces/tax-hook.json) | Read enabled, resolved active and separate gate/schedule/tax inputs; authenticate the actually linked hook. No universal transfer-success conclusion. |
| First-round sellout / `first-round-exhaustion` | Unknown from final observed purchase alone | `AuctionStarted` contains no first-round allocation; a later `DayRolled.cap` belongs to that later round. Establish effective capacity, changes and complete relevant scope; otherwise say last observed. |
| Charter refund / `charter-refund-amount` | Unknown settlement: reviewed charter interfaces | Sale event price, transaction value and gas are independently reportable. Their difference is not proof of a refund; use appropriate trace/transfer/balance and implementation evidence. |
| Buyback depth/control inputs / `contraction-pool-and-controls` | Available: [Contraction Vault](../assets/interfaces/contraction-vault.json) | Pool ETH depth, bounded manager enumeration and effective BPS/tick-labelled inputs. These are not executable size, burn-outcome or implementation proofs. |
| Selected reserve holdings / `selected-reserve-holdings` | Available: [Expansion Vault](../assets/interfaces/expansion-vault.json) | `holdingsOf(asset)`, `isReserveAsset`, `reservePool` for identified assets; not a complete portfolio census, common raw unit or executable market quote. |
| Fee shares and liability / `current-versus-queued-fees` | Available: [FeeSplitter](../assets/interfaces/fee-splitter.json) | Current shares, queued shares/pending flag, team wallet and owed ETH. Queued is not effective; liability is not settled payment or holder entitlement. |
| Founding sale / `founding-sale-state` | Available: [GenesisMinter](../assets/interfaces/genesis-minter.json) | Open/finalized flags, minted count and proceeds/price; distinct from ongoing charter auctions and not refund/finalization-flow proof. |
| Full registry/liquidity/POL/incentives capabilities / `incompletely-reviewed-control-roles` | Unknown: [publisher control fragment](../assets/interfaces/publisher-control-fragment.json), not full role ABIs | Selected owner/pendingOwner leads; executionPermissionless is bound specifically to registry reads. Obtain more authenticated evidence rather than guessing keys or exporting a flag to other roles. |

## Current reads, archive state and execution history

A current getter answers state at its selected block. A capable archive provider may execute that same getter at a historical block, subject to deployment existence, provider support and applicable semantics. A missing day-parameter history getter therefore does not mean all historical evidence is inaccessible without logs.

Logs answer observed executions and transitions. Discover by emitting contract and authenticated event layout, not only `transaction.to`: internal calls can emit auction events. `eth_getLogs` supplies full log identity/order; headers supply timestamps and canonicality observations; receipts separately corroborate inclusion and transaction success. Coverage and identity/receipt checks remain distinct. See [history collection and reuse](auction-history.md) and the [worked example](research-example.md).

An available getter can narrow discovery without answering the entire question. Counter/log disagreement is a reconciliation problem; neither automatically wins. A complete inventory of a publisher ABI is not complete deployed behavior, discovered history, supported access or economic interpretation. Listing writes is documentation only: [wallet and preparation boundaries](safety.md#preparation-and-wallet-boundary) are unchanged.

## Future additions

Every new contract/generation follows the [inventory methodology](inventory-methodology.md). Update role bindings, shared review provenance, complete/partial coverage, exact entry layouts and relevant capability rows together. Unknown scope must remain unknown; do not convert missing inventory coverage into a research prohibition.
