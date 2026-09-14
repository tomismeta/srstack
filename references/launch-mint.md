# Launch mint

Current publisher design: [v1 sources](../assets/sources/website-v1.json), `sr-whitepaper-v1` §§6,11–12,15; retrieval dates remain in source records. Exact settings: [launch parameters](../assets/parameters/launch.json). Design terms are not observed mint or finalization transactions.

## Founding terms

Whitelist entry charges `whitelist-liquidity-fee` with `whitelist-wallet-limit`; `genesis-charters` is the founding allocation. Remaining supply enters a public Dutch auction open to everyone, including whitelist participants. `founding-public-transaction-limit` and `founding-wallet-limit` constrain public transactions and combined holdings across both phases. The source describes exponential decay over `genesis-public-auction-duration` to `genesis-public-auction-floor`, then a fixed floor. The exact executable curve is not established from current source; verified implementation required. [sr-whitepaper-v1: charters]

`founding-proceeds-escrow` and `founding-accrual-start` distinguish this sale from ongoing instant auctions. No founding accrual occurs during distribution; finalization starts all founding charters together. The same described atomic transaction launches liquidity, the tax clock and epoch one. The owner sets `founding-launch-price`; `founding-whitelist-window-control` permits pre-opening changes but freezes timestamps once open. [Genesis](genesis.md) and [reserves](reserves.md) explain the proceeds split. [sr-whitepaper-v1: charters, reserves, immutables]

## Availability and gaps

Exact scheduled clock times and the public opening price: **Not established from current source; verified implementation required.** Wallet eligibility and sale availability require separate authenticated evidence; a design document does not establish either.

The token page displayed the pool as not launched, and the charter page displayed ongoing auctions as not enabled. These source-dated UI observations are not authenticated chain state or proof of subsequent activation. [sr-token-page-v1; sr-charters-page-v1]

[Trading](launch-trading.md) covers taxes and pool settings; [contracts](contracts.md) routes deployment identity and implementation limits. Reading these materials does not authorize a wallet connection or mint.
