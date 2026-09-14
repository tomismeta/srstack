# Charters and branches

Publisher design: [core sources](../assets/sources/website-core.json), `sr-whitepaper` §§6–10,12. Exact ongoing settings: [participation parameters](../assets/parameters/participation.json); genesis settings: [launch parameters](../assets/parameters/launch.json).

## Charter and branch lifecycle — §§6–7

A charter is an initially soulbound NFT licensing its holder to run a bank and receive issuance. It opens with `initial-branches` and can hold `maximum-branches`. Branches divide the epoch's issue pro rata; new branches accrue from opening, not retroactively. An expansion license paid in $STANDARD opens an additional branch, with payment burned according to `license-burn-share`. [sr-whitepaper: charters, branches]

Retiring branches withdraws their proportional share of the charter's accrued balance and destroys the retired earning capacity. Retiring the final branch burns the charter. The described return path is purchasing a new charter at auction; a closed charter does not reopen. Purchasing another seat does not preserve the retired branches. [sr-whitepaper: charters, exits]

## Follow the question

- [Genesis entry](genesis.md): current paid whitelist, remaining public supply, selection and proceeds. [Launch mint](launch-mint.md) has the dated schedule, EST ambiguity and token-without-liquidity graphic.
- [Ongoing auctions](auctions.md): daily charter/license purchases, exponential price, limits, rollover and hidden floor. Do not substitute these rules for the genesis auction.
- [Exits and dormancy](exits.md): pro-rata retirement, resolution fee, bounty ordering, check-in and future NFT transferability.
- [Reserves](reserves.md): genesis versus ongoing ETH routing and ownership.
- [History](announcement-history.md): superseded free-mint promise, never current entry pricing.

Ledger credits versus spendable/burnable wallet tokens remain unresolved; see [conflicts](risk-conflicts.md).
