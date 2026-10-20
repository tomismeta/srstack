# Launchpad tokens, curves and creator controls

A launchpad token is a factory-created third-party token with its own curve, pair asset and eventual pool; it is not STANDARD, a charter, a stock claim or a protocol endorsement. The October 19, 2026 review establishes publisher descriptions and dated deployment relationships, not a certificate of every token's implementation or safety. Use [contract authentication](contracts.md), [public-read inspection](inspection.md) and the existing [wallet/preparation boundary](safety.md#preparation-and-wallet-boundary); no connection or transaction is needed to explain these objects.

## Identify the token generation

The [current publisher guide](https://www.standardreserve.xyz/docs/launchpad/) explicitly says the two launchpads coexist and the app displays both together. A token keeps the generation that launched it; a new UI or factory does not migrate old tokens.

| Published distinction | Earlier `launch-2026-10-14` | New `urc5-2026-10-19` |
| --- | --- | --- |
| Pair assets | Listed stocks | Listed stocks or ETH, with WETH held by curve/pool |
| Transfers before graduation | Locked | Ordinary transfers allowed; curve/venue restrictions still apply |
| Creator extra fee | 0–5%, selected and fixed at launch | Graduated-pool hook module determines extra fee |
| Other pools | No own-pool restriction described | Optional own-pool-only policy chosen permanently at launch |
| Charter reservation | Up to 10% of token supply, per-branch payout | Up to 80% of token supply, per-branch or complete-exit payout |

**The earlier creator extra fee is not its entire trading fee.** Any separately evidenced base trading fee and creator share of that base fee are distinct. Do not import the new guide's 1% base fee or its split into the earlier generation without generation-specific evidence.

Identify a token by `(chain, factory, token, curve)` and authenticated factory-child/dependency relationships, not ticker, apparent age or the latest factory address. Resolve both generations through the [launchpad interface inventory](interface-inventory-launchpad.md). A curve implementation address is not an individual token's curve; a shared PoolManager is not its graduated pool. User-submitted names and ticker collisions do not make a token an official Reserve asset.

Use this question table with the [capability planning map](capabilities.md#planning-map), not as a required read order. Exact signatures, layouts and coverage belong in the [family inventory](interface-inventory-launchpad.md).

| Question | Capability and minimum relevant evidence |
| --- | --- |
| Which launchpad and stage does this token belong to? | `launchpad-generation-and-state`: authenticated factory-token-curve association, dependencies/implementation and token-specific lifecycle state at an identified block. An indexer classification is useful discovery, not an exhaustive factory census. |
| What would a buy cost, refund or graduate? | `launchpad-quotes-and-graduation` has unknown quote coverage: authenticate the applicable quote/simulation interface, pair asset/scales, amount/direction and fees. Available lifecycle inputs remain in generation/state and the role inventory. Actual cost/refund additionally needs receipt and attributable transfers. |
| Can a creator change fees or controls? | `launchpad-fees-and-controls`: applicable Config, fee recipient, module, escrow and authority evidence. A selected ABI or getter alone does not prove complete privileges. |
| Is another venue permitted? | `launchpad-venue-policy` is unknown: no deployed token permission ABI was acquired. Generation/state exposes scoped flags only. Authenticate the token's actual canonical-set and directional interface; the reference specification is not a deployed binding. |
| Do I receive a charter drop or pilot payout? | `charter-distribution-state` covers selected stimulus/top-up/refund and earlier-drop reads; newer drops separate available `launchpad-drop-snapshot-state` from unknown `launchpad-drop-entitlement`. `market-pilot-entitlement` remains unknown. See [drops](charter-distributions.md#launchpad-charter-drops) and [pilot rules](market-pilot.md), not a token-balance-derived reward estimate. |

## Curve and graduation

For the **new-generation guide reviewed October 19**, published mechanics are a fixed **1 billion-token supply with 18 decimals**, a pair-denominated curve, and a creator buy of up to **10% of published total supply** in the launch transaction. The guide describes a flat ETH launch fee but does not give an exact amount there. These are scoped documentation claims, not immutable defaults for arbitrary deployments or proof that every older token shares them.

The guide illustrates shape parameter **m = 3.5**, curve allocation `m / (m + 1)`, pool allocation `1 / (m + 1)` and final/start price ratio `m²`. Reserving tokens for a charter drop sizes the curve over the remaining supply while the described graduation raise stays the same, increasing the price per curve token. These formulas and illustrations do not establish deployed integer rounding, all fee sequencing or an executable pricing calculator. Use authenticated quotes for the actual token and amount rather than reconstructing a price from the picture.

The published final buy fills only the remaining curve amount, charges for that executed portion, returns the remainder and graduates **inside that same buy**. Quote, submitted input, executed cost, refund and graduation are separate facts; verify receipt/transfers and the refund asset instead of assuming a quote proves payment. Native ETH, WETH, USDG, stock units and launch-token units remain distinct. ETH-paired curves/pools hold WETH; the router is described as wrapping/unwrapping at the edges. Stock-route documentation's general statement that launch tokens only accept stock must not override the new guide's explicit ETH/WETH support.

The guide describes a graduated token/stock or token/WETH v4 pool, zero LP fee and hook-charged trading fees. It claims the pool opens at the curve's final price and the curve owns a full-range position with no withdrawal path. **Published locked/nonwithdrawable graduation liquidity is not a blanket safety guarantee**: it does not establish module safety, executable exits, issuer backing, all authority limits or absence of other pools/positions.

## Fees and creator controls

Keep these new-generation publisher fee streams separate; current deployed settings require their own evidence:

| Fee or allocation | Published basis and boundary |
| --- | --- |
| Base trading fee | 1% of the pair-asset side of buys and sells, on curve and graduated pool. Published split is 30% creator / 20% pilot reward pool / 50% protocol **of that base fee**, not of trade value. |
| Optional snipe fee | Extra fee on early curve buys, not sells, creator buy or graduated-pool swaps; all to protocol. Published seconds 0–6: 99%, 39%, 16%, 6%, 2.5%, 1%, 0.4%; none at 7+. The guide caps combined fees at 99%, reducing the snipe component if binding. This is dated guide content, not a live quote. |
| Module fee | Up to 10% extra on graduated-pool swaps, charged in the pair asset and allocated to the creator under the published Tier 1 model. |
| Integrator fee | Reacquired builder text says up to **1%**, payable to the chosen recipient in the same transaction. Buys assess only executed input; sells deduct from payout, with exact-output sells adding it on top. The earlier catch-up report says 2%; do not silently blend that discrepancy or use either as an authenticated current cap. |
| Creator escrow | Accumulated fees await claim. The guide says anyone can trigger claim, but payment goes to the token's current fee recipient, not the caller or all token holders. |

The rendered reward page's protocol-share wording and approximately 0.7%-of-trade examples conflict with the guide's 20%-of-base-fee pilot contribution. Preserve the [pilot source conflict](market-pilot.md#conflicting-published-rules); do not derive an exact reward entitlement or reconcile funding by naming the same fee twice. Source-established denominators do not establish every gross/net ordering across conversion, base, module, snipe and integrator fees.

Published percentage splits are not a decoder for every similarly named ABI field. In particular, a `creatorShareOfBaseBps` suffix does not establish its denominator: the older factory's fee-share scale remains unestablished without source arithmetic or authenticated publisher usage. Keep raw fee-share values separate from trading-rate BPS and from the new guide's published percentages.

**Creator, fee recipient, module and protocol authority differ.** The guide says fee-stream handover transfers unclaimed earnings and control of the module, venue blocks and outside-liquidity switch. Merely holding the token grants none of those rights. Authenticate the relevant authority and any pending-versus-accepted ownership state for current questions.

Published Tier 1 modules may add up to 10%, refuse buys and use bounded hook-managed records. They cannot refuse sells or move funds directly; decisions use a static call. The described failure behavior refuses buys while sells use the base fee. After graduation the creator can attach, replace or remove a module immediately; the protocol can disable a module address. Tier 2 describes sell-refusal, fee-ledger and rebate powers requiring protocol review/listing, but is explicitly **not available in the reviewed product**. Do not silently enable it or treat a reference template as an authenticated deployment. These are publisher mechanics unless exact source/deployment correspondence is independently established.

The guide's Config prose says the owner can replace protocol numbers in one call, effective immediately. The dated contract report records factory source `ILaunchConfig public immutable config`: **an immutable Config address is not immutable Config contents**, and changing contents is not replacing that factory's dependency address. Fresh acquisition could not recover explorer bodies, so the declaration remains attributed historical source inspection, not a newly reproduced whole-source certificate.

## Venue policy and URC5

[URC-5](https://raw.githubusercontent.com/Uniswap/URCs/863af9cddaf7eb9c3a40fdc9c8fa616c5945bea4/URCs/urc-5.md) is a **token-declared policy interface**, not authority for a hook or unrelated contract to speak for another token. Its canonical pools, mode and external permissions must be distinguished from actual transfer enforcement.

- **Preferred** recommends canonical pools without declaring venue restrictions. **Enforced** requires consumers to honor restrictions on boundary-crossing hops; the mode does not guarantee that the token can enforce every route onchain.
- Inbound permission concerns tokens moving into a venue; outbound concerns tokens leaving it. The directions are independent. A bulk unrestricted direction does not enumerate individual reactive refusals; the relevant point permission may still be needed. Ordinary wallet-to-wallet transfers are outside these venue restrictions, not proof that unrelated token rules never apply.
- A true permission is not execution success: pauses, caps, transaction-specific authorization and other checks can still fail. Missing/failed policy reads are unknown, not permission. Do not infer a complete policy from a truncated allowlist.
- The specification's reference implementation **omits enforcement**. Net-zero intermediate hops inside a shared PoolManager or other singleton can credit/debit the token without a visible token transfer; a transfer gate cannot force those hops through canonical pools or capture their canonical-hook fee. Netting does not remove a fee when the canonical pool itself is actually used.

The new launchpad guide claims own-pool-only tokens allow settlement only for hook-authorized amounts, keep ordinary transfers unaffected, permit inbound outside-venue blocks and allow the creator to open outside liquidity. It claims copies cannot be traded and routers need no changes. Keep these **attributed implementation claims**, not proved perfect vampire-pool prevention, universal router adoption or guaranteed sellability; the standard's observation limits still matter.

[PR 20](https://github.com/Uniswap/URCs/pull/20) was reported merged October 18, and the [October 19 announcement](https://x.com/standard_rsv/status/2112221351759286660) presents acceptance into the repository. The pinned canonical specification still says **Draft**, while [urc5.org](https://urc5.org/) says **Final**. Merge, document status, promotional status, deployed conformance and security review are separate claims.

## Evidence and integration limits

[Launchpad sources](../assets/sources/launchpad.json): `sr-launchpad-docs-2026-10-19`, `sr-launchpad-bindings-2026-10-19`, `sr-launchpad-creations-2026-10-19`, `sr-launchpad-selected-abis-2026-10-19`, `sr-launchpad-verified-abis-2026-10-19`, `sr-urc5-specification-2026-10-19`, `sr-urc5-announcement-2026-10-19`. The root-linked launchpad module and pinned URC text were inspected as data; imported numeric descriptions are also corroborated by the dated rendered guide. Publication time is not supplied for the guide. The reviewed artifact date is not the deployment date.

The dated catch-up reports selectively inspected explorer source, but fresh explorer requests were denied. Follow each role's actual [inventory coverage](interface-inventory-launchpad.md): selected publisher arrays support only their recorded calls/layouts, and an identity-only role has no invented ABI. Factory, router, curve, hook, Config, escrow, token and drop are distinct recording contracts, not a combined fictitious interface. Missing source or policy ABI limits the dependent conclusion without blocking useful authenticated public observations.

Current fees, owners, modules, policy lists, balances and token inventories stay outside this reference. [Market discovery](liquidity-markets.md#public-market-evidence) is optional publisher evidence, not a bundled client or permanent token router. The audit-expenditure announcement is not a report/scope/deployment certificate. Charter payout mechanics have one home in [launchpad charter drops](charter-distributions.md#launchpad-charter-drops); referral events and offchain points do not supply a reward estimator.
