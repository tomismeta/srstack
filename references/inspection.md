# Inspect: bounded public snapshots

An intent within srstack, not an installed command, RPC adapter or live backend. Answer the requested public metric at an identified boundary. Read [safety](safety.md) before external requests; load [contracts](contracts.md) for identity gaps and [research workflow](research-workflow.md) for historical discovery, quantitative accounting or reconciliation—not every reference by default.

Use only existing permitted public readers, clean unauthenticated browser rendering when needed, explorers/APIs and read-only chain facilities. The procedures below do not supply providers, archive support, price feeds or enumeration APIs. No installation, credentials, wallet access, source-code execution, transaction preparation, state-changing simulation or tracing workaround. Public addresses do not authorize discovery of private account data or other user addresses. No background watchers, schedules or alerts; later inspection needs a new bounded request. Missing capabilities produce a gap report, not a fabricated adapter/result or broader access.

## 1. Scope only the requested observation

Establish entity/generation, network/environment, full public target and any charter identifier/ownership or beneficiary relationship; metric and exact unit; current snapshot or bounded historical interval/block; coverage (one charter is not every owner position); and valuation/quote asset if requested. Ask only for user-dependent scope absent from evidence.

Wallet tokens differ from issuance credits; charter counts differ from branch counts. Topic-linked source records describe packaged evidence, not current chain state. Use [source index](../assets/sources.json) only to locate an unknown source ID; [parameter index](../assets/parameters.json) only to locate a documented design parameter. No example-derived identity or economics. Current requests warrant fresh bounded reads, not rewritten catalogs or automatic source refresh outside scope.

## 2. Authenticate before ABI reads

The [entity index](../assets/entity-index.json) routes 14 publisher-listed Robinhood addresses, all with Etherscan-displayed bytecode. Read each record's source-publication status and shared limits: the 12 protocol modules and Pool Manager lack published source/ABI; Multicall has Similar Match source/ABI. Neither publisher attribution nor a similar match establishes exact code correspondence, ownership or activation. Use the recorded Robinhood Etherscan links; failures remain gaps. Shared infrastructure and user-supplied addresses are not interchangeable protocol identities.

1. Establish original publisher attribution, chain/environment, generation and role, retaining URLs and publication/retrieval times.
2. Through permitted RPC, use `eth_chainId` and `eth_getBlockByNumber`; record number, hash, timestamp and UTC retrieval. An old cached block is not current; do not assume finality.
3. Check `eth_getCode` at that address/block. Establish source/bytecode correspondence and relevant ABI/version, proxy and implementation through evidence. Code presence does not establish role, activation, safety or authorship.
4. Bind charter ID and ownership/beneficiary relationship through authenticated registries, factories, interfaces or events. Authenticate each discovered target before ABI reads; permitted reads may establish relationships, but do not claim them prematurely.
5. Stop affected conclusions if attribution, chain, role, relationship, ABI or implementation remains unknown. Never guess addresses, selectors, slots, events or methods.

Report attribution, code correspondence, activation, ownership and audit scope independently, not one `verified` flag. A deployment lead/code observation is not necessarily an authenticated charter balance.

## 3. Read the scoped state

Use authenticated ABI `view`/`pure` `eth_call` at the identified block; wrappers and all nested/batched members must qualify. No mutating call merely because it will not broadcast; planner fields do not establish an ABI.

Bound addresses/topics, pages, resources, intervals, batches and retries. Discover through authenticated relationships; known positions are not a census. Historical `eth_getLogs` needs demonstrated coverage; current access proves neither history nor archive capability. Pin compatible reads to a common block, document exceptions and handle reorganizations per research workflow.

Retain raw values, authenticated decimals, units, derivations and anchors. Unknown semantics/scales block normalized quantities. Failed reads, redactions, missing history, unsupported methods, empty provider responses and incomplete enumeration are not zero. Displayed estimates remain attributed estimates. Balance changes are not income without flow accounting.

Collect only useful fields: possibly charter ID, owner/beneficiary, branches, issuance credits and evidenced lifecycle state. External branches/global budget need separately authenticated observations/accounting; do not assume planner fields exist on chain. Partial reserve holdings are not a portfolio total or solvency finding.

## 4. Anchor any price separately

Record exact base/quote identities and units, venue/provider/methodology, indicative/aggregated/executable status, quote/source and retrieval times, block if available, and requested amount/conditions if relevant. State and price freshness are independent. Report staleness, missing markets, incompatible anchors and coverage.

No invented markets, unrelated-token quotes, unqualified stablecoin=USD assumptions or liquidity guarantees. A quote neither authorizes a transaction nor guarantees proceeds. Without authenticated suitably fresh pricing, report token quantities without unsupported ETH valuation.

## 5. Report observations and gaps

Report **answer/classification; scope/units/ownership; identity evidence and unresolved links; requested/observed chain ID and block number/hash/time plus provider and UTC retrieval; raw values/scales and justified normalized derivations; independent price anchor/freshness; bounded coverage/failures/conflicts; original source URLs/IDs and locators**. Distinguish direct observation, publisher claim, derived quantity and unknown per field—not a blanket hypothetical label because fields are missing.

No authenticated contracts or permitted chain tools means an identity/capability-gap report, not a live-position result. Narrow success does not establish launch, security, solvency, complete activity or future issuance. Searches/failures cannot establish zero activity or universal absence.

## 6. Explicit planning handoff only

A request for research does not silently authorize inspection or planning; none authorizes persistence or financial action. If planning is requested, follow [planning](planning.md), schema 1 and explicit `documented`/`stress` mode. **The combined answer must start with the exact SKILL planning warning**, including blocked, missing-input and unavailable-runtime handoffs; JSON/link/footer is insufficient. Independently supported observations remain labeled observations.

The engine accepts economics, not addresses, ABI, wallet data, provenance objects or paths. Keep the observation-to-assumption mapping outside strict JSON: source, units, chain/block or quote time, retrieval and limits; confirm user approval of imported initial conditions. Future multipliers, flat prices/growth, issuance availability, license costs, gas, fees/taxes/slippage and funding feasibility require explicit assumptions. Never turn one observation into future flatness, a design parameter into live economics or fictional example into defaults.

Mode differs from exit mode. Documented conflicts block numbers; stress requires explicit choice and retains conflicts, computational bounds and valid fixed rules. Show fresh selected-detail conformance/evidence and unresolved semantics, using [conformance](planning-conformance.md) only if interpretation requires it. Cap matches do not authenticate positions; frontend ranges do not prove on-chain policy. `summary` defaults; full accounting/history are opt-in, with history requiring full. Engine acceptance confers no freshness or authenticity. Report execution/errors per workflow, not missing output as zero. No saving, overwrite, source refresh, monitoring or financial action is implied.
