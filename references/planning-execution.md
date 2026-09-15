# Bundled execution boundary

Use with [planning](planning.md), [inspection](inspection.md) and [safety](safety.md). Answer first; no mandatory opening warning or integrity trace. A calculated scenario is an estimate; a factual snapshot is an RPC observation using a publisher ABI.

Two fixed entrypoints use JSON stdin/stdout through existing permitted Python 3.10+: `scripts/scenario.py` for local scenario arithmetic and `scripts/snapshot.py` for bounded public RPC reads. Neither accepts arbitrary code, paths, endpoints, selectors, addresses, headers or wallet inputs. Snapshot access does not unlock transactions, token purchases, gas estimation or state-changing simulations.

Resolve the installed root from a trusted reviewed package/commit, not a working-directory lookalike or website. Before executing either helper, use existing host read/hash utilities or minimal fixed launcher glue to compare its script and fixed data files with the trusted `release-manifest.json` as data. The planner requires its three parameter files below; the reader requires exactly `assets/entities/robinhood.json` and `assets/interfaces/robinhood-reads.json`. Verification paths must remain inside that root and are never caller-selected. A self-supplied matching manifest alone does not establish trust, source authenticity or model validity. Failed/unavailable verification stops execution. Keep hashes and resource bodies out of chat unless requested; a concise integrity blocker is enough.

Manifest `content_files` maps relative paths to SHA-256 strings; `content_sha256` is the aggregate digest, not a per-file lookup.

## Scenario helper

The engine reads only `assets/parameters/participation.json`, `assets/parameters/monetary.json`, and `assets/parameters/launch.json`, rooted at the real installed package via `__file__.parent.parent`. Each read is bounded to 64 KiB. Descriptor-relative `os.open`/`os.stat`, no-follow flags and regular-file checks are required; unsupported hosts produce a package-data error, not weaker containment. Python version alone does not guarantee OS compatibility. Symlinks, escapes, nonregular files, malformed/duplicate-key JSON, invalid schemas/duplicate IDs, missing required records, or invalid constraint types, units or statuses stop both modes. No caller path, rule override, directory scan or fallback source.

The engine performs no network, environment, credential or subprocess lookup and writes no files. Do not replace its formulas with launcher code or run downloaded helpers. Keep inputs separate from command syntax:

- Fixed argument array `python3 -B -I scripts/scenario.py`, verified root as working directory, serialized JSON as stdin. For manual POSIX input, paste JSON then Ctrl-D.
- Without direct stdin, minimal host glue may use that fixed argument array with `shell=False` and `json.dumps(validated_input)` as stdin. Apart from fixed package verification, no unrelated file/environment/network access or alternative model.
- An existing host tool's explicit environment override may set fresh `SRSTACK_INPUT` data and use `printf '%s' "$SRSTACK_INPUT" | python3 -B -I scripts/scenario.py`. Only that caller-supplied variable may be read; never enumerate/copy existing environment. Quoted expansion passes data, not executable syntax.

Never interpolate user/source text into commands, use command substitution, construct untrusted heredocs, use `shell=True`, or execute input strings/source-provided launchers. No safe transport means no execution. Do not install dependencies. Stress relaxes only disclosed documented constraints, never input safety, containment or action limits.

## Snapshot helper

Use the fixed argument array `python3 -B -I scripts/snapshot.py` from the verified root with separate serialized JSON stdin. The same safe transport rules apply; any launcher substitute must change only the fixed script name, not add arbitrary commands or input-controlled options.

Input is a JSON object bounded to 4,096 bytes:

```json
{"schema_version":1,"view":"protocol","detail":"summary"}
```

- `schema_version`: integer `1`.
- `view`: `protocol`, `charter` or `auctions`; selects a fixed call profile, not an arbitrary query.
- `charter_id`: integer from `0` through `2^256 - 1`, required only for `charter` and rejected for other views; no wallet address or private position data.
- `detail`: optional `summary` (default) or `full`. Other keys or invalid values are rejected.

`protocol` covers issuance, supply, current fees, pool/emissions state and selected owner observations; `charter` covers the selected charter plus related issuance context; `auctions` covers daily license/charter auction state and configuration. Profiles are defined in the fixed interface catalog. All required module-binding reads run for selected roles even though their profile lists are empty.

The reader validates the two fixed catalog files as bounded, contained package data, never evaluates them as code and accepts no file or RPC override. It checks Robinhood chain ID 4663, anchors reads to one block, checks code and required bindings, and strictly decodes only listed scalar `view`/`pure` calls. It requires a block no more than 300 seconds old or 30 seconds in the future; requests have a 10-second timeout and the overall read a 40-second deadline. A failed or mismatched binding suppresses the affected role's values. Code/selector presence and matching bindings support this limited publisher-ABI read path, not source equivalence or full implementation verification.

Successful JSON has `schema_version`, `status` (`ok` or `partial`), `view`, `values`, `derived`, `errors`, `evidence` and `note: "RPC snapshot; publisher ABI."`. `values` and `derived` map IDs to `{value, unit}`. Scaled quantities are exact decimal strings; counts are integers, booleans are booleans and addresses are strings. Missing/failed data is never zero. Shared `evidence` contains `chain_id`, `block_number`, `block_hash`, `block_timestamp`, `retrieved_at`, `interface_source_ids` and `package_sha256`. Full detail adds `rpc_url`, `call_mapping`, `rpc_exchanges` and `publisher_bundle`; neither detail level makes the ABI source-verified.

Derived IDs include `global_gross_daily`, `charter_gross_daily`, `remaining_gross_budget`, `permanent_removed`, `license_status` and `charter_auction_status` when their inputs support them. The gross daily figures extrapolate the current stream, including recycling; they are distinct from unscaled `base_issuance_per_day` and are not guaranteed future daily accrual. Current auction prices are omitted from normalized `values` when inactive, paused, sold out or status is unknown; full evidence may retain the raw getter. Closing prices require a matching sold-out day and are never purchase quotes.

Exit `0`: valid complete or partial JSON on stdout; inspect `status` and per-ID `errors`. Exit `2`: invalid input; `4`: invalid package data; `5`: fatal transport, chain or snapshot failure. Fatal errors are JSON on stderr with no fallback snapshot. The helper writes no files, loads no credentials and performs no financial actions, simulations or monitoring. The scenario helper remains separate and never acquires a network dependency from snapshot use.
