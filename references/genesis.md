# Genesis entry

Current design: [v1 sources](../assets/sources/website-v1.json), `sr-whitepaper-v1` §§6,11–12,15. Exact economics: [launch parameters](../assets/parameters/launch.json).

## Paid founding distribution

The whitelist mint charges `whitelist-liquidity-fee`, with `whitelist-wallet-limit`; `genesis-charters` is the founding supply. Remaining charters enter a public Dutch sale open to everyone, including whitelist participants. §6 specifies one charter per public transaction and a combined three-charter wallet cap across both phases. Public pricing decays exponentially to the whitelist price over `genesis-public-auction-duration` and remains there. The exact implementation function is not established by that prose (`genesis-public-auction-curve`); do not borrow the daily-auction equation. [sr-whitepaper-v1: charters]

Exact combined-wallet and public-transaction limits are `founding-wallet-limit` and `founding-public-transaction-limit`; they are distinct from the whitelist claim limit.

Wallet eligibility and live sale availability are not established by the design document. Reading a page does not authorize connecting a wallet or minting.

## Escrow and finalization

Founding proceeds escrow until finalization. Founding charters accrue nothing during the sale; finalization starts accrual for all of them together with epoch one. The owner sets the launch price. In the same described atomic transaction, the pool launches, the tax-decay clock starts and emissions begin. [sr-whitepaper-v1: charters, reserves]

Canonical lifecycle records: `founding-proceeds-escrow`, `founding-accrual-start`, `founding-launch-price`.

The first 25 ETH of accepted proceeds forms a protocol-owned floor bid below launch price. Of the remainder, 60% is held for POL pairing as price discovers, 20% funds contraction and 20% expansion. The token allocation is single-sided above launch price; there is no team share of founding proceeds. `genesis-liquidity-vault-split`, `genesis-protocol-proceeds-share` and `genesis-team-proceeds-share` are authoritative parameter records. This is **not** the ongoing fee split. [sr-whitepaper-v1: currency, reserves, parameters]

The allocation components are `founding-floor-bid`, `founding-pol-remainder-share`, `founding-contraction-remainder-share` and `founding-expansion-remainder-share`; the percentages apply after the floor bid, not to total receipts.

The owner may change the whitelist window only before opening; opening freezes its timestamps. The whitepaper calls the whitelist price and public opening price/curve immutable, but does not itself supply every implementation detail. [sr-whitepaper-v1: immutables]

`founding-whitelist-window-control` records that source policy. Exact scheduled clock times and the public opening price are not established from current source; verified implementation required.

[Launch mint](launch-mint.md) summarizes founding terms and remaining gaps. The token page displayed the pool as not launched; the charter page displayed ongoing auctions not enabled. Those rendered observations do not prove finalization or activation. [sr-token-page-v1; sr-charters-page-v1]
