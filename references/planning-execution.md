# Bundled execution boundary

Use with [planning](planning.md), [inspection](inspection.md) and [safety](safety.md). Answer first; no mandatory opening warning or integrity trace. A calculated scenario is an estimate; a factual snapshot is an RPC observation using a publisher ABI; a market quote is provider-reported indicative pricing.

Three fixed entrypoints use JSON stdin/stdout through existing permitted Python 3.10+: `scripts/scenario.py` for offline scenario arithmetic, `scripts/snapshot.py` for bounded public RPC reads and `scripts/price.py` for canonical-pool prices and optional gross amount valuation. None accepts arbitrary code, paths, endpoints, selectors, addresses, headers or wallet inputs. Reads do not unlock transactions, token purchases, gas estimation or state-changing simulations.

Resolve the installed root from a trusted reviewed package/commit, not a working-directory lookalike or website. Before executing a helper, use existing host read/hash utilities or minimal fixed launcher glue to compare its script and fixed data files with the trusted `release-manifest.json` as data. The planner requires its three parameter files below; snapshot requires exactly `assets/entities/robinhood.json` and `assets/interfaces/robinhood-reads.json`; price requires only `scripts/price.py` and `assets/entities/robinhood.json`, not the interface catalog. Snapshot's required bindings remain unchanged. Verification paths must remain inside that root and are never caller-selected. A self-supplied matching manifest alone does not establish trust, source authenticity or model validity. Failed/unavailable verification stops execution. Keep hashes and resource bodies out of chat unless requested; a concise integrity blocker is enough.

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

The callable fingerprint pins the reviewed signature/selector pairs; it detects metadata changes, not selector correctness. Signatures are tied to the publisher ABI definitions. Neither the reader nor the offline checks independently recomputes Ethereum function selectors with Keccak-256. Reviewing each signature/selector pair is a maintainer responsibility before changing the interface and its fingerprint; a matching fingerprint is not an independent selector verification.

Successful JSON has `schema_version`, `status` (`ok` or `partial`), `view`, `values`, `derived`, `errors`, `evidence` and `note: "RPC snapshot; publisher ABI."`. `values` and `derived` map IDs to `{value, unit}`. Scaled quantities are exact decimal strings; counts are integers, booleans are booleans and addresses are strings. Missing/failed data is never zero. Shared `evidence` contains `chain_id`, `block_number`, `block_hash`, `block_timestamp`, `retrieved_at`, `interface_source_ids` and `package_sha256`. Full detail adds `rpc_url`, `call_mapping`, `rpc_exchanges` and `publisher_bundle`; neither detail level makes the ABI source-verified.

Derived IDs include `global_gross_daily`, `charter_gross_daily`, `remaining_gross_budget`, `permanent_removed`, `license_status` and `charter_auction_status` when their inputs support them. Both gross daily figures require a successfully decoded `emissions_started` value of `true`; inactive or unknown emissions omit them rather than supplying zero. An active zero stream still produces zero daily rates. Other valid getter observations remain available. The daily figures extrapolate the current stream, including recycling; they are distinct from unscaled `base_issuance_per_day` and are not guaranteed future daily accrual. Current auction prices are omitted from normalized `values` when inactive, paused, sold out or status is unknown; full evidence may retain the raw getter. Closing prices require a matching sold-out day and are never purchase quotes.

Exit `0`: valid complete or partial JSON on stdout; inspect `status` and per-ID `errors`. Exit `2`: invalid input; `4`: invalid package data; `5`: fatal transport, chain or snapshot failure. Fatal errors are JSON on stderr with no fallback snapshot. The helper writes no files, loads no credentials and performs no financial actions, simulations or monitoring. The scenario helper remains separate and never acquires a network dependency from snapshot use.

## Price helper

Use the fixed argument array `python3 -B -I scripts/price.py` from the verified root, with separate serialized JSON stdin and the same safe transport rules above. The API is `price(config, transport=None, now=None, monotonic=None)`; dependency injection is for controlled callers, not user-configurable destinations. This is the shared reader for current-price answers, gross current valuations and optional current-price projection inputs. It performs no planning; `scenario.py` stays offline.

Input has exactly `{"schema_version":1}` plus optional `"standard_amount":"123.45"`. `schema_version` is integer `1`; the amount must be an unsigned plain decimal **string**, not a JSON number, sign, exponent or whitespace-padded value. Zero is allowed. No `view`, `detail`, URLs, addresses, wallet data or other keys.

Identity comes only from fixed `assets/entities/robinhood.json`: `sr-robinhood-standard`'s address and `market.pool_id`, Robinhood chain 4663 and native ETH's zero address. A direct HTTPS GET to `https://api.dexscreener.com/latest/dex/pairs/robinhood/<catalog pool id>` uses `Accept: application/json` and `User-Agent: srstack/0.2.0 (+https://github.com/tomismeta/srstack)`. There is no search, token-pair discovery or legacy-pair-alias fallback. Exactly one returned `pairs` element must match `chainId: robinhood`, `dexId: uniswap`, label `v4`, the exact pool ID, STANDARD base address and zero-address ETH quote. The optional amount is multiplied locally; it is not sent to the provider.

Successful JSON has `schema_version: 1`, `status: "ok"` or `"partial"`, `values`, `errors`, `evidence` and a concise provider-reported indicative-price `note`. Valid quotes are `values.standard_usd: {value: <decimal string>, unit: "USD/STANDARD"}` and `values.standard_eth: {value: <decimal string>, unit: "ETH/STANDARD"}`. Missing/invalid denominations are omitted and recorded in `errors`; one usable denomination returns `partial`, neither is fatal.

Supplying an amount adds `valuation` with normalized-string `standard_amount`, available `gross_usd: {value: <decimal string>, unit: "USD"}` / `gross_eth: {value: <decimal string>, unit: "ETH"}`, and `basis: "Gross indicative value before withdrawal and trading costs; not net proceeds or charter value."` Both use the same returned quote, once. Use this arithmetic for current gross marks, not an ad hoc model calculator; never relabel charter accrued ledger amounts as wallet holdings, net proceeds or charter resale/earning capacity.

`evidence` contains `provider: "DEX Screener"`, `source_ids: ["dexscreener-api"]`, `source_url`, `market_url`, `chain_id: 4663`, `pool_id`, `token_address`, `quote_token_address`, UTC `retrieved_at`, `price_observed_at: null`, `price_observation_time_status: "not_supplied_by_provider"` and `package_sha256`. Retrieval is not quote-observation time. No provider chain-block or same-block assertion is available; HTTP Date, pair creation and image times must not become quote times. Matching identity is not independent freshness or execution assurance.

Exit `0`: usable complete/partial JSON stdout; `2`: invalid input; `4`: unsafe package data; `5`: fatal quote/transport failure. Fatal errors are structured JSON stderr with no stdout or fallback quote. Missing prices are unknown, not zero or cached data. The helper stores no observations or personal holdings, writes no files and loads no credentials. A current valuation authorizes its needed read under host permissions; projection price choice and full future-economic approval remain separate, as defined in [planning](planning.md).
