# Charters and branches

Apply the [preparation and wallet boundary](safety.md#preparation-and-wallet-boundary).

Publisher design reviewed through **2026-09-26**: [sources](../assets/sources/website-v1.json), `sr-whitepaper-v1` §§6–10,12–13 and `sr-charters-page-v1`. Dated reference settings: [participation](../assets/parameters/participation.json) and [launch](../assets/parameters/launch.json), not current configuration.

## How are my branches doing?

Use the supplied public charter ID to read authenticated branch count, ledger balance and meaningful current accrual through host public-read tools. With an address instead, [discover its charters](inspection.md#branch-scope-and-earnings) within a bounded scope; no wallet connection is needed. Answer the requested status naturally with the observation time and material gaps, without unnecessary price or history requests.

Accrued balance belongs to the whole charter, not each branch. The rate equivalent is not earned-today, cash received or a promise of uninterrupted accrual. For earnings over dates, reconcile ledger changes and relevant flows; for net profit, also establish costs and valuation basis. Keep that historical task separate from the useful current summary.

## Charter and branch lifecycle — §§6–7

A charter is an initially soulbound NFT licensing its holder to run a bank and receive issuance. It opens with `initial-branches` and can hold `maximum-branches`. Branches divide issuance pro rata; a new branch earns from opening, not retroactively. An expansion license opens another branch. The whitepaper's full-payment-removal description (`license-burn-share`) is a scoped reference, not a verified current proceeds split; the earlier proposed 50/50 split is not confirmed by either release announcement. Token holding alone does not earn branch issuance or confer governance rights. [sr-whitepaper-v1: charters, branches, currency; sr-token-page-v1; sr-protocol-v1-1-announcement; sr-protocol-v1-2-announcement]

Retirement releases the retired branches' proportional share of accrued balance, net of a resolution fee, and destroys their earning capacity. Retiring the final branch burns the charter. The described return path is purchasing a new charter at auction; a closed charter does not reopen. [sr-whitepaper-v1: charters, exits]

The whitepaper's initial zero charter allocation is older design provenance. [V1.2](updates.md#protocol-v12-announced-changes) announced one charter per branch period and branch limit orders with best-attempt keeper execution. [Authenticate current auctions](contracts.md) before reading availability, allowance or orders; a global bid count is not a wallet's orders.

A fresh market price can mark a whole-charter ledger amount indicatively. That is not wallet tokens, net withdrawal proceeds, NFT resale value or earning capacity. Authenticate both amount and price units, retain their separate observation times, and do not divide by branch count without a reason or use a zero-amount fee preview for the full balance.

Earnings-funded affordability uses **verified unspent earned accrual + contract-derived projected future accrual − commitments and purchases**, excluding deposits and wallet funds. Exclude unknown attribution rather than treating the whole ledger as earnings. Authenticate rates, branch dilution and settlement behavior; stop at an epoch boundary unless an explicitly labelled scenario supplies assumptions beyond it. Keep token costs, price scenarios and network gas distinct. [Policy](protocol-policy.md), [exits](exits.md) and [modeling boundaries](risks.md#what-economics-alone-cannot-establish) explain the financial distinctions.

## Follow the question

- [Genesis entry](genesis.md): paid whitelist/public entry, escrow and common accrual start at finalization. [Launch mint](launch-mint.md) summarizes founding terms and scheduling gaps.
- [Ongoing auctions](auctions.md): branch limit orders, announced charter cadence, observed clocks/capacity and scoped published price rules.
- [Exits and dormancy](exits.md): retirement, published fee formula, qualifying activity, transfer grace and unresolved bounty ordering.
- [Reserves](reserves.md): founding versus ongoing routing, and assets owned by the protocol rather than bankers.
- [Risks](risks.md): owner controls and optional guardian despite non-upgradeability.

The source distinguishes permanent ledger removal from token-deposit conversion; [supply accounting](protocol-policy.md) explains why not every removed ledger unit was a circulating token. Design text does not establish source/ABI correspondence.
