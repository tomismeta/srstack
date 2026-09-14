# Launch mint thread and schedule

Reviewed through 2026-09-14T16:40:35Z. [Mint source records](../assets/sources/launch-mint.json) preserve the root, terms, schedule and closing; [trading source records](../assets/sources/launch-trading.json) hold both intervening continuations. Exact settings: [launch parameters](../assets/parameters/launch.json). These are announced events, not observed activation.

The [root announcement](https://x.com/standard_rsv/status/2098969960404103353) (`sr-post-2098969960404103353`) says “in 2 days, on 9/14.” RSS supplies September 13 UTC; the individual X page displayed September 12 at 9:00 PM while the profile displayed September 13. Preserve these source representations rather than silently changing the wording or treating the relative countdown as an exact clock.

- **Mint sequence.** [Mint Details](https://x.com/standard_rsv/status/2098969964283846751) and [Mint Schedule](https://x.com/standard_rsv/status/2098969968201359736) describe a whitelist window followed immediately by a public descending Dutch auction of the remaining Genesis Charters. Canonical records: `whitelist-window-start`, `whitelist-window-end`, `whitelist-window-duration`, `genesis-public-auction-end`, `genesis-public-auction-duration`, `genesis-public-auction-start-price`, `genesis-public-auction-floor` and `genesis-public-auction-curve`.
- **Timezone and image detail.** The schedule uses **EST literally**. Do not silently substitute EDT or publish a UTC conversion without resolving that label. Its reviewed timetable says the token launches **without liquidity** when the allowlist opens; liquidity is added, the public auction closes and charter emissions begin at the later scheduled point. This describes a proposed sequence, not observed token issuance or tradability.

- **Thread boundary.** The [closing reply](https://x.com/standard_rsv/status/2098969986190733410) repeats the event date; its reviewed image says it is the last post in the thread. This identifies the publisher's thread boundary, not completeness of all account replies.

The root and earlier launch graphics contain Robinhood branding. Branding alone does not authenticate a network, contract deployment or partnership scope; use [contracts](contracts.md) for the evidence boundary.

The genesis public auction’s exact decay function is not disclosed (`genesis-public-auction-curve`); do not borrow the ongoing daily auction curve or duration. [sr-post-2098969968201359736]

[Genesis entry](genesis.md) covers current selection/cost/proceeds. [Trading continuation](launch-trading.md) preserves the tax graphic and day-one sequence. [History](announcement-history.md) records the superseded free-mint terms.
