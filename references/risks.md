# Risks and disclosure limits

Documented limits, not vulnerability findings or an audit. Current publisher source: [v1 sources](../assets/sources/website-v1.json), `sr-whitepaper-v1`. Earlier notices and presentations remain separately dated in [website core](../assets/sources/website-core.json) and [website context](../assets/sources/website-context.json).

## Publisher disclaimer — §16

STANDARD is described as experimental, not a bank or regulated financial institution, with no customer funds/accounts and no investment advice. Reserves are protocol property and not redeemable (`reserve-redemption-policy`). About's earlier “holds no deposits” wording must not be confused with the current token-to-ledger deposit-conversion mechanism: conversion does not create a reserve-redemption entitlement. [sr-whitepaper-v1: currency, disclaimer; sr-disclaimer; sr-about; sr-app-about]

Earlier whitepaper/About notices call their material design overviews rather than implementation specifications and warn that omitted safeguards matter. Preserve those notices with their dated sources; the current frozen section text is not an authenticated implementation specification either. Neither canonical-site rhetoric, a code line count nor published addresses establishes deployed-bytecode correspondence. [sr-whitepaper: opening notice; sr-about; sr-app-about]

## Non-upgradeable does not mean uncontrolled — §12

The whitepaper claims no proxies or code-migration mechanism (`protocol-upgrade-policy`). It separately describes substantial owner discretion:

- **Fixed constraints:** cap, base-rate ceiling with downward-only ratchet, multiplier rule, resolution curve, revocation fee, manual-tax ceiling, precommitted launch-tax schedule, vault execution bounds and founding price/curve constraints.
- **Bounded tuning:** epoch length, taxes, daily license/charter counts, fee splits, auction floors/windows/decay half-lives. Exact bounds live in `epoch-length-minimum`, `epoch-length-maximum`, `owner-manual-tax-ceiling`, `licenses-per-day-owner-ceiling`, `charters-per-day-owner-ceiling`, `ongoing-team-share-owner-ceiling` and `auction-owner-controls`. The whitelist window freezes when the sale opens (`founding-whitelist-window-control`).
- **Owner identity and process:** the source says production deployment initially assigns sole ownership to the broadcast sender/deployer, with no protocol-enforced delay, notice period, threshold or cancellation window. A later manual Ownable2Step transfer of selected contracts to a Safe/multisig is possible, but no recipient is deployed/configured/assigned by production launch (`owner-control-policy`). This describes launch setup, not verified current owner state.
- **One-way switches:** charter transferability and permissionless contraction-buyback/POL-pairing execution may be enabled permanently (`transfer-enablement`, `vault-execution-enablement`). Expansion reserve purchases remain owner-only (`expansion-reserve-purchase-policy`).

An **optional**, not necessarily configured, guardian can pause auctions and vault purchases only. It cannot pause withdrawals, touch funds or change parameters; the owner can disable or permanently renounce it (`guardian-powers`). Do not infer that withdrawals cannot revert: §9 expressly retains independent settlement dependencies. [sr-whitepaper-v1: exits, immutables]

## Published facts and remaining limits

The current whitepaper has sixteen sections, including new **Immutables**, and its launch summary is now visible. Policy bounds/recurrence, exit pressure/fee formula, license floor, founding split and owner controls are no longer “still redacted.” Exact parameter records carry current facts, dated prior values and explicit limits. [sr-whitepaper-v1: policy, branches, exits, reserves, immutables, parameters]

Two current contradictions prevent an executable source-only interpretation: §12 launch taxes open 90%/90%, versus §15's 20%/40%; and §7's geometric-to-floor auction equation differs from §§7–8's four-hour gap-halving prose. Steady taxes agree at 2%/3%. Preserve conflicts rather than choosing a preferred formula or claiming code resolves them. [Source conflicts](risk-conflicts.md)

The separately added deployment directory and protocol conditions remain publisher evidence, not source-code/ABI verification. Authenticated implementation, permissions, audit correspondence, reserve custody and live balances remain distinct evidence requirements. [Contracts](contracts.md) and [inspection](inspection.md) retain those boundaries. [sr-contract-directory; sr-protocol-conditions]

## What economics alone cannot establish

Burning, retirement, redistribution, permanent liquidity and buybacks are not promises of returns, realizable exit prices, solvency, continuous settlement or manipulation resistance. Published recurrence is not a future multiplier forecast. Numerical scenario output remains **Hypothetical—not contract-verified or a forecast.**

Use [policy](protocol-policy.md), [auctions](auctions.md), [exits](exits.md), [reserves](reserves.md) and the [parameter catalog](../assets/parameters.json) for topic-specific facts. [Audit history](announcement-history.md) records claims, not security assurance. Do not classify missing evidence as a vulnerability or call this public-source review an audit.
