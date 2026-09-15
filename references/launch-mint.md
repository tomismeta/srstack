# Launch mint

Current publisher design: [v1 sources](../assets/sources/website-v1.json), `sr-whitepaper-v1` §§6,11–12,15; retrieval dates remain in source records. Exact settings: [launch parameters](../assets/parameters/launch.json). Design terms are not observed mint or finalization transactions.

## Founding terms

Whitelist entry charges `whitelist-liquidity-fee` with `whitelist-wallet-limit`; `genesis-charters` is the founding allocation. Remaining supply enters a public Dutch auction open to everyone, including whitelist participants. `founding-public-transaction-limit` and `founding-wallet-limit` constrain public transactions and combined holdings across both phases. The source describes exponential decay over `genesis-public-auction-duration` to `genesis-public-auction-floor`, then a fixed floor. The exact executable curve is not established from current source; verified implementation required. [sr-whitepaper-v1: charters]

`founding-proceeds-escrow` and `founding-accrual-start` distinguish the sale from ongoing auctions. No founding accrual occurs during distribution; finalization starts epoch one for founding charters. `founding-whitelist-window-control` permits pre-opening changes and freezes timestamps once open. Exact founding allocation and token launch-price details are not supplied by the current publication. [Genesis](genesis.md) and [reserves](reserves.md) explain supported terms. [sr-whitepaper-v1: charters, immutables]

## Availability and gaps

Exact scheduled clock times and the public opening price: **Not established from current source; verified implementation required.** Wallet eligibility and sale availability require separate authenticated evidence; a design document does not establish either.

The latest official recap reports the public founding sale sold out in 11 seconds. The protocol page now displays a live first epoch. Use current snapshot status for availability; do not offer a completed founding sale as an executable opportunity. [sr-recap-genesis; sr-protocol-conditions]

[Trading](launch-trading.md) covers taxes and pool settings; [contracts](contracts.md) routes deployment identity and implementation limits. Reading these materials does not authorize a wallet connection or mint.
