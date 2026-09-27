# Maintaining reviewed contract inventories

This is the maintainer contract for every future contract, generation or interface addition. It governs what the package claims, not which contracts an agent may investigate. Ordinary research can use newly authenticated evidence without modifying the skill or matching its inventory.

## Three layers, three independent evidence claims

1. **Contract identity:** chain, economic role, generation, dated publisher bindings, dependencies and creation/cutover evidence where established. An address is a dated lead, not an active router. Distinguish shared infrastructure from project-authored contracts, and role replacement from code upgrades.
2. **Reviewed interface:** every entry in a specifically identified reviewed ABI, including overloads, tuple components, constructors, events, errors and fallback/receive entries where present. Completeness is relative to that interface, not the universe of deployed capabilities.
3. **Question capability:** what that interface can directly answer, what it does not expose, what remains unknown, and the alternative evidence needed. A callable function, authenticated semantics and deployed implementation correspondence are separate claims.

The [contract inventory](contracts.md), [interface index](interface-inventory.md), [capability guide](capabilities.md) and [shared review records](../assets/interfaces/reviews.json) implement these layers. Read only the part relevant to the question.

## Add or refresh a contract

- Find original publisher/deployment evidence and record its explicit page-to-source chain. Retrieve complete relevant source/ABI data when possible; do not execute downloaded JavaScript or treat a similarly named contract as correspondence. Partial retrieval means partial coverage, not a complete interface.
- Assign stable role/generation/interface identities. Preserve historical generations needed for history. Record unknown deployment or activation facts as unknown; never infer activation merely from a directory or successful call. Token identities and decimals still need deployment-specific authentication.
- Create a shared immutable review record containing review date, source IDs/URLs, exact source/literal or adaptation locators, hashing convention, fingerprints, coverage and limitations. Each interface entry references its review ID and generation context. A new source or changed interface gets a new review identity; never silently rewrite an old review as if it observed newer bytes. When retaining an earlier review, give the revised interface its own stable revision ID/file and dated binding record, then point applicable capability rows at the new review; do not reassign the old review's interface ID to newer bytes. Reuse unchanged historical evidence with its original date rather than pretending to have refreshed it.
- Extract ABI data without evaluating source expressions. Where the publisher explicitly adapts an earlier ABI, account for every removal and addition as data and document the transformation. Preserve input order/names/types, output order/names/types, state mutability, tuple components, event anonymity and every `indexed` flag. Canonical signatures do not encode indexing, so a signature alone is insufficient to decode logs.
- Inventory every entry in the reviewed interface, not just familiar getters. Explain its specific purpose, relevant units, state/time scope and limitations. Mark name/ABI-derived interpretation as such; do not invent privileged callers, accumulator scales, opaque registry keys, refund behavior or Solidity rounding. Shared units or administrative notes may be referenced rather than copied across entries.
- Bind the interface to dated contract/generation evidence. An ABI fingerprint authenticates the reviewed artifact, not current deployed code. Keep publisher attribution, observed code, source/compiler correspondence, permissions and economic semantics independently qualified.
- Update the capability map and its provenance. Use **available**, **not exposed in the reviewed interface**, or **unknown**. Positive rows cite actual signatures; negative rows cite complete reviewed scope and exact absent candidates where applicable. A partial ABI cannot justify a negative capability claim. Distinguish no day-parameter history getter from an existing getter usable at a historical block through an archive provider.
- Update affected explanations, units, indexed-field examples and history/cutover guidance. Never merge charter and branch-license semantics because some signatures coincide. Keep the short skill entrypoint as a pointer, not a duplicated function catalog.

## Freshness and contradictions

An interface-review date is not a current-state timestamp or a promise that the publisher will not change. Revisit affected bindings/reviews when the publisher changes an interface or generation, source/literal fingerprints differ, observed calls/log layouts conflict with the recorded ABI, or independently authenticated deployment evidence contradicts the stored lead. A failed call alone does not identify the cause: wrong block/generation, permissions, provider capability and true interface drift need distinction.

Retain conflicting evidence with scope; do not make a newly successful decode silently resolve identity or semantics. Unknown capabilities remain open research questions, not a denylist. For canonicality and incremental observation reuse, follow [history guidance](auction-history.md), which is separate from interface freshness.

## Verification and publication

From the reviewed source checkout, run the inventory consistency checks together with package and research regressions. Consistency must cover review/source references, exact ABI/signature/layout relationships, overload identity, interface counts/fingerprints, contract-to-interface coverage, and positive/negative capability references. Checks can detect inconsistent inventory claims; they cannot independently certify publisher truth or implementation correspondence.

Exercise the changed resource from a standalone exported skill: locate the relevant role, resolve its review and an actual function/event, and use the documented example without access to source-only fixtures. New or changed decoding semantics need a behavior regression; do not pin incidental wording. Keep maintenance code, regression machinery and private/live evidence outside the runtime. The explicitly fictional installed worked example is instructional data, not a live dataset or calculation default.

After review and observed verification, update revision evidence and rebuild the integrity manifest. Export the pinned commit, verify exact membership/bytes, and publish without overlaying retired runtime resources. Missing review provenance, incomplete interface enumeration labelled complete, or unqualified negative claims are publication failures—not reasons to restrict an agent's independent research.
