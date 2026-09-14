# Protocol: system and routing

Publisher design, not verified deployment. Current whitepaper: `sr-whitepaper-v1`, captured 2026-09-14T22:15:13.789Z; [source index](../assets/sources.json). Earlier `sr-whitepaper` and website presentations retain their own dates.

## System and ownership — whitepaper §§1–2

STANDARD describes an ERC-20 currency, an ETH ↔ $STANDARD hooked Uniswap v4 pool, an issuing central bank, charter NFTs, branches within those charters, and expansion/contraction vaults. Traders need no charter. A branch represents a share of issuance, not a reserve-redemption claim. The protocol owns liquidity and reserve assets; the bank/company analogy is not a legal bank account or customer deposit product. [sr-whitepaper-v1: introduction, entities, disclaimer]

Trading generates fees and pool-flow measurements; issuance credits branch balances pro rata; expansion licenses permanently remove ledger value; retiring branches releases accrued value through withdrawal minting. Token deposits instead convert wallet tokens into re-mintable ledger value. Post-genesis charter auction ETH enters the ongoing fee engine; founding proceeds have a separate allocation and escrow/finalization sequence. [sr-whitepaper-v1: entities, currency, charters, reserves]

## Read only the needed mechanics

- [Supply and policy](protocol-policy.md): supply identities, deposit conversions, flow signals, published multiplier recurrence and source-only limits; [monetary parameters](../assets/parameters/monetary.json).
- [Charters](charters.md): branches, founding entry, auctions, exits and dormancy; [participation parameters](../assets/parameters/participation.json).
- [Reserves](reserves.md): separate founding/ongoing allocations, ownership and buybacks; [reserve parameters](../assets/parameters/reserves.json).
- [Launch trading](launch-trading.md): finalization, tax contradictions and activation claims; [launch parameters](../assets/parameters/launch.json).
- [Risks](risks.md): non-upgradeability does not eliminate owner discretion or the optional guardian.

## Publisher's feedback-loop thesis — §14

- **Adoption:** charter purchases fund reserves, liquidity and buybacks; additional branches change allocation rather than independently increasing the daily issuance budget.
- **Expansion:** licenses permanently remove value while increasing the purchaser's future issuance share.
- **Fee flow:** either trading direction generates fees; the current regime directs the active vault toward reserves or buybacks.
- **Policy:** outflow is described as combining issuance cuts, buybacks and crowd-priced resolution fees that burn and redistribute value.

These are the publisher's incentive arguments, not guaranteed rational behavior, profitability, price support or bank-run prevention. [sr-whitepaper-v1: flywheels]

## Presentation is not state

The earlier mint snapshot said not live; protocol counters, About diagrams and launch banners are time-bounded presentation, not authenticated state. About's opening describes issuance into an LP, whereas current §3 separates ledger accrual and withdrawal minting from genesis liquidity. Do not merge those descriptions. The separately reviewed deployment directory and protocol-condition additions remain available through [contracts](contracts.md); publication of addresses or conditions is not code/ABI correspondence. [sr-mint; sr-protocol; sr-about; sr-app-about; sr-whitepaper-v1: currency; sr-contract-directory; sr-protocol-conditions]

See [documents](documents.md) for all sixteen current sections and dated baseline coverage, and [conflicts](risk-conflicts.md) for incompatible source claims.
