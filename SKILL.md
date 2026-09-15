---
name: srstack
description: Standard Reserve research, planning, and public inspection.
license: MIT
compatibility: Python 3.10+ for fixed helpers; network access for live public RPC, indicative prices and web research. Packaged research and scenario calculations work offline.
metadata:
  version: "0.2.0"
---

# srstack

Independent Standard Reserve research, guided scenario planning and bounded public reads. Use existing host permissions; no wallet or transaction actions.

## Answer style

Lead with the answer, useful numbers or next question—not a disclaimer. For a simple question use a short paragraph or small table, not both repeating the same facts. Default to roughly 3–6 useful lines; expand only when the question needs it.

Use at most one short caveat when it changes interpretation: **“Estimate; inputs held constant.”** or **“RPC snapshot using publisher ABI.”** Mark missing values and excluded costs directly. Do not repeat generic warnings, long limitations or provenance tables.

Normally cite one or two useful source links. A short observation time is enough when freshness matters; omit block numbers/hashes unless requested. Keep raw responses, call mappings and detailed assumptions available on request. Never call publisher-ABI reads source-verified or present estimates as guaranteed returns.

## Bare invocation

For only `srstack`, `Use srstack` or a host equivalent, print this menu without reads or requests:

- **research** — Source-grounded explanations and evidence gaps.
- **plan** — Guided hypothetical comparison; approve assumptions in plain language, then run the permitted local planner.
- **inspect** — On-demand public protocol, auction or charter snapshot, current STANDARD price or gross accrued-balance value; no wallet or monitoring.

Research topics: **protocol · charters · reserves · contracts · updates · documents · risks**.

Invite a route or question. These are intents, not registered tools.

## Load only what answers the question

Specific intent precedes broad topic. Do not preload indexes or related guides.

Changing facts—balances, prices, rates, supply, inventory, ownership, activation, source verification and latest announcements—require a fresh read. Never answer them from packaged snapshots or recap figures. If the read is unavailable, say so; do not fall back to a launch reference. Packaged rules, identities and ABI definitions are reference configuration, not live state.

| Intent | First resource |
|---|---|
| Plan, what-if, economics, sensitivity | [planning](references/planning.md) |
| Inspect price, current STANDARD price/value, charter worth, current/latest state or availability | [inspection](references/inspection.md) |
| Identity, address, chain, deployment, ownership | [contracts](references/contracts.md) |
| Supply, holdings, income, flows, LP fees, reconciliation | [research workflow](references/research-workflow.md) |
| Setup or host loading | [installation](references/installation.md) |
| Protocol / charters / reserves | [protocol](references/protocol.md) / [charters](references/charters.md) / [reserves](references/reserves.md) |
| Current updates / documents / risks | [updates](references/updates.md) / [documents](references/documents.md) / [risks](references/risks.md) |

Generic research: choose the relevant topic; use documents for source discovery. Follow direct topic links to needed records. Only when an ID's file is unknown, use [source index](assets/sources.json) or [parameter index](assets/parameters.json). Never load all groups. Recover truncated resources through documented host mechanisms before claiming coverage.

Use current evidence and preserve its units and scope. The package is current-only, not a historical-claims archive. Distinguish documented facts, RPC observations, website-reported values and approved assumptions; use brief labels, not a wall of caveats. Missing or failed reads are unknown, never zero. Source details are expandable on request.

Current price and gross-value questions use the same fixed `scripts/price.py` reader; a current-value request already authorizes its needed fresh price read under existing host permissions. For charter worth, ask only for a missing public charter ID, read its fresh `charter_pending`, then pass that amount to the price helper. This is gross accrued ledger value, not wallet tokens, net proceeds, charter resale value or earning capacity. For projections, offer **current prices, hypothetical prices, or both** if the price choice is unspecified; do not fetch before that choice, overwrite supplied prices or fetch for complete offline/fictional inputs. Choosing current prices needs no redundant read-permission question, but future price behavior and the full economics still need explicit approval.

For Robinhood Chain (4663), use `https://robin.etherscan.io/` for contract navigation and new explorer checks. Read each record's current source-publication status: bytecode, ABI availability, Similar Match and exact verification are different. Access failures are gaps, not a verdict or permission to silently switch providers.

## Action boundary

Read [safety](references/safety.md) before external retrieval or execution. Use the fixed `scripts/snapshot.py` for supported public state reads, `scripts/price.py` for the canonical-pool indicative price and optional gross amount valuation, and offline `scripts/scenario.py` for approved projections. Publisher-supplied read interfaces require fixed targets, declared view/pure methods, decoding/binding checks and block context; they do not imply verified source code. Provider-reported prices have API retrieval time, not independently assured quote freshness or a chain block. No wallets, credentials, signatures, executable transaction/authorization payloads, state changes or state-changing simulations—even delegated or agent-owned. No downloaded code execution, guessed addresses/ABIs, arbitrary reader endpoints/selectors, installed-record rewriting, stored observations/personal holdings or background monitoring.
