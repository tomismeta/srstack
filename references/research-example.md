# Fictional logs to an exact partial round summary

This is a **synthetic worked example**, not a deployment, saved live observation or suggested route. The installed `assets/examples/research-evidence-v1.json` is the single canonical example used by the source-only regressions. Its chain ID `999999`, `0x1111111111111111111111111111111111111111` emitter, all hashes, heights, header times and payment values are invented. `FICTIONAL_PAYMENT` has two decimals **only by this example's assumption**; it is neither STANDARD nor USD. Do not use these identities as network configuration.

Nothing executes on installation. These optional Python 3.10+ recipes use only the standard library, make no network calls and require no source checkout. Use them only under existing [host permissions](safety.md#public-retrieval-and-calls); they grant no wallet, signing or submission authority. Resolve the actual installed skill location first. Every command below works from any working directory:

```sh
SRSTACK_ROOT='/absolute/path/to/installed/srstack'
python3 -I -B "$SRSTACK_ROOT/scripts/research.py" rounds \
  --input "$SRSTACK_ROOT/assets/examples/research-evidence-v1.json"
```

The command consumes the existing evidence-v1 input mode, not raw RPC logs. It does not decode ABI data or authenticate the evidence. The following steps explain the mapping already present in the example.

## Raw logs and decoded observations

`extensions.example.raw_logs` preserves ten Ethereum-shaped log observations: hexadecimal block/transaction/log indices, 20-byte address, 32-byte hashes and topics, ABI data, and the source's `removed` flag. One deliberately incomplete export omits `logIndex`. The top-level `events` array is the corresponding evidence-v1 representation; `raw_log_ref` joins each observation to its raw record. Normalized integer fields are decimal strings. Raw topics/data remain alongside the decoded values so disagreements need not be erased.

The [reviewed purchase-event layout](interface-guide.md#branch-license-auction-events) is used to illustrate decoding, not to authenticate this fictional emitter:

- Signature: `LicensesPurchased(uint256,uint256,uint256,uint256)`.
- Topic0: `0x01862d9110233f6709760be3b1cc45660f4b8b0698777de996e5a7d262638fb5`.
- Topic1 is indexed `charterId`; topic2 is indexed `day`. The latter maps to `round_id`, not a calendar date. Charter ID and round ID are different domains.
- Data word0 is nonindexed `count`, mapped to `quantity`; data word1 is nonindexed `unitPrice`, mapped to `unit_price_raw`. Both are unsigned 32-byte integers. Consideration is **count × unitPrice**, not unitPrice alone, a transaction's value or a second supporting ledger event.
- `logIndex` is the **block-global** log index, not the transaction-local event ordinal. The unusual indices below are intentional.

This small decoder reads the installed raw records and demonstrates the exact values placed in `events`. It is an illustration for this one static ABI layout, not a new transport or a general ABI decoder:

```sh
python3 -I -B - "$SRSTACK_ROOT/assets/examples/research-evidence-v1.json" <<'PY'
import json
import sys
from pathlib import Path

packet = json.loads(Path(sys.argv[1]).read_text(encoding="utf-8"))
topic0 = "0x01862d9110233f6709760be3b1cc45660f4b8b0698777de996e5a7d262638fb5"
for observation in packet["extensions"]["example"]["raw_logs"]:
    log = observation["log"]
    topics = log["topics"]
    data = bytes.fromhex(log["data"][2:])
    if len(topics) != 3 or topics[0] != topic0 or len(data) != 64:
        raise ValueError("Not the illustrated LicensesPurchased layout")
    decoded = {
        "event_name": "LicensesPurchased",
        "charter_id": str(int(topics[1], 16)),
        "round_id": str(int(topics[2], 16)),
        "quantity": str(int.from_bytes(data[:32], "big")),
        "unit_price_raw": str(int.from_bytes(data[32:], "big")),
    }
    position = {name: str(int(log[rpc], 16)) if rpc in log else "unknown"
                for name, rpc in (("block_number", "blockNumber"),
                                  ("transaction_index", "transactionIndex"),
                                  ("log_index", "logIndex"))}
    print(observation["id"], json.dumps({**position, "decoded": decoded}))
PY
```

The example adds chain/emitter/generation, hashes, removal flags, denomination and source references to these decoded observations. Sources have unknown retrieval/observation times; those times must not replace header timestamps. Headers are keyed by chain plus block hash. Two different hashes at height 105 are retained; one timestamp is unknown. No current canonicality is asserted.

| Record | Height / block-global log index | Charter / round | Quantity | Raw unit price | Treatment |
| --- | --- | --- | ---: | ---: | --- |
| `sale-a` | 100 / 2 | 41 / 7 | 2 | 105 | Uncontested; synthetic matched-success receipt check |
| `sale-b` | 101 / 7 | 42 / 7 | 3 | 99 | Uncontested; receipt not checked |
| `sale-c` | 102 / 4 | 43 / 7 | 1 | 101 | Uncontested; receipt not checked |
| `removed` | 103 / 5 | 44 / 7 | 9 | 90 | Removed; retained separately, not counted |
| `conflict-a` | 104 / 9 | 45 / 7 | 4 | 90 | Same identity as next row; conflicting content, neither counted |
| `conflict-b` | 104 / 9 | 45 / 7 | 5 | 90 | Competing quantity and raw data, not another purchase |
| `reorg-a` | 105 / 3 | 46 / 7 | 8 | 80 | Unresolved competing block hashes, neither counted |
| `reorg-b` | 105 / 3 | 46 / 7 | 10 | 80 | Alternative hash/transaction; timestamp unknown |
| `sale-d` | 106 / 6 | 47 / 7 | 1 | 98 | Uncontested; receipt not checked |
| `incomplete` | 107 / unknown | 48 / 7 | 6 | 95 | Deferred: missing block-global log index |

To make `incomplete` usable for aggregation, obtain its complete log or matching receipt, anchored to the same chain/transaction/block hash, to recover the missing block-global index and reconcile any alternatives. Do not guess `0`, use arrival order, or substitute a transaction-local ordinal. Its raw quantity and price are already decodable; unknown identity is not zero quantity. Its missing header timestamp independently prevents a timed endpoint claim, but does not prevent quantity accounting once identity is established. For a real canonical-sale claim, ABI/emitter/units, receipt and canonicality evidence still need their own support.

## Exact expected partial result

There is one emitter/round/denomination group. Only `sale-a`, `sale-b`, `sale-c`, `sale-d` contribute to its **uncontested supplied-observation subtotal**:

- Quantity `Q = 2 + 3 + 1 + 1 = 7`.
- Raw consideration `C = 2×105 + 3×99 + 1×101 + 1×98 = 706`, exactly `7.06 FICTIONAL_PAYMENT`.
- Exact weighted raw unit price `706/7`; integer quotient `100`, remainder `6`, satisfying `706 = 100×7 + 6`.
- Exact asset-unit average `706/(7×100) = 353/350`; six-decimal half-even display `1.008571`. Averaging four event prices without quantity weights would be wrong.
- Uncontested minimum unit price `98` raw (`0.98` asset units), also the last observed unit price here. Neither establishes a protocol floor or future offer.
- First observed eligible record: `sale-a`, position `(100, 1, 2)`, header timestamp `1000`.
- Last observed eligible record: `sale-d`, position `(106, 1, 6)`, header timestamp `1127`.
- Observed span `1127 − 1000 = 127` seconds, exactly **2m7s**. The incomplete row is deferred, not silently assigned the last time. First/last in this helper include disputed complete observations if they occupy an endpoint; they are not necessarily uncontested sales.
- One conflict identity (two variants), two disputed reorg identities, one removed observation and one deferred observation remain visible. None is silently dropped from the packet.

This is **not sellout time**, a scheduled-opening duration or a proved closing sale. There is no supply/exhaustion evidence or authenticated scheduled opening. Block 108 is failed and blocks 109–110 unsearched. Supplied scan scope 100–107 is not proof of uncapped/exhaustive discovery. Only one receipt check is matched; the others are not checked. Receipt coverage, discovery coverage and canonicality remain separate from arithmetic. See [history evidence](auction-history.md) and [research tools](research-tools.md).

## Exact table and duration

This recipe calls the installed `rounds` CLI and formats its exact JSON result without binary floating point. `Fraction` preserves the average; the explicit display rule is round-to-nearest, ties-to-even at six decimal places. Duration uses integer `divmod(seconds, 60)` with no minute rounding. It adds no CLI flag or runtime input mode and writes no files:

```sh
python3 -I -B - "$SRSTACK_ROOT" <<'PY'
from fractions import Fraction
import json
from pathlib import Path
import subprocess
import sys

root = Path(sys.argv[1])
if not root.is_absolute():
    raise SystemExit("Supply the absolute installed skill path")
summary = json.loads(subprocess.check_output(
    [sys.executable, "-I", "-B", str(root / "scripts/research.py"), "rounds",
     "--input", str(root / "assets/examples/research-evidence-v1.json")], text=True))

def fixed(value, places):
    # Exact round-to-nearest, ties-to-even; supports either sign.
    value = Fraction(value)
    magnitude = abs(value) * 10**places
    quotient, remainder = divmod(magnitude.numerator, magnitude.denominator)
    if 2 * remainder > magnitude.denominator or (
            2 * remainder == magnitude.denominator and quotient % 2):
        quotient += 1
    whole, fractional = divmod(quotient, 10**places)
    sign = "-" if value < 0 and quotient else ""
    return f"{sign}{whole}.{fractional:0{places}d}"

print("round | quantity | consideration FICTIONAL_PAYMENT | average/unit | observed span")
for group in summary["rounds"]:
    totals = group["uncontested_totals"]
    scale = 10 ** int(group["key"][4])
    average = totals["average_raw"]
    average_text = "unknown" if average is None else fixed(
        Fraction(int(average["numerator"]), int(average["denominator"]) * scale), 6)
    seconds = group["observed_span_seconds"]
    if seconds is None:
        duration = "unknown"
    else:
        minutes, remaining_seconds = divmod(int(seconds), 60)
        duration = f"{minutes}m{remaining_seconds}s"
    consideration = fixed(Fraction(int(totals["consideration_raw"]), scale), 2)
    print(f"{group['key'][2]} | {totals['quantity']} | {consideration} | "
          f"{average_text} | {duration}")
PY
```

Expected display:

```text
round | quantity | consideration FICTIONAL_PAYMENT | average/unit | observed span
7 | 7 | 7.06 | 1.008571 | 2m7s
```

The narrow display recipe assumes this example's known, single two-decimal denomination. General evidence can contain separate emitters/assets, unknown denominations, tied or unknown endpoints, and zero quantity; preserve those distinctions instead of copying this display as a general reporting contract. The unrounded rational and quotient/remainder remain in CLI JSON. The table is a presentation of a partial fictional subtotal, not a verification upgrade.
