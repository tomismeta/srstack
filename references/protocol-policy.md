# Supply, flow and issuance policy

Publisher design: `sr-whitepaper-v1` §§3–5,12,15; [source index](../assets/sources.json). Exact settings and provenance: [monetary parameters](../assets/parameters/monetary.json); removal shares: [participation](../assets/parameters/participation.json) and [reserves](../assets/parameters/reserves.json).

## Currency and supply — §3

Canonical settings: `hard-cap`, `token-decimals`, `genesis-liquidity`, `issuance-budget`. Genesis is the only pre-mint: protocol-owned liquidity single-sided above the owner-set launch price, with no upper price ceiling and described as non-withdrawable. The original issuance budget is not a measured remaining balance. On exhausting cumulative issuance budget, base issuance stops permanently; the publisher describes closed-loop recycling thereafter. Burns do not reopen that cumulative budget. [sr-whitepaper-v1: currency, reserves]

Issuance first credits internal ledger balances; actual tokens are minted on withdrawal. Permanent value removals differ from conversions:

- The current whitepaper retains 100% license-payment burning and describes the burned halves of resolution/revocation fees as permanent ledger removals. `license-burn-share` is a published rule, not a verified deployed proceeds split.
- Contraction Vault buybacks and protocol-position token-side fees burn wallet/pool tokens under the whitepaper design. POL Buyback acquisitions are separate: both current §11 and the official v1.1 policy send acquired tokens to the Incentives Vault unburned.
- Deposits destroy tokens but credit the ledger one-for-one; that value remains re-mintable on withdrawal. A deposit conversion is not a permanent economic burn.

With G = `genesis-liquidity`, H = `hard-cap`, M(t) cumulative withdrawal mints, B(t) permanent token burns, C(t) deposit conversions and R(t) permanent ledger removals, the published identities are:

- S_circ(t) = G + M(t) − B(t) − C(t).
- S_max(t) = H − B(t) − R(t).

The publisher calls the first quantity circulating supply, including genesis pool tokens. It says public burns and ledger removals lower the mintable ceiling, while the CentralBank deposit-conversion path is exempt; minted supply plus outstanding bank obligations must fit under that ceiling. These are source claims, not authenticated getter semantics or a substitute for implementation accounting. [sr-whitepaper-v1: currency equations 3.1–3.2]

Canonical accounting records: `circulating-supply-formula`, `mintable-ceiling-formula`, `deposit-ledger-conversion`. Formula strings describe the source, not verified callable code.

For read-only implementation context, the reviewed token source exposes `burnedForever()` and `ledgerRetired()` separately; [inspection](inspection.md#supply-restrictions-and-control-context) maps them to `token_burned_forever` and `token_ledger_retired`. Their sum is permanent cap reduction (`HARD_CAP - maxSupply`), not all buybacks. Token conversion burns remain distinct, and `maxSupply - totalSupply` is not the remaining cumulative issuance budget. The publisher conditions UI's “Burned forever” label describes the combined cap reduction; it must not be silently equated with the narrower token getter. Source-reviewed token accounting does not verify CentralBank ledger or settlement implementation.

The [official v1.1 announcement](updates.md#protocol-v11-announced-changes) confirms bid-side POL sending acquired tokens to the Incentives Vault, not burning them. It does **not** confirm the earlier proposed 50/50 branch-payment burn/incentive split. Retained vault balances, potential future distributions and eventual-burn proposals are not permanent removals. Keep current token/ledger burn counters separate from receipt-attributed causes: `history.py buybacks` covers Contraction Vault burn events, while `history.py pol-buybacks` reports raw acquired `tokensOut` and destination without inferring token identity, decimals or wallet flows. No announcement rewrites the supply identities or proves a complete deployed ledger settlement algorithm.

## Flow signal and policy — §§4–5

F_n = gross ETH entering through buys − gross ETH leaving through sells in epoch n. Issuance policy uses the trailing `signal-lookback` completed epochs; fee routing uses the sign of current F_n. Positive current flow means expansion; negative or zero means contraction. A current contraction-routing regime does not itself establish a negative trailing policy signal. The claim that capital-based measurement resists manipulation is an argument, not a demonstrated security result. [sr-whitepaper-v1: net-flow, policy]

The documented launch base (`base-issuance`) is **700,000 STANDARD/day before the multiplier**, not an already-scaled rate. The owner may lower it for the next epoch but never raise it back. For d days, base rate r and multiplier m_n, epoch issuance is I_n = r × d × m_n. A branch's daily-equivalent share is r × m / N while total branches N and other inputs stay fixed. Accrual streams second by second; a new branch earns from opening. [sr-whitepaper-v1: policy equations 5.1–5.2, branches]

`base-issuance-owner-policy` records the ratchet and effective-epoch claim. `time-to-full-issue` means opening at the full base rate, not time to exhaust the original issuance budget.

The official current-conditions explanation says “Epoch settlement is pending. Accrual is stopped until rollover” and “Settlement is required before the next epoch streams.” Treat this as a publisher-stated boundary on streaming, not a report that settlement is currently pending or a verified CentralBank implementation claim. Wall-clock passage alone does not prove rollover. Requested accrual scenarios may model explicit settlement pauses and assumed rollover times; they do not schedule or submit settlement transactions. [sr-protocol-conditions: epoch-end help and settlement notice]

A snapshot stream rate or daily-equivalent amount alone is not a settlement-aware forecast. Requested accrual or time-to-target calculations may hold that rate constant or model changes, with explicit assumptions for branch dilution, epoch boundaries, settlement delays, emissions status, policy-scaled base issuance and recycling. A scalar rate reduction does not establish the actual timing or effect of missed accrual; distinguish modeled timing from observed state. See [inspection](inspection.md#units-and-financial-interpretation).

`protocol` also observes queued policy with explicit pending flags and recycling state. Queued values are not active settings. `recycleStreamed` and `issuanceStreamed` remain raw ledger units because their scaling is unestablished; publisher-interpreted STANDARD quantities/rates have separate denomination evidence. Those getters alone do not establish ledger reconciliation or a future-accrual equation; any modeled treatment of unestablished scaling must be labeled as an assumption, not converted into a reported balance. [sr-extended-read-interface; inspection](inspection.md#units-and-financial-interpretation)

The source publishes `multiplier-floor`, `multiplier-ceiling`, `multiplier-launch`, `epoch-length`, `rate-cut`, `rate-raise` and `multiplier-update-rule`: a negative trailing signal cuts toward the floor; a positive signal sustained for the qualifying consecutive epochs raises toward the ceiling; otherwise the multiplier holds. The rate changes are additive multiplier steps, not percentage changes. Timing/dilution illustrations (`time-to-full-issue`, `time-to-multiplier-ceiling`, `time-ceiling-to-floor`, `ceiling-to-floor-dilution-cut`) retain their source meanings and limits; they are not unconditional forecasts. [sr-whitepaper-v1: policy]

These published formulas and launch values do not establish current issuance, multiplier, epoch length or branch supply; use fresh `protocol` readings and report unavailable fields as unknown. They also do not establish code correspondence, epoch-boundary rounding or future pool flows. Requested conditional forecasts, strategy comparisons and executable source-rule models may use the published recurrence without verified implementation, provided assumed flows, policy changes, timing and rounding are explicit and outputs are not represented as deployed behavior or guaranteed accrual. [Risks](risks.md#what-economics-alone-cannot-establish) covers modeling boundaries and owner controls; [contracts](contracts.md) covers implementation evidence.
