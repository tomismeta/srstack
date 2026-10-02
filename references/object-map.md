# Objects, contracts and relationships

A conceptual map, not a current deployment router, complete ABI or verified implementation. Definitions below summarize the dated [published protocol](protocol.md), [charter lifecycle](charters.md), [reserve routing](reserves.md) and [announcements](updates.md). Authenticate a relationship's implementation, generation and block before using it as an executable rule. [Discover the relevant deployment](contracts.md#discover-a-role-without-prior-session-context); then select the matching [interface](interface-guide.md).

## Economic objects are not contract instances

| Object | Definition and relationship | Do not confuse it with |
| --- | --- | --- |
| Public address / participant | An address may own charter NFTs and hold wallet tokens. Current ownership is a block-scoped fact; historical ownership and earning attribution require history. | The administrator of CentralBank or an auction; a legal bank account. |
| Charter | A protocol participation position represented by an NFT. Its holder, branch count and ledger are related records, not interchangeable balances. Published lifecycle and transfer conditions are scoped in [charters](charters.md). | A branch, an auction order, redeemable reserve ownership or company equity. |
| Branch | A counted unit of charter earning capacity under the published issuance model. CentralBank exposes counts per charter and globally. | A separately enumerated NFT/contract, unsold license inventory or a fixed daily income promise. |
| Expansion license | The purchase that opens additional branches for an existing charter under the applicable generation's rules. | Acquisition of a new charter, an ERC20 approval or proof of a separately transferable license token. |
| Pending ledger credit | CentralBank's reported whole-charter pending amount; stored checkpoint fields and computed pending can differ. | Wallet STANDARD, verified unspent earnings, immediate spendability or net withdrawal proceeds. |
| STANDARD | The fungible token. Wallet balances, supply, permanent burns and ledger conversions are separate accounting dimensions. | ETH, a branch, a reserve-redemption claim or automatic entitlement to protocol income. |
| Bid / limit order | Purchase intent recorded by the applicable license-auction interface: bidder, quantity and limit price. An observed order is not a purchase or guaranteed fill. | Auction inventory, the current ask, a receipt execution or an authenticated charter ID merely because a raw page ID fits a getter. |
| Auction round | A family-, chain-, emitter- and generation-qualified round. Scheduled boundaries, actual materialization and sale times are separate. | A human calendar day or the charter's allowance window. |
| Allowance window | The interval over which the applicable license-purchase limit is consumed/reset; alignment and prior usage require evidence. | ERC20 allowance, auction round, rolling 24-hour horizon or a replenishment of funds. |
| Issuance epoch | A policy/accrual interval with associated settings and settlement state. Active and queued settings differ. | An auction round or proof that today's rate continues through its boundary. |
| Reserve asset / LP position | Protocol-held property or liquidity exposure; identity, custody, holdings and rights need their own evidence. | A charter holder's redeemable assets or proof that an illustrative website portfolio exists. |
| S-Bill | A STANDARD deposit position recorded by the separately deployed `sbills` role, with principal, booked premium, stored maturity and settlement state. Identity is `(chain, contract, bill ID)`; ID zero is valid. | A charter, branch, wallet balance, sample UI bill or guaranteed yield. See [S-Bills](sbills.md); no NFT or transferability inference. |

## Ownership and record relationships

```text
Public address
  owns → charter NFT (CharterNFT records the holder)
    identified by → charter ID
    associated with → branch count (CentralBank record)
    associated with → pending/checkpoint ledger (CentralBank records)
  holds → wallet STANDARD (STANDARD token record)

Charter auction
  acquires/creates → new charter
  reports consideration in → ETH
  emits → CharterPurchased

Branch-license auction
  expands → existing charter's branch count
  reports consideration in → STANDARD ledger denomination
  emits → LicensesPurchased
  may record → bids (generation-specific)
```

These arrows identify different relationships, not legal ownership of every connected object. A charter owner does not thereby administer the bank, own its reserves or control its auctions. A charter transfer does not by itself establish who earned the transferred ledger balance. New-charter ETH funding and branch-expansion ledger funding require separate accounting; conversion between them cannot be assumed.

## Contract roles and dependencies

| Role | What it records or does in the reviewed design | Relationship to authenticate |
| --- | --- | --- |
| CentralBank | Charter branch counts, pending/checkpoint state and monetary-policy/accrual interfaces. | Its CharterNFT, STANDARD and registry references; action authorization and exact accrual/ledger implementation separately. |
| CharterNFT | Charter token identity, holder and transfer-related state. | Its CentralBank reference; `ownerOf(charterId)` is position ownership, not module `owner()`. |
| STANDARD token | Fungible balances/allowances, supply and restriction interfaces. | Bank/hook/registry dependencies where relevant; token transfers are not ledger movements by definition. |
| AddressRegistry | Role-to-address configuration used by the deployed system. | Exact key meaning, consumers and block-scoped binding; historical `AddressSet` is not perpetual routing or proof every module consults it. |
| GenesisMinter | Publisher-listed founding-entry component, distinct from ongoing charter auctions. | Founding eligibility, escrow, finalization and common accrual start under [genesis](genesis.md); founding terms are not a current ongoing offer. |
| Charter auction | New-charter acquisition and ETH-denominated purchase events. | Its bank, generation, own schedule/inventory/price and payment/refund path. Original and v1.2 identities are distinct; no separate v1.1 charter replacement is established by the reviewed mapping. |
| Branch-license auction | Expansion purchases and, for the reviewed v1.2 interface, order views/events. | Its bank and current authorization, generation, STANDARD-ledger payment path, capacity and allowance rules. Original, v1.1 and v1.2 identities must remain distinct in history. |
| Trading / TaxHook | Hooked pool trading conditions, taxes and flow-related interfaces. | Actual pool/hook binding, enabled versus active restrictions, current versus scheduled rates, and bank/fee-routing dependencies. |
| PoolManager / pool | Shared Uniswap infrastructure manages pools; a particular pool is separately identified by its full key/ID. | Chain, currencies, fee, tick spacing and hook as applicable. A manager address alone does not identify the STANDARD pool or make the infrastructure project-authored. |
| Multicall3 | Publisher-listed shared call-aggregation infrastructure, not an economic position or project ownership registry. | Deployment/interface and individual subcall results if used; aggregation does not authenticate targets, make failed reads zero or authorize writes. |
| FeeSplitter | Published routing of ongoing ETH flows to designated destinations. | Effective recipients/shares, active versus queued configuration, liabilities and actual transfers. Founding proceeds have separate routing. |
| Expansion Vault | Published accumulation of ETH and reserve-asset purchases. | Assets, custody, execution authority and holdings; protocol property is not holder redemption entitlement. |
| Contraction Vault | Published market buybacks followed by burns. | Acquisition, actual burn accounting, execution limits and controls. Do not count tokens retained elsewhere as burns. |
| Genesis Liquidity Manager | Historical founding liquidity management and continuing fee collection described by the publisher. | Actual positions, custody and current responsibilities; an old frontend `polManager` label is not today's registry destination. |
| POL Buyback | Announced incremental market purchases directed to the Incentives Vault. | Current route, purchase execution and receiving vault; not the Contraction Vault's buyback-and-burn path. |
| Incentives Vault | Holds acquired tokens for the announced incentive purpose. | Holdings, permissions and actual distribution terms; retained tokens are neither burned nor automatically owed to token/charter holders. |
| S-Bills | Deposit bills, rate/amount quotes, premium budget and exit/redemption/roll interfaces. | STANDARD token, deployment/generation, bill owner and stored terms; funding transfers and administrative powers need separate evidence. See [S-Bills](sbills.md). |
| Administrator / guardian / Safe dependencies | Control relationships, not economic participation positions. Reviewed administrative infrastructure includes Safe dependencies; scope varies by module. | Accepted versus pending owner, guardian powers, supply controllers and relevant Safe configuration. An administrative proxy does not prove every monetary module is upgradeable. |

Published fee-flow relationships are described in [reserves](reserves.md); their percentages and destinations must not be copied into current execution accounting without evidence. Asset migration, role replacement and code upgrade are different operations. An ABI name proves neither permission nor successful migration.

## Identities and generations

Preserve the domain of every identifier: chain ID, address, charter ID, raw order-page ID, round ID, allowance-window index, epoch number, token ID and pool ID are not interchangeable. Identical integer values or successful decodes do not establish a join.

For historical questions retain `(chain, role/family, generation, address, object ID)` as applicable. A replacement auction does not create a new CentralBank or migrate every object by implication. Distinguish deployment, activation, registry cutover and observed last activity. An old generation remains in the discovery scope until the requested evidence justifies excluding its activity.

## Evidence status and freshness

Use claim-level labels: **published design**, **developer proposal**, **official announcement**, **publisher interface/deployment attribution**, **observed onchain relationship**, or **implementation-established behavior**. These are not interchangeable stages, and a later post does not automatically outrank deployed evidence for a current-state question.

[Updates](updates.md) and the [source index](../assets/sources.json) retain review dates, conflicts and coverage limits. The map does not certify that every website paragraph, tweet, contract or product has been freshly reviewed. Do not invent modules for an announced strategy such as the Second Mandate, or assume a product is deployed because a preview has buttons or sample positions.
