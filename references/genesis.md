# Genesis entry

Current design: [v1 sources](../assets/sources/website-v1.json), `sr-whitepaper-v1` §§6,11–12,15. Exact economics: [launch parameters](../assets/parameters/launch.json).

## Paid founding distribution

The whitelist mint charges `whitelist-liquidity-fee`, with `whitelist-wallet-limit`; `genesis-charters` is the founding supply. Remaining charters enter a public Dutch sale open to everyone, including whitelist participants. §6 specifies one charter per public transaction and a combined three-charter wallet cap across both phases. Public pricing decays exponentially to the whitelist price over `genesis-public-auction-duration` and remains there. The exact implementation function is not established by that prose (`genesis-public-auction-curve`); do not borrow the daily-auction equation. [sr-whitepaper-v1: charters]

Exact combined-wallet and public-transaction limits are `founding-wallet-limit` and `founding-public-transaction-limit`; they are distinct from the whitelist claim limit.

Wallet eligibility and live sale availability are not established by the design document. Reading a page does not authorize connecting a wallet or minting.

## Escrow and finalization

Founding proceeds escrow until finalization. Founding charters accrue nothing during the sale; finalization starts them together with epoch one. [sr-whitepaper-v1: charters]

Canonical lifecycle records: `founding-proceeds-escrow`, `founding-accrual-start`, `founding-launch-price`.

The documented founding proceeds fund initial liquidity and protocol vaults, with no team share. The current document does not specify an exact allocation. `genesis-liquidity-vault-split`, `genesis-protocol-proceeds-share` and `genesis-team-proceeds-share` hold the supported values and gaps. [sr-whitepaper-v1: charters]


The owner may change the whitelist window only before opening; opening freezes its timestamps. The whitepaper calls the whitelist price and public opening price/curve immutable, but does not itself supply every implementation detail. [sr-whitepaper-v1: immutables]

`founding-whitelist-window-control` records that source policy. Exact scheduled clock times and the public opening price are not established from current source; verified implementation required.

[Launch mint](launch-mint.md) summarizes founding terms. Use fresh authenticated reads for current availability and finalization, and [updates](updates.md) for official announcements. If the requested state cannot be read, report it as unknown; founding terms do not establish a live offer. [sr-protocol-conditions; sr-publisher-read-interface]
