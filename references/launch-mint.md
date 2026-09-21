# Launch mint

Current publisher design: [v1 sources](../assets/sources/website-v1.json), `sr-whitepaper-v1` §§6,11–12,15; retrieval dates remain in source records. Exact settings: [launch parameters](../assets/parameters/launch.json). Design terms are not observed mint or finalization transactions.

## Founding terms

Whitelist entry charges `whitelist-liquidity-fee` with `whitelist-wallet-limit`; `genesis-charters` is the founding allocation. Remaining supply enters a public Dutch auction open to everyone, including whitelist participants. `founding-public-transaction-limit` and `founding-wallet-limit` constrain public transactions and combined holdings across both phases. The source describes exponential decay over `genesis-public-auction-duration` to `genesis-public-auction-floor`, then a fixed floor. The exact deployed curve is not established from current source; verified implementation is required for that claim, not for requested conditional arithmetic using an explicitly assumed curve and opening price. [sr-whitepaper-v1: charters]

`founding-proceeds-escrow` and `founding-accrual-start` distinguish the sale from ongoing auctions. No founding accrual occurs during distribution; finalization starts epoch one for founding charters. `founding-whitelist-window-control` permits pre-opening changes and freezes timestamps once open. Exact founding allocation and token launch-price details are not supplied by the current publication. [Genesis](genesis.md) and [reserves](reserves.md) explain supported terms. [sr-whitepaper-v1: charters, immutables]

## Availability and gaps

Exact scheduled clock times and the public opening price are **not established from current source**. Wallet eligibility and sale availability also require separate authenticated evidence; a design document does not establish them. Assumed times/prices may be used in labeled scenarios, never as a live offer.

For sale availability or finalization, obtain fresh authenticated state through [inspection](inspection.md), using the fixed reader where it covers the question or other host-authorized evidence paths; use [updates](updates.md) for official announcements. If the relevant state cannot be read, report it as unknown. Founding terms alone are not a live offer. [sr-protocol-conditions; sr-publisher-read-interface]

[Trading](launch-trading.md) covers taxes and pool settings; [contracts](contracts.md) routes deployment identity and implementation limits. Requested mint how-to, unsigned preparation and nonbroadcast simulation follow [safety](safety.md); do not request wallet signatures, sign or submit a mint.
