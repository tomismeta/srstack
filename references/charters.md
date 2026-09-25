# Charters and branches

Publisher design: [current sources](../assets/sources/website-v1.json), `sr-whitepaper-v1` §§6–10,12–13 and `sr-charters-page-v1`. Exact ongoing settings: [participation parameters](../assets/parameters/participation.json); founding settings: [launch parameters](../assets/parameters/launch.json).

## How are my branches doing?

With a public charter ID, run `python3 -B -I scripts/snapshot.py charter --id ID` (replace `ID`, never guess it). Default to one row: **charter / branches / accrued STANDARD / current-rate equivalent STANDARD per day**, plus observation time or the specific unavailable field. No price, full protocol context or history scan is needed. With a public address instead, [discover its charters](inspection.md#branch-scope-and-earnings) using bounded public evidence, then inspect the identified IDs; no wallet connection is required.

Accrued balance belongs to the whole charter, not each branch. The rate equivalent is not earned-today, cash received or a promise of uninterrupted accrual. For earnings over dates, reconcile ledger changes and relevant flows; for net profit, also establish costs and valuation basis. Keep that historical task separate from the useful current summary.

## Charter and branch lifecycle — §§6–7

A charter is an initially soulbound NFT licensing its holder to run a bank and receive issuance. It opens with `initial-branches` and can hold `maximum-branches`. Branches divide issuance pro rata; a new branch earns from opening, not retroactively. An expansion license opens another branch. The whitepaper's full-payment-removal description (`license-burn-share`) is a scoped reference, not a verified current v1.1 split; the earlier proposed 50/50 split is not confirmed. Token holding alone does not earn branch issuance or confer governance rights. [sr-whitepaper-v1: charters, branches, currency; sr-token-page-v1; sr-protocol-v1-1-announcement]

Retirement releases the retired branches' proportional share of accrued balance, net of a resolution fee, and destroys their earning capacity. Retiring the final branch burns the charter. The described return path is purchasing a new charter at auction; a closed charter does not reopen. [sr-whitepaper-v1: charters, exits]

The whitepaper places founding distribution before one-time license activation and defines `initial-daily-charter-count` as the initial charter supply. The replacement v1.1 license auction has separately corroborated historical cutover/start evidence; that is not current availability. Use `snapshot.py auctions` directly with its pinned current interface for live activation and round inventory. No rediscovery or historical scan is needed. Charter-specific allowance getters require authenticated supplemental reads, not an invented auction-profile ID argument. Stored-round counters may lag lazy rollover; the 12-hour license round is separate from the 24-hour charter cap window. Missing reads leave the requested state unknown. [sr-v1-1-deployment-evidence; sr-v1-1-read-interface]

For “what is my charter worth now?”, follow [inspection](inspection.md)'s price path: read fresh `charter_pending`, then pass its exact whole-charter STANDARD amount to `price.py`. This is a gross indicative accrued-ledger mark, not wallet tokens, net withdrawal proceeds, NFT resale value or earning capacity. Do not automatically divide by branch count; a zero-amount fee preview does not price withdrawal of that balance. RPC block and price retrieval are separate clocks.

For requested earning projections, time-to-target or branch/exit strategy comparisons, use the [policy formulas](protocol-policy.md) and [exit rules](exits.md) with explicit assumptions for changing branch counts, rates, settlement and fees. These estimates are distinct from the gross mark above and do not require verified implementation unless presented as deployed behavior; follow [modeling boundaries](risks.md#what-economics-alone-cannot-establish).

## Follow the question

- [Genesis entry](genesis.md): paid whitelist/public entry, escrow and common accrual start at finalization. [Launch mint](launch-mint.md) summarizes founding terms and scheduling gaps.
- [Ongoing auctions](auctions.md): separate license/charter clocks, capacity and published price rules.
- [Exits and dormancy](exits.md): retirement, published fee formula, qualifying activity, transfer grace and unresolved bounty ordering.
- [Reserves](reserves.md): founding versus ongoing routing, and assets owned by the protocol rather than bankers.
- [Risks](risks.md): owner controls and optional guardian despite non-upgradeability.

The source distinguishes permanent ledger removal from token-deposit conversion; [supply accounting](protocol-policy.md) explains why not every removed ledger unit was a circulating token. Design text does not establish source/ABI correspondence.
