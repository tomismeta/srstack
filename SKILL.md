---
name: srstack
description: Standard Reserve research, auctions, charters, orderbook.
license: MIT
metadata:
  version: "0.3.0"
---

# srstack

Research Standard Reserve and inspect public protocol, charter, auction and orderbook state. Prefer the bundled commands where they fit; use authenticated supplemental evidence for gaps.

Helpers need permitted Python 3.10+ execution and network access for live reads. Packaged explanations and calculations can work offline.

## Answer style

Lead with the answer or useful numbers. Default to 3–6 useful lines: a short paragraph or small table, not both repeating facts. Normally cite one or two useful links and a short observation time. Include only material caveats/gaps; raw evidence, hashes and call mappings are opt-in.

Snapshot summary output is compact in the helper itself; `--detail full` opts into raw evidence. Keep that distinction when presenting results rather than retrieving full output only to hide it.

For only `srstack`, `Use srstack` or a host equivalent, show this menu without reads:
- **research** — Source-grounded explanations and evidence gaps.
- **inspect** — On-demand public protocol, auction, charter or treasury state, bounded auction/buyback history, STANDARD price or gross accrued-balance value.
- **analyse** — Calculations, conditional forecasts, scenarios, comparisons and plans using evidence and explicit assumptions.
- **workflows** — User-requested reports, exports and bounded automation under [host permissions](references/safety.md).

Research topics: **protocol · charters · reserves · contracts · updates · documents · risks**.

## Route, then load only what is needed

| Intent | First resource |
|---|---|
| “How are my branches doing?” / charter N earnings | `python3 -B -I scripts/snapshot.py charter --id N`: report branches, accrued STANDARD and current-rate daily equivalent. No price lookup unless requested. For an address rather than an ID, use scoped ownership discovery. |
| Dormancy / last activity / do I need to check in? | `python3 -B -I scripts/snapshot.py charter --id N --detail activity`: owner and raw activity/transfer/period getters. Deadline, dormancy status and last check-in stay unknown without authenticated semantics; `lastActive` is not specifically check-in. [Activity interpretation](references/exits.md#inspect-one-charters-activity). |
| Current branch/license auction status or price | `python3 -B -I scripts/snapshot.py auctions`: report license availability, remaining quantity, usable price and observation time. No history scan or contract rediscovery. |
| “What will the next license round open at?” / “When does it start?” | Run `python3 -B -I scripts/snapshot.py auctions`; use its [conditional policy preview and derived schedule](references/auctions.md#next-license-opening-documented-policy-estimate). No sales plus an unavailable next-round floor means **unknown opening price**, not today's floor as a fallback. A supported sale-based candidate is provisional and floor-qualified; a scheduled boundary is not keeper execution. |
| Branch limit orders / “what's on the book?” | `python3 -B -I scripts/snapshot.py orderbook --start 0 --count 20`: a bounded raw-ID page, **not a price/quantity/owner listing**. Optional `--charter-ids N,M` reads independently known charter bids/fillability. Never autojoin page IDs or promise fills. [Interpretation](references/auctions.md). |
| Charter-auction launch or cadence | [Protocol v1.2](references/updates.md#protocol-v12-announced-changes): announced one charter at branch-auction cadence; 5.5 ETH is the announced first opening, not a current quote. Use fresh auction observations and surface any interface/schedule conflict rather than imposing the older 24-hour design. |
| Current state, burns, cap/gate, owners, charter balance/worth or STANDARD price | [Inspection common paths](references/inspection.md#common-question-paths) |
| Last N rounds / auction purchases or revenue | `python3 -B -I scripts/history.py license --generation current --last-rounds 3`: newest-first, observed rounds only. A young deployment may have one; missing events leave prices unknown. No cross-generation backfill. See [coverage and other history scopes](references/auction-history.md#question-to-window). |
| Treasury routing, team liability, buyback controls or a specified reserve asset | [Inspection common paths](references/inspection.md#common-question-paths): `snapshot.py treasury`, optional `--asset ADDRESS`; approval-gated raw holdings, not a portfolio |
| Past buybacks | [Bounded history helper](references/auction-history.md): `history.py buybacks` for ContractionVault burn accounting; `history.py pol-buybacks` for POL event-reported ETH, raw token output and destination, not burns |
| Second Mandate, manifesto, tokenized-stock liquidity vision or sample positions | [Second Mandate](references/updates.md#second-mandate-liquidity-for-tokenized-stocks) |
| “How are my S-Bills doing?” / staking positions | [Position inspection](references/inspection.md#common-question-paths): use a supplied public bill ID/address or user-consented position export; establish the actual deployment/read surface, never substitute preview samples or an old availability label. |
| Burn/ledger retirement or epoch rules, without live values | [Supply and epoch policy](references/protocol-policy.md) |
| Successor migration versus code upgradeability | [Source-reviewed mechanics](references/contracts.md#source-reviewed-mechanics-versus-publisher-abi-leads) |
| Cap/gate mechanics or transaction-success limits, without live state | [Launch restrictions](references/launch-trading.md#enabled-versus-active-restrictions) |
| Contract identity, address, chain or deployment evidence | [Contracts](references/contracts.md) |
| Holdings, income, flows, LP fees or reconciliation | [Research workflow](references/research-workflow.md) |
| Estimates, time-to-target, scenarios, strategy comparisons or user-supplied data | [Research workflow](references/research-workflow.md) plus the relevant mechanics reference; distinguish observations from assumptions |
| Setup, host loading or release identity | [Installation](references/installation.md) |
| Protocol / charters / reserves | [Protocol](references/protocol.md) / [charters](references/charters.md) / [reserves](references/reserves.md) |
| Updates / documents / risks | [Updates](references/updates.md) / [documents](references/documents.md) / [risks](references/risks.md) |

Specific intent wins over broad topic. Explanation-only questions need no live refresh. Follow the direct link; use the [source](assets/sources.json) or [parameter](assets/parameters.json) index only to locate an unknown ID. Do not preload whole guides or all references. Recover relevant truncation before claiming coverage.

For auctions, distinguish stored counters from elapsed rounds and auction periods from charter cap windows. Label pending rollover; never combine stale sales with current availability as “sold today.” Current state uses getters; purchases/revenue use history. Failed reads stay unavailable.

For orderbook and last-N history, prefer host-managed `SRSTACK_RPC_URL` or `ALCHEMY_API_KEY`; the public default is best-effort for small snapshots. Helpers never silently fail over. A 401/403 is a blocked request, not a failed install. Keep secrets out of prompts/files/CLI arguments. [Provider configuration](references/execution.md#rpc-provider-guidance).

For requested estimates and comparisons, calculate with explicit inputs, assumptions and units. Ask only for material missing choices. Uncertainty permits labelled models, not invented facts or guaranteed returns.

## Evidence and operational boundaries

- Current claims need fresh evidence; historical observations keep their original time/block. Distinguish rules, proposals, samples, observations and estimates. Missing evidence is unknown, not zero; sample positions are not holdings or entitlements.
- Preserve units: ledger STANDARD is not wallet tokens, branches are not charters, and USD is not ETH or implicitly a stablecoin. Rate equivalents are not promised earnings; gross accrued value is not net proceeds or charter resale value.
- Apply [safety](references/safety.md) for access and execution. Never sign, request signatures or submit/broadcast transactions, including through delegation. Calldata, transaction deep links and filled unsigned transaction objects require an **explicit request to prepare them**; an inspect or explanation request is not authorization.
- Default Robinhood Chain explorer links to `https://robin.etherscan.io/`: `/address/ADDRESS`, `/tx/HASH`, `/block/NUMBER`. Retain other providers' actual evidence URLs only as provenance. Bytecode, publisher ABI, Similar Match and exact source verification are distinct.
- Preserve original denial diagnostics and host controls. Independent sources require their own identity, time/block and coverage evidence; never present a failed helper as successful or use installed snapshots as fallback state.
