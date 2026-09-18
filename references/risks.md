# Risks and disclosure limits

Documented limits, not vulnerability findings or an audit. Current publisher source: [v1 sources](../assets/sources/website-v1.json), `sr-whitepaper-v1`.

## Publisher disclaimer — §16

STANDARD is described as experimental, not a bank or regulated financial institution, with no customer funds/accounts and no investment advice. Reserves are protocol property and not redeemable (`reserve-redemption-policy`). Token-to-ledger deposit conversion does not create a reserve-redemption entitlement. [sr-whitepaper-v1: currency, disclaimer]

The whitepaper warns that implementation safeguards are absent from its overview. Neither publisher text, a code line count nor published addresses establishes deployed-bytecode correspondence. [sr-whitepaper-v1]

## Non-upgradeable does not mean uncontrolled — §12

The whitepaper claims no proxies or code-migration mechanism (`protocol-upgrade-policy`). It separately describes substantial owner discretion:

- **Fixed constraints:** cap, base-rate ceiling with downward-only ratchet, multiplier rule, resolution curve, revocation fee, manual-tax ceiling, precommitted launch-tax schedule, vault execution bounds and founding price/curve constraints.
- **Bounded tuning:** epoch length, taxes, daily license/charter counts, fee splits, auction floors/windows/decay half-lives. Exact bounds live in `epoch-length-minimum`, `epoch-length-maximum`, `owner-manual-tax-ceiling`, `licenses-per-day-owner-ceiling`, `charters-per-day-owner-ceiling`, `ongoing-team-share-owner-ceiling` and `auction-owner-controls`. The whitelist window freezes when the sale opens (`founding-whitelist-window-control`).
- **Owner identity and process:** `owner-control-policy` describes the publisher's ownership setup and manual Ownable2Step transfer path, with no protocol-enforced delay, notice period, threshold or cancellation window. Determine current owners and any Safe/multisig configuration freshly; the launch description is not an owner-state answer.
- **One-way switches:** charter transferability and permissionless contraction-buyback/POL-pairing execution may be enabled permanently (`transfer-enablement`, `vault-execution-enablement`). Expansion reserve purchases remain owner-only (`expansion-reserve-purchase-policy`).

An **optional**, not necessarily configured, guardian can pause auctions and vault purchases only. It cannot pause withdrawals, touch funds or change parameters; the owner can disable or permanently renounce it (`guardian-powers`). Do not infer that withdrawals cannot revert: §9 expressly retains independent settlement dependencies. [sr-whitepaper-v1: exits, immutables]

The current publisher-linked ABIs expose `migrateToSuccessor` and `HoldingsMigrated` for ContractionVault, ExpansionVault and FeeSplitter, and `supplyController`/`setSupplyController` for both auctions. Asset migration is not necessarily code replacement: immutable code can coexist with successor holdings transfers or replaceable registry bindings. This qualifies the scope of the whitepaper's no-code-migration wording; it does not prove the wording false or establish those modules' deployed correspondence, migration authority, controller powers or current configuration. Keep those implementation hypotheses separate until independently evidenced. No migration or setter action is authorized. [sr-contract-directory: publisher-linked app ABI; contracts](contracts.md)

## Published facts and remaining limits

The current whitepaper has sixteen sections. Policy bounds, withdrawal-fee envelope, license-floor reference, founding terms and owner controls are in the [parameter catalog](../assets/parameters.json). Exact founding allocation is not specified by the current document.

The launch tax schedule is a published reference rule; read current settings freshly through the publisher ABI. If reads are unavailable, current settings remain unknown—not launch defaults. Future taxes, exact auction execution and transaction-specific amounts remain assumptions unless separately established. Do not turn an unavailable auction into a zero-cost quote.

The directory identifies the targets; the fixed reader supports block-scoped observations with explicit bindings and decoding. Source equivalence, complete permissions, audit correspondence and reserve custody are separate questions. Mention only the limitation material to the answer; details remain in [contracts](contracts.md) and [inspection](inspection.md). [sr-contract-directory; sr-publisher-read-interface]

## What economics alone cannot establish

Burning, retirement, redistribution, permanent liquidity and buybacks are not promises of returns, realizable exit prices, solvency, continuous settlement or manipulation resistance. Published recurrence is not a future multiplier forecast. Numerical scenario output remains **Hypothetical—not contract-verified or a forecast.**

Use [policy](protocol-policy.md), [auctions](auctions.md), [exits](exits.md), [reserves](reserves.md) and the [parameter catalog](../assets/parameters.json) for topic-specific facts. Do not classify missing evidence as a vulnerability or call this public-source review an audit.
