# Current updates

On a current/latest update request, freshly read the [official account](https://x.com/standard_rsv) and [developer @0xbeans](https://x.com/0xbeans), then open the relevant original posts. Answer the requested update first, with post links and publication times where available; retrieval time is not publication time. Attribute each statement to its author: developer discussion or a proposed implementation is not automatically an official policy announcement or a deployed change. Distinguish proposals, reported implementation, published source/ABI evidence and freshly observed behavior. If either source is unavailable or coverage is incomplete, say which; do not substitute packaged proposal context for fresh status or infer chronology from discovery order. Explanation-only questions about the reviewed thread can use the context below without a live refresh.

For current auction-day length, availability and prices, use `scripts/snapshot.py` with the `auctions` view. Sold-out closing prices and current price-function outputs are not interchangeable purchase quotes. Read current state rather than inferring implementation from an announcement.

For current issuance, taxes, supply decomposition and restriction flags, use the `protocol` snapshot. For a selected public charter, use the `charter` view with its ID. Distinguish enabled from active restrictions and permanent token burns from ledger retirement; totals do not identify the cause of each removal. The helper reads a fixed publisher ABI at one block; it does not execute trades or reproduce the entire implementation.

Use [documents](documents.md) for published rules, [contracts](contracts.md) for identities, and [planning](planning.md) to turn freshly read observations into approved assumptions. Unavailable state remains unknown. No automatic monitoring or saved-state/source updates.

## Reviewed branch-auction, burn and POL proposal

The [linked @0xbeans thread](https://x.com/0xbeans/status/2101024624914170176) proposes the following changes. This is attributed proposal context, **not a saved current-status verdict or a replacement for published rules**. [Source provenance](../assets/sources/deployments.json), `sr-beans-auction-burn-pol-proposal`, records public-mirror retrieval and its limits; absolute publication time was unavailable.

| Proposal | What the author describes | What it does not establish |
|---|---|---|
| 12-hour branch auctions | Half the daily branch allocation in each auction; unchanged total daily branches and daily dilution | A live auction duration, a changed charter-auction schedule, or twice the daily allocation |
| Branch-auction proceeds | 50% burned immediately, 50% retained in a dedicated protocol incentive vault; no additional mint allocation for those incentives | Half-price licenses, already-distributed rewards, or verified token/ledger settlement accounting |
| Incremental POL | ETH-side bids without pairing acquired STANDARD into additional two-sided liquidity; acquired STANDARD remains in the POL vault | A burn of retained STANDARD, changes to existing LP positions, or guaranteed price/exit-liquidity improvement |

The author says incentive tokens are not for the team, promises allocation restrictions, and proposes burning unused tokens; if none are distributed, the proposed eventual net burn is unchanged. These are intended rules, not verified deployed controls, a distribution schedule or a promise that retained incentives are already burned. The separate buyback-burn vault is explicitly described as unchanged.

The thread says new contract deployment and a separate security review are required, with an estimate of “early next week.” Do not turn that relative estimate into a date, a completed review, or a claim that implementation is live. To establish implementation, obtain current publication/deployment evidence, authenticate changed targets and interfaces, and read relevant state. Existing fixed getters alone do not prove the proceeds split, incentive restrictions or POL strategy; never redirect them to an announced address.

Keep canonical whitepaper parameters and model `"1"` unchanged until reviewed implementation evidence warrants a deliberate update. Explain conflicts with the old full-burn/two-sided-POL descriptions rather than presenting either as verified current behavior. For impact questions, see [auctions](auctions.md), [reserves](reserves.md) and [planner limits](planning-model.md#published-mechanics-versus-fixed-proxies). Any explicitly approved hypothetical sensitivity must fit the existing model and remain labelled as an assumption, not a simulation of these proposed mechanisms.
