# Launch mint: current design and dated schedule

Current design: [v1 sources](../assets/sources/website-v1.json), `sr-whitepaper-v1` §§6,11–12,15, captured 2026-09-14T22:15:13.789Z. The earlier thread was reviewed through 2026-09-14T16:40:35Z; [mint records](../assets/sources/launch-mint.json) and [trading records](../assets/sources/launch-trading.json) preserve it. Exact values and their histories: [launch parameters](../assets/parameters/launch.json). None is an observed mint/finalization transaction.

## Current founding terms

Whitelist entry charges `whitelist-liquidity-fee` with `whitelist-wallet-limit`; `genesis-charters` is the founding allocation. All remaining supply goes to a public Dutch auction open to everyone, whitelist participants included. `founding-public-transaction-limit` and `founding-wallet-limit` constrain public transactions and combined holdings across the two phases. The public sale decays exponentially for `genesis-public-auction-duration` to `genesis-public-auction-floor`, then remains there. `genesis-public-auction-curve` retains the absence of an exact implementation function; do not substitute the ongoing daily curve. The opening price's announcement provenance remains separate from the paper's immutability claim. [sr-whitepaper-v1: charters, immutables]

`founding-proceeds-escrow` and `founding-accrual-start` distinguish this sale from ongoing instant auctions. No founding accrual occurs during distribution; finalization starts all founding charters together. The same described atomic transaction launches liquidity, the tax clock and epoch one. The owner sets `founding-launch-price`; `founding-whitelist-window-control` allows pre-opening changes but freezes timestamps once open. [Genesis](genesis.md) and [reserves](reserves.md) explain the now-published proceeds split. [sr-whitepaper-v1: charters, reserves, immutables]

## Earlier announcement schedule, preserved rather than repaired

The [root](https://x.com/standard_rsv/status/2098969960404103353) says “in 2 days, on 9/14.” RSS supplies September 13 UTC; the individual X page displayed September 12 at 9:00 PM while the profile displayed September 13. Do not convert the relative phrase into an exact publication clock. [sr-post-2098969960404103353]

[Mint Details](https://x.com/standard_rsv/status/2098969964283846751) and [Mint Schedule](https://x.com/standard_rsv/status/2098969968201359736) announce the whitelist window followed by the remaining public sale. Canonical schedule records are `whitelist-window-start`, `whitelist-window-end`, `whitelist-window-duration`, `genesis-public-auction-end`, `genesis-public-auction-duration`, `genesis-public-auction-start-price` and `genesis-public-auction-floor`.

The schedule says **EST literally in September**. Do not silently substitute EDT or invent a UTC conversion. Its image distinguishes token launch **without liquidity** at allowlist opening from later liquidity addition, auction closing and emissions. Current finalization prose supplies the design relationship, not proof that the announced clock schedule was executed. [sr-post-2098969968201359736; sr-whitepaper-v1: reserves]

The [closing reply](https://x.com/standard_rsv/status/2098969986190733410) repeats the event date and its reviewed image marks the thread's last post. That boundary is not an entire-account archive guarantee. Robinhood branding in launch graphics alone does not authenticate deployment or partnership scope; [contracts](contracts.md) retains the later, separately sourced directory/condition evidence.

[Trading](launch-trading.md) covers conflicting launch-tax descriptions and activation. [History](announcement-history.md) records the superseded free-mint promise; [genesis](genesis.md) covers selection and eligibility boundaries.
