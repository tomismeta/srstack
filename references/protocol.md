# Protocol: system and routing

Publisher design, not verified deployment. [Core sources](../assets/sources/website-core.json): `sr-whitepaper` v0.1, `sr-protocol`, `sr-mint`.

## System and ownership — whitepaper §§1–2

STANDARD describes a closed monetary economy centered on an ERC-20 currency, an ETH ↔ $STANDARD Uniswap v4 hooked pool, an issuing central bank, charter NFTs, branches within those charters, and expansion/contraction vaults. Traders need no charter. Bankers hold the charter that operates their branches; a branch represents a share of issuance, not a separate reserve claim. The protocol owns the stated permanent liquidity position and the bank holds reserve assets. The central bank reads pool flow, sets issuance and routes fees. [sr-whitepaper: introduction, entities]

Trading pays fees; the hook reports net ETH flow; issuance is credited pro rata to branches; expansion licenses consume and burn $STANDARD; branch retirement releases accrued balance through withdrawal minting; post-genesis charter auction ETH enters the fee engine. Genesis proceeds have a separately described destination: see [charters](charters.md) and [reserves](reserves.md). The publisher's bank/company analogy is not a legal bank account or deposit product. [sr-whitepaper: entities, charters, disclaimer]

## Read only the needed mechanics

- [Supply and policy](protocol-policy.md): accounting identities, current flow versus trailing signal, streamed issuance and hidden recurrence; [monetary parameters](../assets/parameters/monetary.json).
- [Charters](charters.md): branch lifecycle, genesis entry, auctions, exits and dormancy; [participation parameters](../assets/parameters/participation.json).
- [Reserves](reserves.md): fees, asset ownership and buybacks; [reserve parameters](../assets/parameters/reserves.json).
- [Launch trading](launch-trading.md): announced activation and temporary tax, not observed execution; [launch parameters](../assets/parameters/launch.json).

## Publisher's feedback-loop thesis — §13

- **Adoption:** post-genesis charter payments finance the fee engine; extra branches change allocation of issue rather than independently enlarging the policy issuance budget.
- **Expansion:** acquiring licenses burns currency while adding the buyer's future issuance share.
- **Fee flow:** buys and sells both generate fees; the current regime directs the active vault toward reserves or buybacks.
- **Policy:** outflow is described as combining issuance cuts, buybacks and higher crowd-priced resolution fees that burn and redistribute value.

These explain the publisher's incentive thesis, not guaranteed rational behavior, profitability, price support or successful bank-run prevention. Charter mechanics and withdrawal pressure are detailed in [charters](charters.md); asset destinations in [reserves](reserves.md). [sr-whitepaper: flywheels]

## Presentation is not state

At the website snapshot, the mint page still said the mint was not live; the banner announced September 14. Protocol-page zero counters and About diagrams are not authenticated state. The About explainer's opening says issuance goes into an LP, while §3 specifies ledger accrual and withdrawal minting apart from genesis; preserve this discrepancy rather than combining incompatible accounting descriptions. [sr-mint; sr-protocol; sr-about; sr-app-about; sr-whitepaper: currency]

About/profile/discovery provenance: [website context](../assets/sources/website-context.json). See [documents](documents.md) for all pages/sections, [contracts](contracts.md) for unresolved identities and [conflicts](risk-conflicts.md) for incompatible descriptions.
