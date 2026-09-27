# Founding-sale interface discovery

[Inventory scope](interface-inventory.md) · [Capabilities](capabilities.md) · [Dated contract identity](contracts.md)

[genesis-minter.json](../assets/interfaces/genesis-minter.json) preserves 91 publisher entries. GenesisMinter is the founding-sale role, not an ongoing charter auction, a branch-license auction or a future sale authorization.

## State and price observations

`opened()` and `finalized()` are separate flags. `mintStart()`, `publicStart()`, `dutchEnd()` and `wlWindow()` describe the founding phases; no ongoing auction schedule is inherited. `strict()`/`strictEnded()` expose flags without establishing every eligibility condition.

`whitelistPrice()`, `publicStartPrice()` and `currentPublicPrice()` are separate publisher ETH-priced fields. Price-function output does not prove available inventory or wallet eligibility. `allowlistAllocation()`, `allowlistMinted()`, `totalMinted()`, `allowlistClaimed(address)` and `mintedBy(address)` supply distinct counts/flags; wallet mint history need not equal current NFT ownership. `totalProceeds()` is accounting, not independently reconciled recipient transfers.

## Commitments, launch and control

`merkleRoot()` is the allowlist commitment, not a membership proof. `hashFor(address)` and `eip712Domain()` expose hash/domain information; no signing authority follows. The exact ordered dynamic EIP-712 extensions output remains in the full ABI. `operator()` is separate from module ownership.

`claimAllowlist`, `mintPublic`, `open`, `endStrict` and `finalizeAndLaunch` are preserved for input decoding or host-authorized unsigned preparation. ABI presence does not grant permission or establish correct payment/refunds, quotas, proof validation or launch effects. `launchTickFor` and reserved tick-related outputs require currency order and source evidence before economic interpretation.

`AllowlistClaimed`/`PublicMinted` index wallet and charter ID, leaving price in data. `GenesisFinalizedAndLaunched` separates minted/proceeds totals, allocation fields, launchPriceWei and signed launch tick; reconcile actual downstream transfers and liquidity positions independently. Dated publisher attribution and a finalization flag do not prove every liquidity/control consequence.
