# Risks and disclosure limits

Documented limitations, not vulnerability findings or an audit. Sources: [website core](../assets/sources/website-core.json) and [website context](../assets/sources/website-context.json).

## What the publisher disclaims — whitepaper §15

The publisher calls STANDARD experimental, says it is not a bank or regulated financial institution, holds no customer funds, offers no accounts, gives no investment advice and places participation at the user's risk. The About footer says “holds no deposits” rather than “holds no customer funds.” Those disclaimers coexist with protocol-held liquidity and bank-held reserves; do not confuse protocol asset ownership with a customer deposit or reserve-redemption entitlement. [sr-whitepaper: disclaimer; sr-disclaimer; sr-about; sr-app-about]

The whitepaper and both About forms explicitly call themselves **design overviews, not implementation specifications**. They say crucial safeguards are omitted, copying the document alone can cause loss, and only the official deployment is canonical. That notice is a publisher claim; it neither authenticates an address nor proves the claimed safeguards exist or work. [sr-whitepaper: opening notice; sr-about; sr-app-about]

## Concrete disclosure limits — §14 and related sections

The launch-parameter summary remains entirely redacted and says final parameters will be announced closer to launch. Some values are visible in earlier prose or tables. Retain each visible claim at its exact locator; do not erase it merely because the summary hides it, or treat it as verified final deployment configuration. Missing policy, exit-fee and auction settings remain null with `redacted` or `not-established` status. [sr-whitepaper: parameters, policy, branches, exits]

The overview does not supply authenticated deployment identities, full implementation rules, access-control permissions, audit evidence, reserve custody terms or live balances. The absence of those details in this reviewed material is not proof they do not exist elsewhere. See [contracts](contracts.md) before making identity or implementation claims.

## Locate the relevant uncertainty

- [Source conflicts](risk-conflicts.md): genesis/ongoing proceeds, issuance destination, autonomy/controls, ledger spending, dormancy arithmetic, launch timestamps and tax text/image tension.
- [Policy](protocol-policy.md), [auctions](auctions.md), [exits](exits.md), [reserves](reserves.md): mechanics and exact missing inputs. Values live in [monetary](../assets/parameters/monetary.json), [participation](../assets/parameters/participation.json), [reserves](../assets/parameters/reserves.json), [launch](../assets/parameters/launch.json).
- [Audit history](announcement-history.md): claims and missing reports, not security assurance.

## What economics alone cannot establish

License burning, branch retirement, fee redistribution, permanent liquidity and buybacks are described mechanisms, not a promise of returns, realizable exit prices, profitability, solvency, continuous withdrawal availability or safety from manipulation. The publisher's “rational move,” anti-run, anti-sniping and defense narratives require distinct implementation and outcome evidence; they are not adopted as established results. [sr-whitepaper: net-flow, policy, branches, exits, reserves, flywheels; sr-post-2098969974044066298]

Do not classify an unknown as a vulnerability, nor call a public-source review a security audit. Explain the documented mechanism, the exact missing evidence and the conclusion it prevents. Use [research workflow](research-workflow.md) for scoped public reads and [safety](safety.md) for action boundaries.
