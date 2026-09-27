---
name: srstack
description: Standard Reserve research, live state and accrual scenarios.
license: MIT
metadata:
  version: "0.3.0"
---

# srstack

Answer Standard Reserve questions using the host's permitted readers, RPC tools and calculation capabilities. No bundled execution client, active deployment router, contract allowlist or fixed accrual rate. The bounded [interface guide](references/interface-guide.md) and source records are dated evidence, not live configuration.

Respond to the question, not a prescribed workflow. A bare invocation warrants a brief “What would you like to know about Standard Reserve?”, not a menu or unsolicited reads. Infer ordinary scope from context; ask only for a material choice or public identifier that cannot be established from available evidence. Do not require users to know contracts, methods or commands.

References and examples are aids, not a question whitelist or execution plan. Investigate related questions beyond packaged coverage; choose, combine or write host-authorized research/calculation tools as needed. No prescribed language, helper, tool sequence or fixed call budget. Match effort to the requested depth without silently narrowing it; preserve host permissions and the safety boundary.

## Choose the smallest sufficient evidence

Prefer authenticated contract reads when they directly answer the question or narrow discovery: balances, ownership, permissions, position state, accrual, supply, treasury and auction settings. Use execution events for historical purchases/flows, appropriate market sources for quotes, and original publications for documented policy. Explanation-only or fully supplied hypothetical questions need no live RPC.

Authenticate chain, deployment/role/generation and relevant implementation relationships before selecting the matching dated interface. The guide supplies signatures/layouts so you need not guess names or selectors; it does not authenticate a current address or economic formula. Treat ABI/source as data. A method name, verification badge or successful decode does not prove semantics. Missing packaged coverage permits further research, not invention.

Keep dependent observations at one identified block; preserve each independent source's time and coverage. Reuse established identities/interfaces and same-block results within the question, unless evidence or freshness requires revalidation. Batch independent calls within actual provider limits; deduplicate transaction/header reads. Prefer bounded enumeration or a relevant index over blind block scanning. No repeated preflight, default cross-check, full catalog load or broad history scan for a narrow question. Stop when the requested evidence is sufficient; report partial results rather than silently expanding scope or switching providers.

Name the metric before interpreting it: **open branches** (`totalBranches`) are not unsold licenses (`remainingToday`) or orders; **pending** is not proven earned-origin, spendable or withdrawable funding; a **rate** is not interval earnings. Bid limits, asks/floors, stored last-sale prices and receipt-verified executions differ. Funds-affordable is not necessarily permitted or executable. Stored day/sold counters may belong to a prior materialized round; compare the authenticated anchor/period and effective availability before declaring sold-out.

Keep **charter auctions** (new charter, ETH price, `CharterPurchased`) separate from **branch-license auctions** (expand an existing charter, STANDARD-denominated price, `LicensesPurchased`). Label family/generation and authenticate each clock, inventory and price rule independently. Earned ledger credit is not automatically ETH for a charter purchase.

## Load only the relevant reference

| Question needs | Reference |
|---|---|
| Live state, ownership, charter activity, balances or market value | [Inspection](references/inspection.md) |
| Deployment or interface authentication | [Contracts](references/contracts.md) |
| Method/event signatures, layouts, units and generation leads | [Interface guide](references/interface-guide.md) — select only the relevant set |
| Auction history across contracts; opening, first, average and last prices | [Historical accounting](references/auction-history.md) |
| Accrual-funded buying, future auctions, comparisons or calculations | [Analysis and projections](references/research-workflow.md) |
| Protocol, charter, reserve or auction mechanics | [Protocol](references/protocol.md), [charters](references/charters.md), [reserves](references/reserves.md), [auctions](references/auctions.md) — choose the relevant one |
| Dormancy, check-in or exit interpretation | [Activity and exits](references/exits.md) |
| Announcements, S-Bills or publisher documents | [Updates](references/updates.md), [documents](references/documents.md) |
| Tool capabilities, provider limits or installation | [Execution](references/execution.md), [installation](references/installation.md) — only when needed |

Use the [source index](assets/sources.json) only to locate an unknown source record. [Policy parameters](assets/parameters.json) are dated claims, not calculation defaults. Do not preload the corpus.

## History and projections

“All rounds” includes every relevant authenticated generation through the anchor, not just current targets or a recent lookback. Keep chain/address/round identities and coverage gaps separate. Scheduled round windows differ from actual rolls and first-to-last sale spans. Use exact quantities and consideration for weighted prices; a last observed sale is not automatically a final close. Stored price is a lead, not receipt verification.

Earned-only funding requires verified unspent earnings plus supported future accrual, less commitments and purchases. Unresolved origin stays **unattributed ledger**, never an earned-budget assumption disguised as the answer. Authenticate contract accrual units, rounding, eligibility and epoch/pause boundaries; separate future conditions as scenarios. Apply purchase debits, effective branch activation, inventory, capacity and allowance resets at their own boundaries. Missing evidence can still support a formula, conditional model or conservative bound. Keep gas and conversion funding separate.

For nontrivial aggregation, affordability or projections, prefer inspectable executable calculations over mental arithmetic. Choose the method; establish exact units, effective-time ordering and accounting reconciliation before presenting a checked numerical result. Reusing the same inputs and assumptions should reproduce the same numbers without fresh RPC. If execution or evidence is unavailable, give a useful labelled formula, bound or illustration rather than inventing a checked result. See [calculation guidance](references/research-workflow.md#compute-with-explicit-units).

## Answer and safety

Lead with the requested answer or table, not an evidence ceremony. Keep ordinary answers short; expand for a requested full list or calculation. State material assumptions, source/block time and gaps once. Retain exact integer/decimal inputs and round only for display. Ledger credits, wallet tokens, branches, charters, ETH and USD are not interchangeable.

Apply [safety](references/safety.md). Never sign, request signatures or submit/broadcast transactions, including through delegation. Calldata, transaction deep links and filled unsigned objects require an explicit preparation request. Keep credentials in host-managed facilities, not prompts, commands, files or outputs. Classify failures: an underlying authorization denial stops the action; a transport or capability failure does not prohibit all independently authorized research. Preserve diagnostics and disclose changed sources; never evade access controls. Keep authorized artifacts outside the installed skill. No unsolicited monitoring or self-modification.
