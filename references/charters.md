# Charters and branches

Publisher design: [current sources](../assets/sources/website-v1.json), `sr-whitepaper-v1` §§6–10,12–13 and `sr-charters-page-v1`. Exact ongoing settings: [participation parameters](../assets/parameters/participation.json); founding settings: [launch parameters](../assets/parameters/launch.json).

## Charter and branch lifecycle — §§6–7

A charter is an initially soulbound NFT licensing its holder to run a bank and receive issuance. It opens with `initial-branches` and can hold `maximum-branches`. Branches divide issuance pro rata; a new branch earns from opening, not retroactively. An expansion license opens another branch and permanently removes its payment value (`license-burn-share`). Token holding alone does not earn branch issuance or confer governance rights. [sr-whitepaper-v1: charters, branches, currency; sr-token-page-v1]

Retirement releases the retired branches' proportional share of accrued balance, net of a resolution fee, and destroys their earning capacity. Retiring the final branch burns the charter. The described return path is purchasing a new charter at auction; a closed charter does not reopen. [sr-whitepaper-v1: charters, exits]

The whitepaper places founding distribution before one-time license activation and defines `initial-daily-charter-count` as the initial daily charter supply. Those are lifecycle rules, not current availability. Use a fresh `auctions` snapshot for activation and inventory; unavailable reads leave the requested status unknown. [sr-whitepaper-v1: branches, auctions; sr-publisher-read-interface]

For “what is my charter worth now?”, use [inspection](inspection.md)'s shared price path: ask only for a missing public charter ID, read fresh `charter_pending`, then pass that whole-charter STANDARD amount to `price.py` for same-quote gross arithmetic. No wallet scan or redundant permission prompt is needed for the requested current value. This is a gross indicative mark on accrued ledger balance, not wallet tokens, net withdrawal proceeds, charter/NFT resale value or earning capacity. Do not automatically divide by branch count; the zero-amount withdrawal-fee preview does not price withdrawal of that balance. Snapshot block and API retrieval are separate clocks, with provider price-observation time unknown.

## Follow the question

- [Genesis entry](genesis.md): paid whitelist/public entry, escrow and common accrual start at finalization. [Launch mint](launch-mint.md) summarizes founding terms and scheduling gaps.
- [Ongoing auctions](auctions.md): separate license/charter opens, capacity and a price-curve gap.
- [Exits and dormancy](exits.md): retirement, published fee formula, qualifying activity, transfer grace and unresolved bounty ordering.
- [Reserves](reserves.md): founding versus ongoing routing, and assets owned by the protocol rather than bankers.
- [Risks](risks.md): owner controls and optional guardian despite non-upgradeability.

The source distinguishes permanent ledger removal from token-deposit conversion; [supply accounting](protocol-policy.md) explains why not every removed ledger unit was a circulating token. Design text does not establish source/ABI correspondence.
