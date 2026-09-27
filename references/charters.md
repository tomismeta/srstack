# Charters and branches

Apply the [preparation and wallet boundary](safety.md#preparation-and-wallet-boundary).

Publisher design reconciled on **2026-09-27**: [sources](../assets/sources/website-v1.json), `sr-whitepaper-v1` §§6–10,12–13 and `sr-charters-page-v1`. The fresh charter guide now says 12-hour charter auctions; retained whitepaper daily wording remains superseded design, not verified deployed timing. Dated reference settings: [participation](../assets/parameters/participation.json) and [launch](../assets/parameters/launch.json), not current configuration.

## How are my branches doing?

Use the supplied public charter ID to read authenticated branch count and whole-charter pending ledger balance through host public-read tools; add current accrual pace only when its calculation is established. With an address instead, [discover its charters](inspection.md#branch-scope-and-earnings) within a bounded scope; no wallet connection is needed. Answer the requested status naturally with observation time and material gaps, without unnecessary price or history requests. The dated [interface guide](interface-guide.md#core-state) supplies read leads.

Pending is not necessarily earned-only, immediately spendable or net withdrawable. An instantaneous rate equivalent is not earned-today, cash received, net profit or a promise of uninterrupted accrual. For earnings over dates, reconcile ledger changes and relevant flows; for profit, establish costs and valuation basis. Current ownership identifies the present holder, not who earned a transferred balance or owned it throughout the interval. Keep these historical tasks separate from a useful current summary.

## Charter and branch lifecycle — §§6–7

A charter is an initially soulbound NFT licensing its holder to run a bank and receive issuance. It opens with `initial-branches` and can hold `maximum-branches`. Branches divide issuance pro rata; a new branch earns from opening, not retroactively. An expansion license opens another branch. The whitepaper's full-payment-removal description (`license-burn-share`) is a scoped reference, not a verified current proceeds split; the earlier proposed 50/50 split is not confirmed by either release announcement. Token holding alone does not earn branch issuance or confer governance rights. [sr-whitepaper-v1: charters, branches, currency; sr-token-page-v1; sr-protocol-v1-1-announcement; sr-protocol-v1-2-announcement]

Retirement releases the retired branches' proportional share of accrued balance, net of a resolution fee, and destroys their earning capacity. Retiring the final branch burns the charter. The described return path is purchasing a new charter at auction; a closed charter does not reopen. [sr-whitepaper-v1: charters, exits]

The whitepaper's initial zero charter allocation is older design provenance. [V1.2](updates.md#protocol-v12-announced-changes) announced one charter per branch period and branch limit orders with best-attempt keeper execution. A **charter auction** creates a new charter and the reviewed purchase event prices it in ETH; a **branch-license auction** expands an existing charter and the reviewed unit price is STANDARD ledger-denominated. Authenticate each family's generation, schedule, inventory, price and payment semantics independently—neither its clock nor floor, cap or price rule transfers to the other. [Authenticate current auctions](contracts.md) before reading availability, allowance or orders; a global license-bid count is not a wallet's orders or unsold charter inventory.

A fresh market price can mark a whole-charter ledger amount indicatively. That is not wallet tokens, net withdrawal proceeds, NFT resale value or earning capacity. Authenticate both amount and price units, retain their separate observation times, and do not divide by branch count without a reason or use a zero-amount fee preview for the full balance.

Earned-only branch-license affordability uses verified unspent earned accrual plus justified projected accrual, less commitments and purchases counted once. Unknown pending origin remains unattributed, not proven earned or proven zero. An all-ledger scenario or a justified upper bound can still answer useful parts of the question; a binding zero purchase bound does not prove provenance. ETH charter affordability is separate unless an explicit, supported conversion model supplies ETH funding and costs. Apply [earned-budget accounting](research-workflow.md#earned-only-projections-and-reinvestment) and [fixed-price/window constraints](research-workflow.md#fixed-price-and-windowed-purchases); deposits, token costs and gas are not interchangeable. [Policy](protocol-policy.md), [exits](exits.md) and [modeling boundaries](risks.md#what-economics-alone-cannot-establish) explain further distinctions.

## Follow the question

- [Genesis entry](genesis.md): paid whitelist/public entry, escrow and common accrual start at finalization. [Launch mint](launch-mint.md) summarizes founding terms and scheduling gaps.
- [Ongoing auctions](auctions.md): branch limit orders, announced charter cadence, observed clocks/capacity and scoped published price rules.
- [Exits and dormancy](exits.md): retirement, published fee formula, qualifying activity, transfer grace and unresolved bounty ordering.
- [Reserves](reserves.md): founding versus ongoing routing, and assets owned by the protocol rather than bankers.
- [Risks](risks.md): owner controls and optional guardian despite non-upgradeability.

The source distinguishes permanent ledger removal from token-deposit conversion; [supply accounting](protocol-policy.md) explains why not every removed ledger unit was a circulating token. Design text does not establish source/ABI correspondence.
