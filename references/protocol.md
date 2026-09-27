# Protocol: system and routing

Apply the [preparation and wallet boundary](safety.md#preparation-and-wallet-boundary).

Publisher rules and selected v1.1/v1.2 announcements reconciled on **2026-09-27**, not independently verified implementation or live configuration. Whitepaper: `sr-whitepaper-v1`; scoped changes: `sr-protocol-v1-1-announcement` and `sr-protocol-v1-2-announcement`. Provenance: [source index](../assets/sources.json); [bounded coverage and timeline gaps](updates.md#september-27-bounded-reconciliation).

## System and ownership — whitepaper §§1–2

STANDARD describes an ERC-20 currency, an ETH ↔ $STANDARD hooked Uniswap v4 pool, an issuing central bank, charter NFTs, branches within those charters, and expansion/contraction vaults. Traders need no charter. A branch represents a share of issuance, not a reserve-redemption claim. The protocol owns liquidity and reserve assets; the bank/company analogy is not a legal bank account or customer deposit product. [sr-whitepaper-v1: introduction, entities, disclaimer]

The [object and contract map](object-map.md) separates economic objects from contracts and distinguishes ownership, ledger records, funding and control relationships. An NFT ID, branch count, wallet token balance, pending ledger amount, auction bid and S-Bill preview are not interchangeable forms of ownership or income.

Trading generates fees and pool-flow measurements; issuance credits branch balances pro rata; retiring branches releases accrued value through withdrawal minting. The whitepaper describes expansion-license payments as permanent ledger removal; that reference is not a verified v1.1 proceeds split. Token deposits convert wallet tokens into re-mintable ledger value. Post-genesis charter auction ETH enters the ongoing fee engine; founding proceeds have a separate allocation and escrow/finalization sequence. [sr-whitepaper-v1: entities, currency, charters, reserves]

The official [Second Mandate](updates.md#second-mandate-liquidity-for-tokenized-stocks) adds an announced direction: an open liquidity engine for tokenized stocks, not another stock issuer. Creating or approving markets, seeding liquidity and recycling trading fees into the Reserve is a stated strategy, not a replacement for the documented monetary mechanics below or evidence of their implementation. [sr-second-mandate-announcement; sr-second-mandate-manifesto]

The historical [v1.1 update](updates.md#protocol-v11-announced-changes) announced 12-hour license rounds of 50 branches, three per charter per 24-hour cap window, a two-hour license-auction half-life, and bid-side-only POL sending acquisitions to the Incentives Vault. **50 is not the current v1.2 allocation:** fresh per-round supply, cap and remaining-inventory getters govern current answers. These historical published references never override live settings; the earlier proposed 50/50 branch-payment split is not confirmed. POL Buyback and Incentives Vault do not replace Contraction Vault burn accounting or automatically change charter schedules.

The later [v1.2 update](updates.md#protocol-v12-announced-changes) announced branch limit orders with FCFS best-attempt keeper execution and charter auctions at branch cadence. Its initial 5.5 ETH opening and subsequent 3× clearing-price rule are dated policy, not current prices or guaranteed fills. Authenticate current deployments; retain earlier generations for historical scope. This auction release and its review claim establish neither S-Bill launch nor completed S-Bill audit.

## Read only the needed mechanics

- [Supply and policy](protocol-policy.md): supply identities, deposit conversions, flow signals, published multiplier recurrence and conditional models; [monetary parameters](../assets/parameters/monetary.json).
- [Charters](charters.md): branches, founding entry, auctions, exits and dormancy; [participation parameters](../assets/parameters/participation.json).
- [Reserves](reserves.md): separate founding/ongoing allocations, ownership and buybacks; [reserve parameters](../assets/parameters/reserves.json).
- [Launch trading](launch-trading.md): finalization, tax gaps and activation; [launch parameters](../assets/parameters/launch.json).
- [Risks](risks.md): non-upgradeability does not eliminate owner discretion or the optional guardian.

## Publisher's feedback-loop thesis — §14

- **Adoption:** charter purchases fund reserves, liquidity and buybacks; additional branches change allocation rather than independently increasing the daily issuance budget.
- **Expansion:** the whitepaper argues for permanent license-payment removal while increasing the purchaser's future issuance share; the actual v1.1 payment split is not established by that thesis.
- **Fee flow:** either trading direction generates fees; the current regime directs the active vault toward reserves or buybacks.
- **Policy:** outflow is described as combining issuance cuts, buybacks and crowd-priced resolution fees that burn and redistribute value.

These are the publisher's incentive arguments, not guaranteed rational behavior, profitability, price support or bank-run prevention. [sr-whitepaper-v1: flywheels]

## Presentation is not state

Use host public-read tools and authenticated current deployments/interfaces for requested state. Auction rounds and charter cap windows differ; stored “today” counters may lag rollover and are not calendar recaps. Failed reads leave fields unknown, never filled from historical snapshots or published defaults. Source rules remain useful as attributed policy or explicitly labelled scenarios, not hardcoded live economics.

See [documents](documents.md) for all sixteen current sections and [risks](risks.md) for remaining evidence gaps.
