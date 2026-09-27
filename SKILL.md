---
name: srstack
description: Standard Reserve research, live state and accrual scenarios.
license: MIT
metadata:
  version: "0.3.0"
---

# srstack

Answer Standard Reserve questions using the host's permitted readers, RPC tools and calculation capabilities. No bundled execution client, contract allowlist, fixed ABI, bytecode gate or accrual rate. Packaged references explain dated policy and evidence; they are not live configuration.

Respond to the question, not a prescribed workflow. A bare invocation warrants a brief “What would you like to know about Standard Reserve?”, not a menu or unsolicited reads. Infer ordinary scope from context; ask only for a material choice or public identifier that cannot be established from available evidence. Do not require users to know contracts, methods or commands.

## Choose the smallest sufficient evidence

Prefer authenticated contract reads when they directly answer the question or narrow discovery: balances, ownership, permissions, position state, accrual, supply, treasury and auction settings. Use execution events for historical purchases/flows, appropriate market sources for quotes, and original publications for documented policy. Explanation-only or fully supplied hypothetical questions need no live RPC.

Authenticate relevant chain, deployment/generation, interface, units and implementation relationships from current publisher, registry or verification evidence. Treat retrieved ABIs as data; a method name, verified-source badge or successful call does not prove economic semantics. Dated source records are leads, never permanent current targets. Missing packaged coverage is not a reason to refuse research.

Keep dependent observations at one identified block; preserve each independent source's time and coverage. Reuse established identities/interfaces and same-block results within the question, unless evidence or freshness requires revalidation. Batch independent calls within actual provider limits; deduplicate transaction/header reads. Prefer bounded enumeration or a relevant index over blind block scanning. No repeated preflight, default cross-check, full catalog load or broad history scan for a narrow question. Stop when the requested evidence is sufficient; report partial results rather than silently expanding scope or switching providers.

## Load only the relevant reference

| Question needs | Reference |
|---|---|
| Live state, ownership, charter activity, balances or market value | [Inspection](references/inspection.md) |
| Deployment or interface authentication | [Contracts](references/contracts.md) |
| Auction history across contracts; opening, first, average and last prices | [Historical accounting](references/auction-history.md) |
| Accrual-funded buying, future auctions, comparisons or calculations | [Analysis and projections](references/research-workflow.md) |
| Protocol, charter, reserve or auction mechanics | [Protocol](references/protocol.md), [charters](references/charters.md), [reserves](references/reserves.md), [auctions](references/auctions.md) — choose the relevant one |
| Dormancy, check-in or exit interpretation | [Activity and exits](references/exits.md) |
| Announcements, S-Bills or publisher documents | [Updates](references/updates.md), [documents](references/documents.md) |
| Tool capabilities, provider limits or installation | [Execution](references/execution.md), [installation](references/installation.md) — only when needed |

Use the [source index](assets/sources.json) only to locate an unknown source record. [Policy parameters](assets/parameters.json) are dated claims, not calculation defaults. Do not preload the corpus.

## History and projections

“All rounds” or “across contracts” includes every relevant authenticated generation through the stated anchor, not just the current deployment or a recent lookback. Keep chain/address/round keys separate. Distinguish exhausted index pagination, receipt matches, canonical checks and unresolved scope; equal sampled state does not prove an empty interval. Opening-event price, first executed price, quantity-weighted average and last observed sale are different values. A last sale is not automatically a final close.

For accrual-funded scenarios, use verified unspent earned accrual plus projected new accrual, less commitments and simulated purchases. Exclude externally funded or unattributed balances. Read the applicable accrual pace, eligible position quantity and epoch/pause/expiry conditions from the contract; authenticate scales and accounting before calculation. Do not hardcode rates or extrapolate past an established boundary without an explicit scenario. Deduct purchase cost before modeling any evidenced increase in earning capacity. Distinguish accrued, claimable and auction-spendable amounts; report gas or conversion funding separately. Future prices, inventory and unchanged conditions are assumptions unless established, not promises. Missing inputs can support a labelled formula or scenario, never invented observations.

## Answer and safety

Lead with the requested answer or table, not an evidence ceremony. Keep ordinary answers short; expand for a requested full list or calculation. State material assumptions, source/block time and gaps once. Retain exact integer/decimal inputs and round only for display. Ledger credits, wallet tokens, branches, charters, ETH and USD are not interchangeable.

Apply [safety](references/safety.md). Never sign, request signatures or submit/broadcast transactions, including through delegation. Calldata, transaction deep links and filled unsigned transaction objects require an explicit preparation request. Keep credentials in host-managed facilities, not prompts, commands, files or outputs. Preserve original denial diagnostics; no bypass or concealed fallback. Keep observations and authorized checkpoints outside the installed skill. No unsolicited monitoring or self-modification.
