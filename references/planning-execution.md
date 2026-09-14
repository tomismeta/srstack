# Planner execution boundary

Use with [planning](planning.md) and [safety](safety.md). All planning answers lead with the exact SKILL warning, including blocked or unexecuted requests.

Only the packaged `scripts/scenario.py` may calculate plans, using explicit JSON stdin and JSON stdout through existing permitted Python 3.10+. This is arithmetic, not contract execution. No arbitrary code, paths, destinations, ABI/address or wallet inputs.

Resolve the installed root from the trusted reviewed package/commit, not a working-directory lookalike or website. Use existing host read/hash utilities, or minimal fixed launcher glue, to compare the script and three fixed parameter files with `release-manifest.json` as data. Return only the integrity result, not manifest/script/resource-body dumps. Verification paths are fixed and contained, never caller-selected. A self-supplied matching manifest alone does not establish trust, source authenticity or model validity. Failed/unavailable verification stops execution.

Manifest `content_files` maps relative paths to SHA-256 strings; `content_sha256` is the aggregate digest, not a per-file lookup.

The engine reads only `assets/parameters/participation.json`, `assets/parameters/monetary.json`, and `assets/parameters/launch.json`, rooted at the real installed package via `__file__.parent.parent`. Each read is bounded to 64 KiB. Descriptor-relative `os.open`/`os.stat`, no-follow flags and regular-file checks are required; unsupported hosts produce a package-data error, not weaker containment. Python version alone does not guarantee OS compatibility. Symlinks, escapes, nonregular files, malformed/duplicate-key JSON, invalid schemas/duplicate IDs, missing required records, or invalid constraint types, units or statuses stop both modes. No caller path, rule override, directory scan or fallback source.

The engine performs no network, environment, credential or subprocess lookup and writes no files. Do not replace its formulas with launcher code or run downloaded helpers. Keep inputs separate from command syntax:

- Fixed argument array `python3 -B -I scripts/scenario.py`, verified root as working directory, serialized JSON as stdin. For manual POSIX input, paste JSON then Ctrl-D.
- Without direct stdin, minimal host glue may use that fixed argument array with `shell=False` and `json.dumps(validated_input)` as stdin. Apart from fixed package verification, no unrelated file/environment/network access or alternative model.
- An existing host tool's explicit environment override may set fresh `SRSTACK_INPUT` data and use `printf '%s' "$SRSTACK_INPUT" | python3 -B -I scripts/scenario.py`. Only that caller-supplied variable may be read; never enumerate/copy existing environment. Quoted expansion passes data, not executable syntax.

Never interpolate user/source text into commands, use command substitution, construct untrusted heredocs, use `shell=True`, or execute input strings/source-provided launchers. No safe transport means no execution. Do not install dependencies. Stress relaxes only disclosed documented constraints, never input safety, containment or action limits.
