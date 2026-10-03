# Efficient evidence collection

Use the smallest sufficient reads, then reduce transport overhead—not evidence quality. This optional recipe uses existing authorized host tools; it adds no installed RPC client, provider, credential store or required workflow. A denied tool/action is not permission to reproduce it through another transport. Follow [execution](execution.md) and [safety](safety.md).

These are planning and evidence-quality recommendations, not extra approval gates for public research. Choose tools, batch sizes, staging, pacing, permitted sources and storage formats autonomously within existing host permissions. No ledger, saved response archive, benchmark, fixed call budget or prescribed gate order is required to answer an ordinary question. Evidence limits what can honestly be claimed, not what the agent may investigate. The existing [wallet boundary](safety.md#preparation-and-wallet-boundary) is unchanged.

## Plan once, collect in dependency stages

1. **Scope and pin.** Authenticate chain, targets and interfaces; resolve one block number/hash/header timestamp for dependent state. Generate its hexadecimal tag from the integer, not by transcription. A batch of `latest` calls is not a pinned snapshot. Reconcile canonicality when using numeric tags or changing providers.
2. **Resolve dependencies.** Discover IDs or transaction hashes before fetching their state/receipts; fetch a page cursor before its next page. Do not invent IDs to parallelize enumeration. Group only reads supported by the same authorized transport and evidence context.
3. **Deduplicate requests.** Within that context, identical method/complete-parameter requests need one fetch. Keep a mapping back to every consumer. Preserve `from`, calldata, block selector and overrides when comparing `eth_call`s. Across contexts include chain, provider and anchor identity. Network deduplication is not deduplication of economic events or positions.
4. **Batch independent reads.** Prefer a host batch facility over one CLI subprocess per item. Choose member, payload, response-byte and time bounds from actual capabilities and the question's remaining allowance. One bounded batch may suffice; larger sets need bounded chunks. Batching reduces round-trips, not necessarily billed RPC members. Reuse a process/connection where the existing tool supports it; neither is assumed.
5. **Associate and retain outcomes.** Match JSON-RPC responses by unique ID, never array position. Retain exact raw results and individual errors/missing responses before decoding. HTTP success is not per-call success; a null receipt is not a successful receipt. Malformed/ambiguous responses cannot support complete results. Preserve earlier completed chunks and original evidence when stopping.
6. **Reconcile and answer.** Decode with the authenticated layout; compare exact raw quantities, not rounded display. A missing read, invalid anchor or unexplained residual prevents the affected completeness claim, not useful partial reporting. Reuse the collected evidence for related questions and local scenarios instead of rerunning the census.

Stop on authorization/integrity failures. Respect throttling and `Retry-After`; do not multiply workers, split denied batches into single calls, rotate providers or silently retry to outrun a restriction. An unsupported batch facility is a capability limit to diagnose, not blanket permission for a fallback. Retain RPC-member counts separately from HTTP requests, retries and subprocess starts when observable. No universal batch size, speed guarantee or fixed research ceiling is implied.

Benchmarks share provider capacity with ordinary work: batched members, sequential comparison reads, retries and recaptures can all consume quota. Consider remaining questions when choosing concurrency and pacing, or run the comparison separately when capacity allows. Honor observed provider signals rather than inventing a universal delay. Later throttling does not by itself prove that batching caused it. A capability limit or exhausted provider budget need not end authorized research through a suitable independently permitted source; record the source change and reconcile anchors under [execution guidance](execution.md#rpc-provider-guidance).

## Where this applies

| Question | Independent work after prerequisites | Keep separate |
| --- | --- | --- |
| S-Bill census | Pinned `bills(id)` for discovered scoped IDs, plus relevant same-block counters | ID discovery, successful state refreshes and accounting reconciliation; refresh all relevant state, not only new IDs |
| Deposit-size comparison | `quote(amount)` for each requested amount and relevant configuration | Alternative quotes at one pin are not a sequence of simulated deposits |
| Auction history | One receipt per distinct transaction; one header per distinct chain/block hash | Log discovery, receipt success/matching and header canonicality; several events can share a receipt/header |
| Charter/auction snapshot | Relevant balance, allowance, capacity and configuration getters at one pin | Choose narrow staging or a broader batch according to the question and latency/member tradeoff |
| Forecasts/what-ifs | Recalculate alternatives locally from one qualified dataset | A changed assumption does not silently refresh the evidence |
| Market marks | Independent provider observations may be fetched concurrently | Ordinary concurrency, not JSON-RPC batching; preserve each provider's identity/time and disagreement |

Batching does not fix thousands of tiny log windows: first choose a feasible authorized discovery source under [scan planning](auction-history.md#retrieve-a-finite-auditable-window). Persisted discovery checkpoints and reorg-aware incremental collection are separate work, not prerequisites for this recipe.

For a narrow eligibility question, checking a likely binding constraint first can save members: for example, an authenticated quote above the available applicable budget can establish an affordability shortfall without fetching every other gate. Batching all relevant independent gates can instead save round trips and support a complete constraint snapshot. Neither approach is intrinsically a failure; choose based on the requested answer, known dependencies and provider costs. A proved negative gate supports a qualified negative answer; a positive eligibility claim still needs its applicable conditions established.

## Optional audit evidence and accounting

When a review calls for independently inspectable evidence, a convenient record per transport attempt contains:

| Evidence | Suggested contents |
| --- | --- |
| Identity/context | Run and attempt identity; purpose (normal collection, comparison baseline or recapture); credential-free provider label; chain and applicable block number/hash/time |
| Request | Exact RPC method, complete parameters and IDs for every submitted member; bindings back to repeated consumers when useful |
| Response | Original response body and HTTP/transport outcome, including partial bodies and errors; whether capture completed |
| Interpretation | ID-matched outcomes, decoded values with interface/units, and separate domain/coverage checks |
| Timing/accounting | Start time, elapsed duration, submitted member count, HTTP attempts and process-start observations; retry linkage to the earlier attempt |

This is an information checklist, not a required schema or storage service. Existing host traces, separate request/response files or another inspectable format are equally suitable. For an audited equivalence comparison, save both the batched and sequential raw results before relying on later historical recapture: providers can lose access to the pinned state. Per-member equality flags support “matched during the run,” not “both raw sides are retained for independent comparison.” Missing artifacts need not block useful answers; identify the narrower audit claim. Keep any retained artifacts in authorized private working storage outside the skill, omit credentials and private host configuration, and sanitize separately before sharing.

An append-only attempt ledger is one way to avoid stale counters; derive totals from the observations rather than manually updating a single aggregate. Each actual retry or recapture contributes its members and HTTP attempts to overall work, with its purpose and retry relationship also reported separately, not added twice. A deduplicated consumer is not another submitted member. A failed or interrupted HTTP attempt still counts; calls never sent do not. Record hidden client retries or counters as unknown when unobservable. Processes are counted when started, not once per request executed inside a reused process. Include discovery/index and market HTTP work separately from RPC, and separate benchmark overhead from normal collection. Timed stages can overlap or leave orchestration overhead; label that rather than forcing their rounded sum to equal wall-clock duration. None of this accounting requires extra network reads merely to fill a report.

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

After matching, apply the checks relevant to the claim: (1) transport/capture outcome, (2) JSON-RPC envelope/member outcome, (3) method-specific meaning, then (4) coverage and reconciliation. For receipts, `result: null` means unavailable or unresolved; a non-null receipt still needs successful status, the expected transaction/emitter/log identity and consistent block evidence before supporting a verified purchase. For `eth_call`, decode the authenticated ABI layout and units and check the applicable anchor. Existing host validators or inline checks are sufficient; no new validator module or always-run checklist is required. The matcher intentionally handles envelopes rather than certifying domain completeness.

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
