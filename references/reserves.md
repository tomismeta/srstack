# Fees, reserves and defense

Publisher accounting, not observed holdings or deployed restrictions. Current source: [v1 sources](../assets/sources/website-v1.json), `sr-whitepaper-v1` §§3,6,11–12,15. Exact settings: [reserve parameters](../assets/parameters/reserves.json), [launch parameters](../assets/parameters/launch.json).

## Founding funding is not the ongoing fee split

Founding proceeds escrow until finalization and fund liquidity and protocol vaults, with no team share. The current publication does not specify the exact split. Genesis token liquidity is described in the currency section; do not substitute ongoing fee-allocation percentages for founding receipts. [sr-whitepaper-v1: currency, charters]


The founding allocation is separate from steady-state trading/charter-auction receipts. Do not use ongoing fee percentages for founding proceeds. [sr-whitepaper-v1: reserves]

## Ongoing ETH routing — §11

Current net flow selects the active vault: expansion when positive, contraction otherwise. Shares are `ongoing-active-vault-share`, `ongoing-pol-share`, `ongoing-team-share`. Of the POL allocation, `pol-swap-share` is swapped to STANDARD, paired with remaining ETH and added as permanent liquidity. §12 allows bounded owner changes to fee splits. [sr-whitepaper-v1: policy, reserves, immutables]

The published launch rule in `launch-trading-tax-curve` describes opening taxes decaying to the steady buy/sell floors. Read fresh tax getters rather than treating launch values as current fees; unavailable reads leave current fees unknown. The canonical pool's LP fee is separate; transaction-specific fee bases remain model assumptions. Protocol-position STANDARD fees are burned under the published design. [sr-whitepaper-v1: currency, reserves, parameters]

Outside liquidity opens after the launch schedule reaches its floors. The publisher says withdrawn ETH principal is taxed at the sell rate and STANDARD principal at the buy rate; accrued LP fees are untaxed. See `outside-liquidity-tax-policy`. This is a description, not an executable liquidity action. [sr-whitepaper-v1: reserves]

## Reserve assets and ownership

Expansion accumulates ETH and purchases tokenized gold and comparable assets. Reserves are protocol property and are not redeemable by charter holders. Sources do not authenticate reserve issuers, custody/redemption terms, balances, valuation policy or purchase venues. Reserve accumulation is neither evidence of holdings nor a fixed peg or guaranteed price floor. ExpansionVault reserve purchases remain owner-only even if the separate execution switch is opened. [sr-whitepaper-v1: reserves, immutables, disclaimer]

Genesis liquidity and subsequent POL additions are described as permanent/non-withdrawable. Those restrictions are not verified deployed permissions or a guarantee of ETH exit value. A banker withdrawing tokens is not withdrawing the protocol's LP position. [sr-whitepaper-v1: currency, reserves]

Authoritative ownership/authority records: `reserve-redemption-policy`, `pol-withdrawal-policy`, `expansion-reserve-purchase-policy`.

The publisher-linked ABIs contain successor holdings-migration entries for both vaults and FeeSplitter. Asset movement to a successor is distinct from changing deployed code; whitepaper non-upgradeability language is not a blanket proof that holdings can never move between components. The ABI alone establishes neither deployment correspondence nor who can move what, registry replacement rules or present authority. Keep these as implementation questions, not custody assurances or migration instructions. [sr-contract-directory; contracts](contracts.md)

## Contraction execution

Contraction buys STANDARD on-market and burns all purchases (`buyback-burn-share`). For vault balance V and pool reserves R, the published rule is:

spend_tick = min(a × V, b × R)

Here a = `buyback-vault-fraction`, b = `buyback-pool-fraction`, and cadence = `buyback-tick`. Commensurate denominations and the exact measurement of R still need implementation evidence. `buyback-daily-depth-bound` is an approximate source description, not a fixed daily budget. Unspent balance rolls forward and the vault is described as unable to sell. [sr-whitepaper-v1: reserves equation 11.1]

`buyback-spend-formula` stores this source-only formula; `vault-execution-enablement` separately records who may execute it.

Contraction-buyback/POL-pairing execution starts owner-cranked; the owner can make it permissionless through a one-way switch. Optional guardian pauses cover auctions and vault purchases, not withdrawals. Non-upgradeability does not imply autonomous execution or absent operational controls. [sr-whitepaper-v1: immutables]

## Accounting boundaries

Keep founding proceeds, ongoing auction receipts, LP fees, protocol taxes, accrued issuance, wallet mints, deposit conversions, ledger removals, redistribution, reserve holdings and buyback spend separate. A reserve purchase is not banker income; a deposit conversion is not a permanent burn; a documented allocation is not an observed transfer. [Contracts](contracts.md) routes identity provenance and fresh verification; [risks](risks.md) identifies evidence boundaries.

The official conditions page's Treasury & controls section reports native ETH vault balances and explicitly does not index reserve-token holdings. Its fee-routing direction is provisional until settlement and uses a different window from issuance policy. Neither a partial ETH display nor the combined “Burned forever” cap-reduction label proves a complete reserve portfolio or cumulative buyback spend. [sr-protocol-conditions; inspection](inspection.md#supply-restrictions-and-control-context)
