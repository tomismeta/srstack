# Supply, flow and issuance policy

Apply the [preparation and wallet boundary](safety.md#preparation-and-wallet-boundary).

Publisher design reviewed through **2026-09-26**: `sr-whitepaper-v1` §§3–5,12,15; [source index](../assets/sources.json). Dated monetary rules: [monetary parameters](../assets/parameters/monetary.json); removal shares: [participation](../assets/parameters/participation.json) and [reserves](../assets/parameters/reserves.json). These are not current execution settings.

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

The dated token-source review distinguishes permanent token burns from permanent ledger retirement; together they reduce the mintable ceiling, but neither is synonymous with all buybacks. Deposit-conversion burns remain distinct, and headroom below the mintable ceiling is not the remaining cumulative issuance budget. A UI “Burned forever” label may describe combined cap reduction rather than token burns alone. Authenticate current deployment and counter semantics before applying these distinctions; token-source evidence does not verify CentralBank settlement.

The [v1.1 announcement](updates.md#protocol-v11-announced-changes) describes retained POL acquisitions in the Incentives Vault, not burns, and does not confirm the earlier proposed 50/50 branch-payment split. Keep aggregate counters separate from receipt-attributed causes. For [historical buybacks](auction-history.md), distinguish Contraction Vault burns from POL acquisitions and authenticate token identity/units rather than inferring them from an event name.

## Flow signal and policy — §§4–5

F_n = gross ETH entering through buys − gross ETH leaving through sells in epoch n. Issuance policy uses the trailing `signal-lookback` completed epochs; fee routing uses the sign of current F_n. Positive current flow means expansion; negative or zero means contraction. A current contraction-routing regime does not itself establish a negative trailing policy signal. The claim that capital-based measurement resists manipulation is an argument, not a demonstrated security result. [sr-whitepaper-v1: net-flow, policy]

The documented launch base (`base-issuance`) is **700,000 STANDARD/day before the multiplier**, not an already-scaled rate. The owner may lower it for the next epoch but never raise it back. The whitepaper's base-issuance illustration is I_n = r × d × m_n for d days, base rate r and multiplier m_n, with daily branch share r × m / N at fixed branch count N. It describes second-by-second streaming and earnings from branch opening. This source-rule illustration does not establish deployed stream components (including recycling), integer units, checkpoint rounding or live eligibility; do not substitute it for the current bank calculation. [sr-whitepaper-v1: policy equations 5.1–5.2, branches]

`base-issuance-owner-policy` records the ratchet and effective-epoch claim. `time-to-full-issue` means opening at the full base rate, not time to exhaust the original issuance budget.

The official current-conditions explanation says “Epoch settlement is pending. Accrual is stopped until rollover” and “Settlement is required before the next epoch streams.” Treat this as a publisher-stated boundary on streaming, not a report that settlement is currently pending or a verified CentralBank implementation claim. Wall-clock passage alone does not prove rollover. Requested accrual scenarios may model explicit settlement pauses and assumed rollover times; they do not schedule or submit settlement transactions. [sr-protocol-conditions: epoch-end help and settlement notice]

A current stream getter is not interval earnings or a settlement-aware forecast. The dated [accrual-interface leads](interface-guide.md#accrual-inputs) and [implementation-evidence limits](research-workflow.md#accrual-evidence) distinguish authenticated publisher declarations from unproved CentralBank calculation semantics. Earned-only projections need attributable unspent earnings and a justified future-accrual model; total pending may include deposits or transferred balances. Unknown attribution allows bounded or explicitly assumed scenarios, not relabeling the ledger as earned. The STANDARD ledger funding of branch licenses is distinct from ETH funding of a new-charter auction; any conversion must be separately established and costed. See [exact earned-budget accounting](research-workflow.md#earned-only-projections-and-reinvestment).

Queued settings are not active. Raw policy/recycling counters do not establish denomination, ledger reconciliation or a future-accrual equation. Preserve unknown units rather than reporting an assumed balance. Segment forecasts at effective issuance/recycling changes, eligible-branch/global-denominator changes and epoch stops or resumption; wall-clock rollover and an auction pause are not proof of bank-accrual behavior.

The source publishes `multiplier-floor`, `multiplier-ceiling`, `multiplier-launch`, `epoch-length`, `rate-cut`, `rate-raise` and `multiplier-update-rule`: a negative trailing signal cuts toward the floor; a positive signal sustained for the qualifying consecutive epochs raises toward the ceiling; otherwise the multiplier holds. The rate changes are additive multiplier steps, not percentage changes. Timing/dilution illustrations (`time-to-full-issue`, `time-to-multiplier-ceiling`, `time-ceiling-to-floor`, `ceiling-to-floor-dilution-cut`) retain their source meanings and limits; they are not unconditional forecasts. [sr-whitepaper-v1: policy]

These published formulas do not establish current issuance, multiplier, epoch length or branch supply; use authenticated public reads and leave unavailable fields unknown. Source-rule scenarios may use the dated recurrence with explicit assumptions, but are not deployed behavior, guaranteed accrual or current earnings-funded affordability. [Risks](risks.md#what-economics-alone-cannot-establish) covers modeling boundaries; [contracts](contracts.md) covers implementation evidence.
