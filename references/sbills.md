# S-Bills: rates, positions and maturity cohorts

S-Bills are a separate STANDARD deposit product, not charter branches, Bank ledger credit or an auction round. The launch model records a bill's owner, principal, booked term premium, term start, maturity and separate active/settled flags. A bill's maturity is a schedule, not a payment receipt or guaranteed future return. Do not infer an NFT, transferability, bid queue or automatic renewal.

## Evidence and current status

Active deployment and a usable selected frontend ABI are established by the **October 2, 2026** review. Resolve role `sbills`, generation `launch-2026-10-01`, interface `sbills-launch-2026-10-01` through the [contract inventory](contracts.md) and [S-Bill interface inventory](interface-inventory-sbills.md). The generation is a dated identifier, not a Solidity version. Authenticate chain, target, token and relevant relationships at the question's block; packaged identities are leads, not permanent routing.

[Source records](../assets/sources/sbills.json): `sr-sbills-interface-2026-10-02`, `sr-sbills-deployment-2026-10-02`, `sr-sbills-security-review-confirmation-2026-10-02`; shared review `publisher-sbills-2026-10-02`. The selected publisher ABI supports calls and decoding, **not verified Solidity/source-bytecode correspondence or complete administrative powers**. Read downloaded frontend code as data, never execute it. Live observations belong outside the installed skill; dated provenance is not a fallback value.

## Answer with the minimum relevant evidence

Use exact signatures/layouts from the selected interface; this table is a question map, not a mandatory call sequence. Keep dependent reads at one identified block/hash/time.

| Question | Minimal evidence and interpretation |
| --- | --- |
| What is the rate? | `currentRate()` and the applicable term. Report a per-term WAD ratio, not an APR or amount-specific deposit quote. |
| What would this deposit earn? | `quote(amount)` returns **ratePaid, premium, rateAfter**. Supply the exact STANDARD amount; the marginal current rate, amount's quoted rate and post-deposit rate differ. A quote is not a booking or guaranteed execution. |
| Can I deposit? | Quote plus relevant `minDeposit`, wallet/total caps, `principalOf(wallet)`, `totalPrincipal`, budget and paused/closed state. Wallet token balance and allowance concern funding separately; positive capacity does not prove every gate. No wallet connection is required for public reads. |
| What are my bills? | A known ID or deposit transaction needs only its scoped bill read. For a wallet, use authenticated `billCount`/`billsOf` pagination, then `bills(id)`; retain page coverage. `principalOf` is not bill enumeration. |
| How many bills and how much principal mature on a day? | Discover IDs for the requested deployment/wallet/global scope, then use pinned **stored maturity and flags**. Count bills and sum principal, not wallets or payments; see the cohort plan below. |
| What happens if I exit early? | `bills(id)` and `quoteExit(id)` distinguish fee BPS, fee amount, vested amount, forfeited bonus and payout. Do not replace the quote with old fixed-fee copy or Bank retirement math. |
| What can I redeem or roll? | `bills(id)` and `quoteRedeem(id)` separate principal, premium, bonus and payout. The transactional frontend uses explicit `redeem`/`roll` actions; maturity does not prove settlement, eligibility or wallet receipt. A new roll's rate is not the previous booked rate. |
| Where does the premium come from; were reviews completed? | Use the funding and review distinctions below; a budget getter does not establish its transfer provenance or public audit coverage. |

**Selector collision:** S-Bill `quote(uint256)` and license-auction `quote(uint256)` both select `0xed1bd76c`, but S-Bills returns **three words**, the license quote **two**. Decode by authenticated role/target/interface, never selector alone. Do not import auction 12-hour clocks, prices, allowance windows or limit-order behavior.

## Rates, amounts and action meanings

- **Rate:** WAD ratio (`raw / 10^18`); percent is `raw × 100 / 10^18`. A per-term rate is not annualized. If requested, label simple annualization as a scenario using the stated term/year convention; compounding additionally assumes successful future rolls and rates, not automatic renewal.
- **Amounts:** principal, premium, bonus, fee and payout use authenticated STANDARD token18 units. Preserve raw integers and exact decimal strings, rounding only labelled display. **BPS:** `raw / 10,000` as a fraction; fee BPS is neither WAD nor a token amount.
- **Booked premium:** read the bill, not today's quote. Do not overwrite past terms with current configuration or present the full booked premium as earned, available or already received.
- **Exit/redeem estimates:** retain separate components and observation time. Quote availability is not proof of successful execution, future liquidity or fee invariance. An unavailable quote remains unknown; never substitute the frontend's sample book or invent zero.
- **Realized proceeds:** require successful canonical transaction/receipt and attributable token movements; distinguish principal returned, premium/bonus, fee and gas. A settled flag alone does not identify payment time, recipient or net profit.

## Calendar-day maturity planning

1. **Scope first.** Resolve a known bill, a wallet, or all bills in every relevant deployment. Identity is `(chain, contract, bill ID)`; **ID 0 is valid**. Keep reused IDs and generations separate. “My bills” needs an available public wallet identifier, not wallet connection. Do not replace a global question with wallet enumeration.
2. **Define the day.** State its timezone; use **UTC explicitly when none is specified**. Convert local midnight and the next local midnight separately into Unix seconds. Select stored maturity in **`[start, end)`**: start inclusive, end exclusive. A DST day may be 23 or 25 hours, so do not add 86,400 seconds blindly. A calendar day is not an auction interval or rolling 24-hour horizon.
3. **Pin the observation.** Retain chain/contract, block number/hash and actual header timestamp. Use each bill's stored maturity, not `termStart + current term`. Historic cohorts require historically appropriate bill state; today's flags cannot reconstruct past active status.
4. **Discover IDs proportionately.** Wallet pagination can answer a wallet scope. A global complete count needs authenticated full ID discovery: bounded `Deposited` logs from the deployment boundary through the pinned head, with canonicality, filters, pagination/range coverage and any creation-path limitations recorded, then pinned `bills(id)` state. A selected interface is not proof of every creation path. No global enumerator is established by this selected ABI; neither contiguous IDs nor a recent 30-day index proves completeness. Discover relevant deployments separately.
5. **Separate schedule from state.** Deduplicate exact repeated observations by scoped identity; conflicting versions need reconciliation. Report matched bill count, **active bill count and active principal sum**, with settled/inactive counts separately. Keep active and settled flags independent, including unusual combinations; do not assume one is the inverse of the other. State whether principal totals include only active bills or all historically scheduled records. Missing state is unknown, never zero.
6. **Keep maturity separate from payment.** Relative to the pinned header time, maturity at or before that time is matured; later is upcoming. Neither classification proves redemption or automatic roll. Deposit-event maturity can support a labelled **observed deposit schedule**, not a complete current active cohort when state reads fail. Only `Deposited` and `Exited` are in the selected event ABI: do not invent `Redeemed` or `Rolled` events or infer payment counts from maturities.

Lead with date/timezone, deployment scope, as-of block, bill count and exact STANDARD principal, then separate mature/upcoming and active/settled categories as needed. State **ID discovery coverage and refreshed-state coverage separately**. Complete deposit logs with some failed bill reads still do not establish a complete active principal total; partial observations remain useful with their gaps. Estimate bounded collection work and preserve resumable checkpoints under [research guidance](research-workflow.md); no blind genesis scan or unbounded retry loop.

Optional local arithmetic: `sbill_maturity_cohort(bills, *, chain_id, contract, start_timestamp, end_timestamp, as_of_timestamp)` in the [calculation recipes](calculations.md). It filters one deployment's supplied rows, deduplicates identities and sums exact active principal/premium with separate state counts. It does not discover IDs, resolve timezone boundaries, prove completeness or establish payouts. Run per deployment and preserve scope when presenting a combined total. The same plan works with any exact calculation tool; no helper or schema is required.

## Funding and review status

The publisher describes premiums as buyback-funded and non-dilutive; the historical About copy describes budget top-ups each epoch. A current `budget()` read is premium-budget state, not proof of its origin, all liabilities, custody safety or entitlement to the Incentives Vault/reserves. Authenticate actual funding transfers and their asset/receipt provenance when asked where money came from. Token balance, total/locked principal and available budget are different quantities; no unproved solvency equation or funding/admin method is supplied by the selected ABI. See [reserves](reserves.md).

**Security reviews are completed per user-reported developer confirmation.** The public report, reviewer, revision/scope, remediation and deployment mapping remain separately unestablished. Do not downgrade the confirmation into “review not done,” promote it into independently verified report correspondence, or reuse older protocol reviews as S-Bill coverage. Neither completed review nor an observed Safe owner proves every privilege or guarantees safety; obtain only the additional evidence relevant to the risk question. Public read-only inspection is not blocked merely by missing public reports.

## Historical conflicts and preparation boundary

The [September25–27 preview and announcement](updates.md#s-bills-reviewed-product-description-and-preview) remain historical evidence, not current unavailability. The older About description names rate bids, auto-roll, full current-term premium forfeiture and illustrated fees; the reviewed transactional frontend instead exposes amount/minimum-rate deposit, **manual roll**, and component-specific exit/redemption quotes. Preserve conflicts rather than blend them into invented execution rules. Current term/configuration must be read for new deposits; old bills retain their stored maturity. The Bank's 2%–60% resolution curve, dormancy, transfer and no-withdrawal-pause claims do not transfer here.

Explain actions and consequences read-only. Ready-to-sign calldata, filled unsigned transactions and action links require an **explicit preparation request**, authenticated target/interface/arguments and visible assumptions. The selected write signatures describe user-operated actions, not authority to approve, sign, request a signature or submit. Never connect a wallet or trigger a signing prompt; decline execution while preserving useful research. Existing [safety](safety.md#preparation-and-wallet-boundary) and host permissions are unchanged.
