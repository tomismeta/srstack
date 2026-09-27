# Optional close-projection calculations

These six pure Python 3.10+ helpers in `scripts/calculations.py` are optional, offline and standard-library-only. They add no CLI mode, network client, dependencies, live data, wallet action or protocol defaults. Existing calculation helpers and the five `research.py` modes are unchanged. Permission and evidence rules in [safety](safety.md), [auction history](auction-history.md), and [round datasets](round-datasets.md) still apply.

## Before projecting

**Consult the latest relevant curated round dataset before deriving a policy opening.** Select a compatible chain, auction family, contract generations and price denomination. Check pinned source head, header times/hashes, coverage, new rounds and setting changes; record why the dataset remains current. Helpers have no wall clock, do not fetch updates and cannot certify freshness or canonicality. Stale, missing, incomplete or conflicting evidence is not permission to invent a numeric close. The installed fixture is deliberately fictional, not a fallback for missing live history or the unavailable 19-round seed.

Keep four distinct quantities visible:

| Quantity | Meaning |
| --- | --- |
| Policy-derived opening | Explicit policy multiplier × qualified prior close; **not** an expected transaction price |
| Current inventory-conditional quote | Supplied curve scenario at supplied elapsed time, subject to remaining inventory and other purchase constraints |
| Observed last sold / qualified close | An observed print; only call it an exhausted close when allocation, coverage and sellout evidence support that claim |
| Current floor / future floor | Historical or pinned current floor is known only as supplied; **future floor remains unknown** |

The reported 2026-09-27 license 2× and charter 3× day-0→1 opening ratios, continuing decay after zero inventory and unchanged `currentDay` until the scheduled boundary are scoped observations. They support conditional publisher scenarios, not all-generation implementation certificates. Use an explicit scenario multiplier, not a hardcoded live ratio. A scheduled boundary is a candidate schedule, not promised inventory, an early sellout rollover or a guaranteed fill.

## Installed-path setup and numeric contract

Resolve the actual installation path; commands work from any working directory and need no source checkout:

```sh
SRSTACK_ROOT='/absolute/path/to/installed/srstack'
```

Each recipe below independently loads the installed module with `runpy`, consumes the same installed synthetic fixture, and prints Python values using `pprint`. `Fraction` values remain exact; `Decimal` values are not silently converted to binary floats. For an actual analysis, replace the example input with an explicitly selected curated dataset and explicit analysis parameters, after the evidence checks above. See [round datasets](round-datasets.md) for schema, provenance and durable storage.

Raw integer inputs accept nonnegative Python integers or canonical decimal strings, never floats or booleans. Rational inputs accept integers, `Fraction`, finite `Decimal` or exact numeric strings, with existing magnitude limits `[1e-1000, 1e1000]` for nonzero values. `precision` is an explicit integer from 16 through 200. Decimal work uses an isolated context of `precision + 12` digits, not the caller's global context. Bounded outputs have `value`, `lower_bound`, `upper_bound`, `absolute_error_bound`, `precision` and `working_precision`. Numerical bounds enclose arithmetic error only; they say nothing about empirical uncertainty, source errors or deployed integer rounding.

Round identities are `(generation, lowercase contract, day)`, with duplicate identities rejected. Chronology uses scheduled start where known, otherwise first-sale timestamp, otherwise last-sale timestamp; records with no chronology are explicitly excluded. Ties sort by identity, not an invented time difference. Day IDs can reset across generations. Callers must establish economic comparability; shared labels alone do not establish equivalent markets or policy regimes.

## 1. Recent sellout close/open ratio statistics

**Inputs:** curated `rounds`, explicit positive `trailing`, and `precision`. Admission requires `sellout is True`, positive `start_price_raw`, known last-sale price, `sold == round_cap > 0`, complete coverage, a supplied nonempty sellout basis, `timestamp_basis == "block_headers"`, and known first/last sale block and timestamp anchors in nondecreasing order. Source/evidence references must be reviewed by the caller; the helper does not resolve or authenticate them. Zero allocation alone is not evidence of demand-driven exhaustion.

Qualified sellouts also require known observation-head block and timestamp. Sale anchors beyond a supplied head are excluded, including in leaf trends; those contradictory observations cannot establish a known close.

```sh
python3 -I -B - "$SRSTACK_ROOT" <<'PY'
import json, runpy, sys
from pathlib import Path
from pprint import pprint
root = Path(sys.argv[1])
api = runpy.run_path(str(root / 'scripts/calculations.py'))
fixture = json.loads((root / 'assets/examples/projection-evidence-v1.json').read_text())
request = fixture['projection_request']
pprint(api['sellout_ratio_summary'](fixture['dataset']['rounds'],
    trailing=request['trailing'], precision=request['precision']))
PY
```

**Outputs:** `ratios`, `mean` and `sample_variance` are exact `Fraction` values. For selected ratios $r_i=C_i/O_i$, the mean is $\bar r=\sum r_i/N$ and sample variance is $\sum(r_i-\bar r)^2/(N-1)$. `sample_variance_ddof` is 1. `sample_sd` bounds the square root. At least two eligible observations are required. `count`, `selected_rounds`, total `qualified_count`, and `excluded` identities/reasons disclose scope; `trailing` selects up to that many most recent eligible observations, not a hidden default sample.

The fictional six-round sample has mean approximately `0.4742302851986265` and sample SD approximately `0.00248659342177725`. These are computed fixture results, **not** a default 0.48 ratio. Selection proves neither all-history sellout nor recurrence. Incomplete/no-sale/unknown rows are not zero-filled or treated as sellouts.

## 2. Exact last-sold close trend

**Inputs:** comparable chronological round records and explicit `trailing`. The leaf helper admits known last-sale prices with a node-header last-sale anchor; when a first-sale anchor is also supplied, their order must agree. It does not require sellout or a known first sale, so partial last-sold observations remain observations rather than proved closes.

```sh
python3 -I -B - "$SRSTACK_ROOT" <<'PY'
import json, runpy, sys
from pathlib import Path
from pprint import pprint
root = Path(sys.argv[1])
api = runpy.run_path(str(root / 'scripts/calculations.py'))
fixture = json.loads((root / 'assets/examples/projection-evidence-v1.json').read_text())
pprint(api['close_trend_projection'](fixture['dataset']['rounds'],
    trailing=fixture['projection_request']['trailing']))
PY
```

**Outputs:** exact `slope_raw_per_round`, `intercept_raw` and `next_raw`, plus selected identities, raw prices, counts and exclusions. Ordinary least squares fits $y=a+bx$ with $x=0,\ldots,N-1$ and extrapolates at $x=N$. This is an **ordinal selected-round axis**, not elapsed-time regression or arithmetic on resettable day IDs. At least two observations are required. Missing/excluded rounds compress this axis and must be disclosed.

For the fixture, slope is `-39900` raw units per selected round, intercept `840000` and next raw close `600600` (`6006` in this fixture's two-decimal display). No float fitting, clipping of negative extrapolations, floor substitution or claim of executability occurs. A negative fit is diagnostic evidence that this simple extrapolation is unsuitable, not a plausible price repaired to zero.

## 3. Structural close estimate and descriptive band

**Inputs:** an explicitly derived `policy_open_raw`, the ratio summary, and `precision`. The runnable example obtains its opening from the composed recipe so it does not silently use an unqualified last print.

```sh
python3 -I -B - "$SRSTACK_ROOT" <<'PY'
import json, runpy, sys
from pathlib import Path
from pprint import pprint
root = Path(sys.argv[1])
api = runpy.run_path(str(root / 'scripts/calculations.py'))
fixture = json.loads((root / 'assets/examples/projection-evidence-v1.json').read_text())
request = fixture['projection_request']
context = api['project_next_close'](fixture['dataset'], **request)
pprint(api['structural_close_projection'](context['policy_open']['value_raw'],
    context['ratio_summary'], precision=request['precision']))
PY
```

**Outputs:** `central_raw = policy_open_raw × mean` is exact. `mean` and `sample_variance` stay exact. `sample_sd` has separate numerical bounds. `band_raw.lower` bounds the endpoint $O(\bar r-s)$ and `band_raw.upper` bounds $O(\bar r+s)$. Each endpoint is its own bounded Decimal result. `band_standard_deviations` is 1 and `is_confidence_interval` is false: this is descriptive empirical dispersion, **not** a confidence interval, calibrated prediction interval or contractual regularity. Numerical endpoint errors are not the empirical band width. A negative lower endpoint remains negative.

The fixture policy opening is `1281000` raw units, but its structural central close is approximately `607488.9953394405` raw units (`6074.889953394405` display units). The descriptive band is approximately `[604303.6691661439, 610674.3215127372]` raw units. Neither the high policy opening nor the band is an executable transaction quote.

## 4. Historical floor context, future floor unknown

**Inputs:** supplied round records and explicit `trailing`. This recipe retains recent chronological rounds whether or not they sold out.

```sh
python3 -I -B - "$SRSTACK_ROOT" <<'PY'
import json, runpy, sys
from pathlib import Path
from pprint import pprint
root = Path(sys.argv[1])
api = runpy.run_path(str(root / 'scripts/calculations.py'))
fixture = json.loads((root / 'assets/examples/projection-evidence-v1.json').read_text())
pprint(api['floor_trend_context'](fixture['dataset']['rounds'],
    trailing=fixture['projection_request']['trailing']))
PY
```

**Outputs:** `series` preserves each selected identity and `floor_price_raw`, including explicit `None` for missing floors. `known_count`, exact historical slope/intercept where at least two floors are known, and exclusions disclose scope. OLS uses the original selected-round ordinals, preserving missing-floor gaps rather than compressing known points. `future_floor_raw` is **always `None`**. The fixture's historical floor slope is `-26600` raw units per selected round and last known floor is `400400`; neither authorizes projecting the future floor or reusing today's floor as tomorrow's floor.

## 5. Inventory-gated curve quote and phantom guard

**Inputs:** explicit opening, floor, half-life and elapsed time in compatible units, `remaining_today`, and `precision`. The helper wraps existing `gap_to_floor_scenario` for $F+(O-F)2^{-t/h}$, retaining its input restrictions and bounded numerical arithmetic. This is an assumed mathematical curve, not certification of the deployed equation or rounding.

```sh
python3 -I -B - "$SRSTACK_ROOT" <<'PY'
import json, runpy, sys
from pathlib import Path
from pprint import pprint
root = Path(sys.argv[1])
api = runpy.run_path(str(root / 'scripts/calculations.py'))
fixture = json.loads((root / 'assets/examples/projection-evidence-v1.json').read_text())
pprint(api['auction_curve_quote'](**fixture['phantom_request']))
PY
```

**Outputs:** with `remaining_today == 0`, `status` is `phantom_not_buyable` and `buyable_price_raw` is `None`. The fixture still has diagnostic curve value approximately `602299.2293024169` raw units at elapsed 900, below its observed exhausted close of `640500` raw at elapsed 800. That diagnostic is explicitly **not purchasable inventory**. Curve decay alone neither changes the proved last close nor advances `currentDay`.

Positive inventory gives `inventory_conditional` and a bounded-curve approximate `buyable_price_raw`; consult `diagnostic_curve` for its numerical bounds. `is_guaranteed_fill` remains false. Unknown inventory (`None`) gives `availability_unknown` with no buyable price. Neither positive inventory nor zero allocation substitutes for all purchase constraints. `exact_curve_raw` is a `Fraction` for integer elapsed/half-life or equal opening/floor; otherwise it is `None` and `diagnostic_curve` supplies bounded Decimal evaluation of the generally irrational expression. There is no alternate sold-out heuristic.

## 6. Composed next-close procedure

**Inputs:** an explicitly selected latest curated dataset, `trailing`, positive explicit `policy_multiplier`, and `precision`. In this synthetic command only, those parameters come from the installed fixture's request object:

```sh
python3 -I -B - "$SRSTACK_ROOT" <<'PY'
import json, runpy, sys
from pathlib import Path
from pprint import pprint
root = Path(sys.argv[1])
api = runpy.run_path(str(root / 'scripts/calculations.py'))
fixture = json.loads((root / 'assets/examples/projection-evidence-v1.json').read_text())
pprint(api['project_next_close'](fixture['dataset'], **fixture['projection_request']))
PY
```

The procedure:

1. Requires a v1 dataset and explicit analysis parameters; establishes the recent evidenced-sellout sample and reports incomplete/no-sale/unknown exclusions.
2. Rejects fewer than two qualified observations. Also rejects any record without chronology or a latest supplied round that is not the latest qualified sellout close. It must not silently drop a newer partial, no-sale or unknown round and forecast “next” from an older close. Historical leaf summaries can still be used to inspect such data.
3. Binds `target.after_round` to that latest qualified round. The target is the next round after this identity; `day` and `scheduled_window` remain unknown rather than guessing a generation reset or boundary.
4. Derives `policy_open.value_raw = last_qualified_close.price_raw × policy_multiplier`, preserving exact rational arithmetic and `is_expected_transaction_price: False` on **the opening**.
5. Returns both `trend` and `structural` next-close projections using the same qualified sample, alongside `ratio_summary`, separate `last_observed` and `last_qualified_close` records, exclusions, dataset metadata and historical `floor_context`. Both top-level and floor-context future floors remain `None`.
6. Retains structured assumptions: continued sellout is conditional; comparable units/regime are required; freshness was not verified by the helper; the multiplier is an explicit scenario; not all history is proved sold out; the result is not an executable quote.

For this fixture only, the four quantities are policy opening `1281000` raw, phantom current curve approximately `602299.2293` raw with **no buyable quote**, last qualified close `640500` raw, and current floor `400400` raw with **future floor unknown**. The two next-close estimates are trend `600600` raw and structural approximately `607488.9953` raw, not the policy opening. The fixture has six stipulated exhausted rounds; it is not a recovered live 19-round history or a forecast for an actual deployment.
