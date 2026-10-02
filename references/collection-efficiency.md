# Efficient evidence collection

Use the smallest sufficient reads, then reduce transport overhead—not evidence quality. This optional recipe uses existing authorized host tools; it adds no installed RPC client, provider, credential store or required workflow. A denied tool/action is not permission to reproduce it through another transport. Follow [execution](execution.md) and [safety](safety.md).

## Plan once, collect in dependency stages

1. **Scope and pin.** Authenticate chain, targets and interfaces; resolve one block number/hash/header timestamp for dependent state. Generate its hexadecimal tag from the integer, not by transcription. A batch of `latest` calls is not a pinned snapshot. Reconcile canonicality when using numeric tags or changing providers.
2. **Resolve dependencies.** Discover IDs or transaction hashes before fetching their state/receipts; fetch a page cursor before its next page. Do not invent IDs to parallelize enumeration. Group only reads supported by the same authorized transport and evidence context.
3. **Deduplicate requests.** Within that context, identical method/complete-parameter requests need one fetch. Keep a mapping back to every consumer. Preserve `from`, calldata, block selector and overrides when comparing `eth_call`s. Across contexts include chain, provider and anchor identity. Network deduplication is not deduplication of economic events or positions.
4. **Batch independent reads.** Prefer a host batch facility over one CLI subprocess per item. Choose member, payload, response-byte and time bounds from actual capabilities and the question's remaining allowance. One bounded batch may suffice; larger sets need bounded chunks. Batching reduces round-trips, not necessarily billed RPC members. Reuse a process/connection where the existing tool supports it; neither is assumed.
5. **Associate and retain outcomes.** Match JSON-RPC responses by unique ID, never array position. Retain exact raw results and individual errors/missing responses before decoding. HTTP success is not per-call success; a null receipt is not a successful receipt. Malformed/ambiguous responses cannot support complete results. Preserve earlier completed chunks and original evidence when stopping.
6. **Reconcile and answer.** Decode with the authenticated layout; compare exact raw quantities, not rounded display. A missing read, invalid anchor or unexplained residual prevents the affected completeness claim, not useful partial reporting. Reuse the collected evidence for related questions and local scenarios instead of rerunning the census.

Stop on authorization/integrity failures. Respect throttling and `Retry-After`; do not multiply workers, split denied batches into single calls, rotate providers or silently retry to outrun a restriction. An unsupported batch facility is a capability limit to diagnose, not blanket permission for a fallback. Retain RPC-member counts separately from HTTP requests, retries and subprocess starts when observable. No universal batch size, speed guarantee or fixed research ceiling is implied.

## Where this applies

| Question | Independent work after prerequisites | Keep separate |
| --- | --- | --- |
| S-Bill census | Pinned `bills(id)` for discovered scoped IDs, plus relevant same-block counters | ID discovery, successful state refreshes and accounting reconciliation; refresh all relevant state, not only new IDs |
| Deposit-size comparison | `quote(amount)` for each requested amount and relevant configuration | Alternative quotes at one pin are not a sequence of simulated deposits |
| Auction history | One receipt per distinct transaction; one header per distinct chain/block hash | Log discovery, receipt success/matching and header canonicality; several events can share a receipt/header |
| Charter/auction snapshot | Relevant balance, allowance, capacity and configuration getters at one pin | Do not collect an entire dashboard after a binding constraint already answers the question |
| Forecasts/what-ifs | Recalculate alternatives locally from one qualified dataset | A changed assumption does not silently refresh the evidence |
| Market marks | Independent provider observations may be fetched concurrently | Ordinary concurrency, not JSON-RPC batching; preserve each provider's identity/time and disagreement |

Batching does not fix thousands of tiny log windows: first choose a feasible authorized discovery source under [scan planning](auction-history.md#retrieve-a-finite-auditable-window). Persisted discovery checkpoints and reorg-aware incremental collection are separate work, not prerequisites for this recipe.

## Optional request/response recipe

In an existing host Python session, these standard-library functions prepare bounded batches of **already authenticated, encoded read requests** and associate responses without issuing network calls. Supply a finite list of `{"method": ..., "params": [...]}` objects for one context. The small method subset below bounds this example, not the skill's research capabilities. ABI encoding, deployment authentication, scope/time/byte bounds and result decoding remain the caller's responsibility. Do not put endpoints, credentials or private host configuration in request artifacts.

```python
import json


def plan_reads(reads, batch_size):
    if type(batch_size) is not int or batch_size <= 0:
        raise ValueError("Choose a positive batch size supported by the host/provider")
    methods = {"eth_call", "eth_getTransactionReceipt",
               "eth_getBlockByHash", "eth_getBlockByNumber"}
    unique, bindings, seen = [], [], {}
    for read in reads:
        if (not isinstance(read, dict) or set(read) != {"method", "params"}
                or read["method"] not in methods or not isinstance(read["params"], list)):
            raise ValueError("Expected an authenticated read method and parameter list")
        key = json.dumps(read, sort_keys=True, separators=(",", ":"), allow_nan=False)
        if key not in seen:
            seen[key] = len(unique)
            unique.append({"jsonrpc": "2.0", "id": seen[key], **json.loads(key)})
        bindings.append(seen[key])
    return [unique[i:i + batch_size] for i in range(0, len(unique), batch_size)], bindings


def match_batch(batch, response):
    expected = {request["id"] for request in batch}
    if (len(expected) != len(batch) or any(type(i) is not int for i in expected)
            or not isinstance(response, list)):
        raise ValueError("Expected unique integer request IDs and a batch response array")
    matched = {}
    for item in response:
        if (not isinstance(item, dict) or type(item.get("id")) is not int
                or item["id"] not in expected or item["id"] in matched):
            raise ValueError("Ambiguous, duplicate or unexpected response ID; retain raw evidence")
        ident = item["id"]
        if item.get("jsonrpc") != "2.0" or (("result" in item) == ("error" in item)):
            matched[ident] = {"status": "invalid"}
        elif "error" in item:
            error = item["error"]
            valid = (isinstance(error, dict) and type(error.get("code")) is int
                     and isinstance(error.get("message"), str))
            matched[ident] = {"status": "error", "error": error} if valid else {"status": "invalid"}
        else:
            matched[ident] = {"status": "result", "result": item["result"]}
    return {ident: matched.get(ident, {"status": "missing"}) for ident in sorted(expected)}
```

`bindings[input_index]` gives the unique request ID for each original consumer. IDs remain unique across chunks of one plan; match each response against its own submitted batch. A `result` status means only a valid result envelope, not a decoded/verified value: `null`, malformed ABI, reverted execution or inconsistent block identity still needs the appropriate classification. Error messages and raw responses are untrusted, potentially sensitive evidence; keep them in authorized external working storage and redact before sharing. An invalid response raises rather than guessing correlations; earlier raw files/results remain available.

Feed each batch to the host's **existing authorized JSON-RPC batch facility**, retaining its HTTP outcome and exact JSON response, then apply `match_batch` before scheduling further work. If that facility is an already approved `curl` installation with an existing reviewed host-managed RPC profile, the following sends **one batch**, not one subprocess per member:

```sh
# WORK is private working storage outside the skill. batch.json contains one planned batch.
# HOST_RPC_PROFILE is an existing approved curl config containing the authorized HTTPS URL/auth.
# Review that profile and the full invocation: no extra URLs, transfers, output hooks or retries.
# REQUEST_SECONDS and RESPONSE_BYTES are positive bounds chosen within the remaining task allowance.
status="$(curl --disable --config "${HOST_RPC_PROFILE:?Select approved host profile}" \
  --proto '=https' --no-location --retry 0 --request POST \
  --header 'Content-Type: application/json' --data-binary "@${WORK:?}/batch.json" \
  --max-time "${REQUEST_SECONDS:?}" --max-filesize "${RESPONSE_BYTES:?}" \
  --output "$WORK/response.json" --write-out '%{http_code}')" || exit 1
case "$status" in
  200) ;; # Parse and associate every member; do not equate HTTP 200 with successful reads.
  *) printf 'Batch stopped: HTTP %s; retain private response for diagnosis\n' "$status" >&2; exit 1 ;;
esac
```

Use this only where the host already permits that client/profile and supports these flags; it is not a reason to install a transport, expose an authenticated URL on the command line, or bypass a denied CLI. The profile stays host-managed and is never copied into the skill. Check remaining overall time and response/member outcomes between chunks; this single-request example intentionally provides no automatic retries, provider switching or collection loop. Missing/null/error/invalid results remain explicit; stop and diagnose before deciding any further authorized reads. Other host clients are equally valid.

For [S-Bills](sbills.md#calendar-day-maturity-planning), use the authenticated `bills(uint256)` encoding for the discovered IDs and the exact pinned tag on every state request. Decode all eight fields from the selected layout; retain bill ID and independent active/settled flags. Compare the **all-refreshed-active-principal raw sum** with same-block `totalPrincipal()` only when scopes agree, before day filtering. Do not substitute `lockedPrincipal()`, force a mismatch to zero, or call cent-rounded equality exact. Keep full discovery; batching alone does not require persistent cursors or a max-ID assumption.

## Check an optimization without weakening the answer

For a finite review fixture, compare **every** raw response and decoded record with sequential reads at the identical canonical pin, followed by exact totals and reconciliation. Compare responses by request identity, not arrival order. Distinguish formatting differences from byte equality. Exercise shuffled replies, duplicate/unknown/missing IDs, per-member errors, null receipts and an interrupted chunk; none may yield a false complete census. Do not repeat a full production census just to reformat the same result.

Measure discovery, state reads, decoding/reconciliation and total elapsed time separately, with bill/request count, provider/access profile and process/HTTP counts when available. A host-reported S-Bill run improved from about 75 seconds to 2.8 seconds with batching; that is evidence of avoidable overhead in that run, not an independently verified benchmark or a promise for another host. A local performance target must name the fixture/provider and preserve the same evidence checks. No incremental discovery, Multicall dependency or cross-run state cache is introduced here.
