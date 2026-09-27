# Treasury interface discovery

[Inventory scope](interface-inventory.md) · [Capabilities](capabilities.md) · [Identity and controls](contracts.md)

## ContractionVault

[contraction-vault.json](../assets/interfaces/contraction-vault.json) preserves 66 entries, including constructor, payable receive, manager-list controls, buyback entrypoint, events and errors. `poolEthDepth()` is publisher-displayed ETH18, not a guaranteed execution quote. `polManagerCount()` and `polManagers(uint256)` expose the manager list, not the list of liquidity positions; bounds and ordering require evidence.

Configured `tickPoolPctBps()`, `tickVaultPctBps()`, `tickCooldown()` and `twapDeviationTicks()` differ from resolved `effectiveTickPoolPctBps()`/`effectiveTwapDeviationTicks()`. Do not infer caller permission or exact public/private policy resolution from names. `lastTickAt()` is a contraction execution-time field, not the hook's price tick.

`BuybackExecuted(uint256 ethSpent,uint256 tokensBurned)` reports ETH spend and STANDARD burn accounting; reconcile actual transfers/burn semantics separately. It is not the POL Buyback's retained-token acquisition event. `migrateToSuccessor()` and `HoldingsMigrated` do not prove movement of every liquidity position or bytecode upgradeability.

## ExpansionVault

[expansion-vault.json](../assets/interfaces/expansion-vault.json) preserves 45 entries. `holdingsOf(address asset)` and `isReserveAsset(address asset)` inspect one supplied asset, not an enumerated complete portfolio. Authenticate asset identity/decimals before converting raw holdings.

`reservePool(address)` returns flat `(address currency0,address currency1,uint24 fee,int24 tickSpacing,address hooks)`. The fee is a raw pool-fee/flag field, not automatically basis points; signed tick spacing is not money. `setReservePool`/`ReservePoolSet` preserve a nested pool-key tuple in their respective layouts. Full tuple components are retained in the ABI data.

`purchaseReserve`, approval/configuration, pause and migration declarations support decoding/authorized unsigned preparation only. `ReservePurchased` separates selected asset, ETH spent and raw output-token amount; it does not independently prove swap settlement or a complete holdings census.

## FeeSplitter

[fee-splitter.json](../assets/interfaces/fee-splitter.json) preserves 38 entries. `teamShareBps()` and `polShareBps()` are active share fields. `queuedShares()` returns `(teamBps,polBps,pending)` and must not be substituted for active routing. `teamWallet()` is a recipient, not necessarily the administrator.

`teamOwed()` is publisher/source-supported ETH liability, not an entitlement for every STANDARD holder. `EpochRouted` reports direction and team/POL/vault amounts; team accrual is not a completed claim. `EpochRoutingSkipped` records retained balance. `SharesQueued` differs from `SharesApplied`; `claimTeam`, `settleEpoch`, migration and receive/error definitions do not establish permission or successful transfer.

## Missing broader roles

Genesis Liquidity Manager, POL Buyback and Incentives Vault remain distinct named roles with dated addresses, but this module exposes only selective control-read declarations for them. Their broader ABI coverage is [explicitly unknown](interface-inventory-infrastructure.md), not silently borrowed from ContractionVault or a similarly named module. Historical source records may supply narrower independent event evidence without establishing a full ABI.
