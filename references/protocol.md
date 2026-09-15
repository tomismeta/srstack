# Protocol: system and routing

Publisher design, not verified deployment. Current whitepaper: `sr-whitepaper-v1`; retrieval dates and provenance are in the [source index](../assets/sources.json).

## System and ownership — whitepaper §§1–2

STANDARD describes an ERC-20 currency, an ETH ↔ $STANDARD hooked Uniswap v4 pool, an issuing central bank, charter NFTs, branches within those charters, and expansion/contraction vaults. Traders need no charter. A branch represents a share of issuance, not a reserve-redemption claim. The protocol owns liquidity and reserve assets; the bank/company analogy is not a legal bank account or customer deposit product. [sr-whitepaper-v1: introduction, entities, disclaimer]

Trading generates fees and pool-flow measurements; issuance credits branch balances pro rata; expansion licenses permanently remove ledger value; retiring branches releases accrued value through withdrawal minting. Token deposits instead convert wallet tokens into re-mintable ledger value. Post-genesis charter auction ETH enters the ongoing fee engine; founding proceeds have a separate allocation and escrow/finalization sequence. [sr-whitepaper-v1: entities, currency, charters, reserves]

## Read only the needed mechanics

- [Supply and policy](protocol-policy.md): supply identities, deposit conversions, flow signals, published multiplier recurrence and source-only limits; [monetary parameters](../assets/parameters/monetary.json).
- [Charters](charters.md): branches, founding entry, auctions, exits and dormancy; [participation parameters](../assets/parameters/participation.json).
- [Reserves](reserves.md): separate founding/ongoing allocations, ownership and buybacks; [reserve parameters](../assets/parameters/reserves.json).
- [Launch trading](launch-trading.md): finalization, tax gaps and activation; [launch parameters](../assets/parameters/launch.json).
- [Risks](risks.md): non-upgradeability does not eliminate owner discretion or the optional guardian.

## Publisher's feedback-loop thesis — §14

- **Adoption:** charter purchases fund reserves, liquidity and buybacks; additional branches change allocation rather than independently increasing the daily issuance budget.
- **Expansion:** licenses permanently remove value while increasing the purchaser's future issuance share.
- **Fee flow:** either trading direction generates fees; the current regime directs the active vault toward reserves or buybacks.
- **Policy:** outflow is described as combining issuance cuts, buybacks and crowd-priced resolution fees that burn and redistribute value.

These are the publisher's incentive arguments, not guaranteed rational behavior, profitability, price support or bank-run prevention. [sr-whitepaper-v1: flywheels]

## Presentation is not state

Use a fresh `protocol` snapshot for current issuance, supply and tax readings, and `auctions` for availability. These use the publisher's fixed ABI with block and binding checks; they do not assert source-code equivalence. If fresh reads are unavailable, report the requested values as unknown rather than using saved state or launch defaults. Keep the answer focused on the requested values. [sr-protocol-conditions; sr-publisher-read-interface]

See [documents](documents.md) for all sixteen current sections and [risks](risks.md) for remaining evidence gaps.
