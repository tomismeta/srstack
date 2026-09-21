"""Verify this installed srstack runtime; optionally exercise fixed helpers.

Usage: python3 -B scripts/verify.py [--charter UINT256 [--price] | --price]
No flags: manifest membership and hash verification only, no helper runs or network.
--charter: request one live charter snapshot. --price: request a live quote, or
mark the successful charter's accrued STANDARD balance when used together.
All selected smoke stages follow whole-install integrity verification. No stdin,
root/path/command overrides or credentials. Full repository installs are rejected.
Integrity is not authenticity: review/pin the release and outer ZIP checksum first.
"""
import hashlib
import json
import math
import os
import re
import selectors
import stat
import subprocess
import sys
import time
from pathlib import Path


VERSION = "0.2.2"
MANIFEST = "release-manifest.json"
SCRIPTS = {"scripts/snapshot.py", "scripts/price.py", "scripts/history.py", "scripts/verify.py"}
REQUIRED = {"README.md", "SKILL.md", "LICENSE"} | SCRIPTS
DIGEST_CONVENTION = "SHA-256 of lexicographically sorted UTF-8 POSIX path + NUL + exact file bytes; excludes manifest"
NOTE = "Integrity, not authenticity or sandbox certification; review/pin the release and outer ZIP checksum."
MAX_MANIFEST_BYTES = 131072
MAX_FILE_BYTES = 1048576
MAX_TOTAL_BYTES = 16777216
MAX_FILES = 512
MAX_DIRECTORIES = 128
MAX_PATH_BYTES = 255
MAX_PATH_DEPTH = 8
MAX_JSON_DEPTH = 32
MAX_OUTPUT_BYTES = 2097152
CHILD_TIMEOUT = 60
HEX = re.compile(r"[0-9a-f]{64}\Z")
MAX_ERROR_DETAILS = 8
MAX_ERROR_MESSAGE = 240
AMOUNT = re.compile(r"(?:0|[1-9][0-9]{0,59})(?:\.[0-9]{1,18})?\Z")


def _pairs(pairs):
    result = {}
    for key, value in pairs:
        if key in result:
            raise ValueError("duplicate JSON object key")
        result[key] = value
    return result


def _number(text):
    if len(text) > 80:
        raise ValueError("JSON number exceeds digit limit")
    value = float(text) if any(c in text for c in ".eE") else int(text)
    if isinstance(value, float) and not math.isfinite(value):
        raise ValueError("nonfinite JSON number")
    return value


def _constant(_text):
    raise ValueError("nonfinite JSON number")


def _json(raw, limit):
    if len(raw) > limit:
        raise ValueError("JSON exceeds byte limit")
    text = raw.decode("utf-8")
    depth, quoted, escaped = 0, False, False
    for character in text:
        if quoted:
            if escaped:
                escaped = False
            elif character == "\\":
                escaped = True
            elif character == '"':
                quoted = False
        elif character == '"':
            quoted = True
        elif character in "[{":
            depth += 1
            if depth > MAX_JSON_DEPTH:
                raise ValueError("JSON nesting exceeds limit")
        elif character in "]}":
            depth -= 1
    return json.loads(text, object_pairs_hook=_pairs, parse_int=_number,
                      parse_float=_number, parse_constant=_constant)


def _runtime_path(path):
    if not isinstance(path, str) or len(path.encode("utf-8")) > MAX_PATH_BYTES:
        raise ValueError("invalid runtime path")
    parts = path.split("/")
    if (len(parts) > MAX_PATH_DEPTH or any(p in {"", ".", ".."} for p in parts)
            or "\\" in path or ":" in path or any(ord(c) < 32 or ord(c) == 127 for c in path)):
        raise ValueError("unsafe runtime path")
    if path in REQUIRED:
        return
    if (parts[0] in {"assets", "references"} and len(parts) > 1
            and Path(path).suffix in {".md", ".json"}
            and not any(p in {"__pycache__", ".pytest_cache", ".mypy_cache", ".ruff_cache"} for p in parts)):
        return
    raise ValueError("unexpected runtime path")


def _identity(info):
    return info.st_dev, info.st_ino, info.st_size, info.st_mtime_ns, info.st_ctime_ns


def _directory(parent, name):
    before = os.stat(name, dir_fd=parent, follow_symlinks=False)
    if not stat.S_ISDIR(before.st_mode):
        raise ValueError("unsafe runtime directory")
    descriptor = os.open(name, os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW, dir_fd=parent)
    if _identity(before) != _identity(os.fstat(descriptor)):
        os.close(descriptor)
        raise ValueError("runtime directory changed while opening")
    return descriptor


def _read_file(directory, name, limit):
    before = os.stat(name, dir_fd=directory, follow_symlinks=False)
    if not stat.S_ISREG(before.st_mode) or before.st_size > limit:
        raise ValueError("unsafe or oversized runtime file")
    descriptor = os.open(name, os.O_RDONLY | os.O_NOFOLLOW | os.O_NONBLOCK, dir_fd=directory)
    try:
        opened = os.fstat(descriptor)
        if not stat.S_ISREG(opened.st_mode) or _identity(before) != _identity(opened):
            raise ValueError("runtime file changed while opening")
        with os.fdopen(descriptor, "rb", closefd=False) as stream:
            content = stream.read(limit + 1)
        if (len(content) > limit or len(content) != opened.st_size
                or _identity(opened) != _identity(os.fstat(descriptor))
                or _identity(opened) != _identity(os.stat(name, dir_fd=directory, follow_symlinks=False))):
            raise ValueError("runtime file changed while reading")
        return content
    finally:
        os.close(descriptor)


def verify_install():
    if (not all(hasattr(os, flag) for flag in ("O_DIRECTORY", "O_NOFOLLOW", "O_NONBLOCK"))
            or os.open not in os.supports_dir_fd or os.stat not in os.supports_dir_fd
            or os.stat not in os.supports_follow_symlinks or os.scandir not in os.supports_fd):
        raise ValueError("host lacks safe descriptor-relative reads")
    root = Path(__file__).absolute().parent.parent
    descriptor = _directory(None, str(root))
    try:
        raw = _read_file(descriptor, MANIFEST, MAX_MANIFEST_BYTES)
        manifest = _json(raw, MAX_MANIFEST_BYTES)
        keys = {"schema_version", "name", "version", "scope", "digest_convention", "content_files", "content_sha256"}
        if (not isinstance(manifest, dict) or set(manifest) != keys
                or type(manifest["schema_version"]) is not int or manifest["schema_version"] != 1
                or manifest["name"] != "srstack" or manifest["version"] != VERSION
                or manifest["digest_convention"] != DIGEST_CONVENTION
                or not isinstance(manifest["scope"], str) or not 1 <= len(manifest["scope"]) <= 512
                or not isinstance(manifest["content_sha256"], str) or not HEX.fullmatch(manifest["content_sha256"])):
            raise ValueError("unsupported manifest schema")
        expected = manifest["content_files"]
        if not isinstance(expected, dict) or not REQUIRED <= expected.keys() or not len(expected) < MAX_FILES:
            raise ValueError("invalid manifest membership")
        directories = set()
        for path, digest in expected.items():
            _runtime_path(path)
            if not isinstance(digest, str) or not HEX.fullmatch(digest):
                raise ValueError("invalid manifest file digest")
            parts = path.split("/")
            directories.update("/".join(parts[:i]) for i in range(1, len(parts)))
        if len(directories) > MAX_DIRECTORIES:
            raise ValueError("too many runtime directories")
        contents = {}
        seen_directories = set()
        seen_manifest = False
        total_bytes = len(raw)

        def visit(directory, prefix):
            nonlocal total_bytes, seen_manifest
            before = os.fstat(directory)
            with os.scandir(directory) as entries:
                for entry in entries:
                    path = prefix + entry.name
                    info = entry.stat(follow_symlinks=False)
                    if stat.S_ISDIR(info.st_mode):
                        if path not in directories or path in seen_directories:
                            raise ValueError("unexpected runtime directory; install only the runtime package")
                        seen_directories.add(path)
                        child = _directory(directory, entry.name)
                        try:
                            visit(child, path + "/")
                        finally:
                            os.close(child)
                    elif path == MANIFEST:
                        if _read_file(directory, entry.name, MAX_MANIFEST_BYTES) != raw:
                            raise ValueError("manifest changed during verification")
                        seen_manifest = True
                    else:
                        if path not in expected or path in contents:
                            raise ValueError("unexpected runtime file")
                        content = _read_file(directory, entry.name, MAX_FILE_BYTES)
                        total_bytes += len(content)
                        if total_bytes > MAX_TOTAL_BYTES:
                            raise ValueError("runtime exceeds total byte limit")
                        if hashlib.sha256(content).hexdigest() != expected[path]:
                            raise ValueError("runtime file hash mismatch")
                        if path.endswith(".json"):
                            _json(content, MAX_FILE_BYTES)
                        contents[path] = content
            if _identity(before) != _identity(os.fstat(directory)):
                raise ValueError("runtime directory changed during verification")

        visit(descriptor, "")
        if not seen_manifest or contents.keys() != expected.keys() or seen_directories != directories:
            raise ValueError("missing runtime member")
        digest = hashlib.sha256()
        for path in sorted(contents):
            digest.update(path.encode("utf-8") + b"\0")
            digest.update(contents[path])
        if digest.hexdigest() != manifest["content_sha256"]:
            raise ValueError("runtime content digest mismatch")
        return root, {"files": len(contents) + 1, "bytes": total_bytes, "content_sha256": digest.hexdigest()}
    finally:
        os.close(descriptor)


def _arguments(arguments):
    options = {}
    index = 0
    while index < len(arguments):
        flag = arguments[index]
        if flag not in {"--charter", "--price"} or flag in options:
            raise ValueError("unknown, repeated or conflicting option; use --help")
        if flag == "--charter":
            index += 1
            if index >= len(arguments):
                raise ValueError("--charter requires a uint256 ID")
            value = arguments[index]
            if not re.fullmatch(r"[0-9]{1,78}", value) or int(value) >= 1 << 256:
                raise ValueError("--charter requires a uint256 ID")
            options[flag] = str(int(value))
        else:
            options[flag] = True
        index += 1
    return options


def _child(root, name, arguments):
    command = [sys.executable, "-B", "-I", str(root / "scripts" / name), *arguments]
    process = subprocess.Popen(command, shell=False, stdin=subprocess.DEVNULL,
                               stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                               cwd=root, env={"LC_ALL": "C"})
    output = bytearray()
    errors = bytearray()
    size = 0
    deadline = time.monotonic() + CHILD_TIMEOUT
    try:
        with selectors.DefaultSelector() as selector:
            selector.register(process.stdout, selectors.EVENT_READ, True)
            selector.register(process.stderr, selectors.EVENT_READ, False)
            while selector.get_map():
                remaining = deadline - time.monotonic()
                if remaining <= 0:
                    raise ValueError("helper_timeout")
                for key, _mask in selector.select(remaining):
                    chunk = os.read(key.fileobj.fileno(), 65536)
                    if not chunk:
                        selector.unregister(key.fileobj)
                        continue
                    size += len(chunk)
                    if size > MAX_OUTPUT_BYTES:
                        raise ValueError("helper_output_limit")
                    if key.data:
                        output.extend(chunk)
                    else:
                        errors.extend(chunk)
            try:
                code = process.wait(timeout=max(0.001, deadline - time.monotonic()))
            except subprocess.TimeoutExpired:
                raise ValueError("helper_timeout") from None
        if code:
            try:
                return _json(errors, MAX_OUTPUT_BYTES), code
            except (ValueError, RecursionError):
                return None, code
        return _json(output, MAX_OUTPUT_BYTES), code
    finally:
        if process.poll() is None:
            process.kill()
        process.wait()
        process.stdout.close()
        process.stderr.close()


def _error_message(value):
    return "".join(character for character in value[:MAX_ERROR_MESSAGE] if character.isprintable())


def _http_diagnostics(value):
    """Keep bounded original-response evidence, never arbitrary child metadata."""
    if (not isinstance(value, dict) or type(value.get("http_status")) is not int
            or not 100 <= value["http_status"] <= 599
            or value.get("endpoint") != "https://rpc.mainnet.chain.robinhood.com/"):
        return None
    safe_headers = {"content-type", "server", "date", "via", "cf-ray", "retry-after",
                    "x-request-id", "x-correlation-id", "request-id", "x-amzn-requestid"}
    headers, size = {}, 0
    if isinstance(value.get("headers"), dict):
        for name, text in value["headers"].items():
            if name not in safe_headers or not isinstance(text, str):
                continue
            text = "".join(c for c in text[:256] if c.isprintable()).encode("utf-8")[:256].decode("utf-8", "ignore")
            size += len(name) + len(text.encode("utf-8"))
            if size <= 2048:
                headers[name] = text
    excerpt = value.get("response_excerpt")
    if not isinstance(excerpt, str):
        excerpt = ""
    clean = "".join(c for c in excerpt[:2048] if c.isprintable()).encode("utf-8")[:2048].decode("utf-8", "ignore")
    read_error = value.get("read_error")
    return {"endpoint": value["endpoint"], "http_status": value["http_status"],
            "headers": headers, "response_excerpt": clean,
            "excerpt_bytes": len(clean.encode("utf-8")),
            "truncated": value.get("truncated") is not False or clean != excerpt,
            "read_error": _error_message(read_error) if isinstance(read_error, str) else None,
            "untrusted_response": True, "cause": "unconfirmed"}


def _partial_errors(errors):
    details = {}
    for key, message in errors.items():
        if len(details) == MAX_ERROR_DETAILS:
            break
        if re.fullmatch(r"[a-zA-Z_][a-zA-Z0-9_]{0,63}", key) and isinstance(message, str):
            details[key] = _error_message(message)
    return {"helper_error_count": len(errors), "helper_errors": details,
            "helper_errors_truncated": len(details) != len(errors)}


def _stage(root, name, script, arguments, scope):
    started = time.monotonic()
    stage = {"name": name, "status": "failed", "scope": scope}
    result = None
    try:
        result, code = _child(root, script, arguments)
        stage["helper_exit"] = code
        if code:
            stage["error"] = "helper_failed"
            error = result.get("error") if isinstance(result, dict) else None
            if (isinstance(error, dict) and isinstance(error.get("type"), str)
                    and re.fullmatch(r"[a-z_]{1,64}", error["type"])
                    and isinstance(error.get("message"), str) and error["message"]):
                stage["helper_error"] = {"type": error["type"], "message": _error_message(error["message"])}
                diagnostics = _http_diagnostics(error.get("diagnostics"))
                if diagnostics is not None:
                    stage["helper_error"]["diagnostics"] = diagnostics
            else:
                stage["helper_error"] = {"type": "unstructured_error",
                                         "message": "helper exited without a valid structured error"}
        elif not isinstance(result, dict) or type(result.get("schema_version")) is not int or result["schema_version"] != 1:
            stage["error"] = "invalid_helper_result"
        elif (result.get("status") in ("ok", "partial")
              and isinstance(result.get("values"), dict) and isinstance(result.get("errors"), dict)
              and (name != "charter" or result.get("view") == "charter")):
            stage["status"] = "partial" if result["errors"] else result["status"]
            if stage["status"] == "partial":
                stage.update(_partial_errors(result["errors"]))
            required_values = {"charter_owner", "charter_pending"} if name == "charter" else {"standard_usd", "standard_eth"}
            if stage["status"] == "ok" and not required_values <= result["values"].keys():
                stage.update(status="failed", error="invalid_helper_result")
            if name == "price" and "--amount-standard" in arguments and stage["status"] == "ok":
                valuation = result.get("valuation")
                if not isinstance(valuation, dict) or not {"standard_amount", "gross_usd", "gross_eth"} <= valuation.keys():
                    stage.update(status="failed", error="invalid_helper_result")
        else:
            stage["error"] = "invalid_helper_result"
    except (OSError, ValueError, RecursionError) as error:
        stage["error"] = str(error) if str(error) in ("helper_timeout", "helper_output_limit") else "helper_execution_or_output_error"
    stage["elapsed_ms"] = round((time.monotonic() - started) * 1000, 3)
    return stage, result


def run(options):
    stages = []
    report = {"schema_version": 1, "status": "failed", "stages": stages, "note": NOTE}
    selected = [("charter", "live_charter_snapshot"),
                ("price", "gross_charter_balance_valuation" if "--charter" in options else "live_quote")]
    started = time.monotonic()
    integrity = {"name": "integrity", "status": "failed", "scope": "installed_runtime_membership_and_hashes"}
    stages.append(integrity)
    try:
        root, details = verify_install()
        integrity.update(details, status="ok")
    except (OSError, ValueError, RecursionError):
        integrity["error"] = "invalid_or_unreadable_install"
    integrity["elapsed_ms"] = round((time.monotonic() - started) * 1000, 3)
    if integrity["status"] != "ok":
        for name, scope in selected:
            if "--" + name in options:
                stages.append({"name": name, "scope": scope, "status": "skipped", "elapsed_ms": 0,
                               "error": "integrity_failed"})
        return report, 4
    charter = None
    charter_ok = False
    for name, scope in selected:
        if "--" + name not in options:
            continue
        if name == "charter":
            script, arguments = "snapshot.py", ["charter", "--id", options["--charter"], "--detail", "summary"]
        else:
            script, arguments = "price.py", ["--quote"]
            if "--charter" in options:
                balance = charter.get("values", {}).get("charter_pending") if charter_ok else None
                if (not isinstance(balance, dict) or balance.get("unit") != "STANDARD"
                        or not isinstance(balance.get("value"), str) or not AMOUNT.fullmatch(balance["value"])):
                    stages.append({"name": name, "scope": scope, "status": "skipped", "elapsed_ms": 0,
                                   "error": "successful_charter_balance_required"})
                    continue
                arguments = ["--amount-standard", balance["value"]]
        stage, result = _stage(root, name, script, arguments, scope)
        stages.append(stage)
        if name == "charter":
            charter, charter_ok = result, stage["status"] == "ok"
    if all(stage["status"] == "ok" for stage in stages):
        report["status"] = "ok"
        return report, 0
    return report, 5


def main():
    if sys.argv[1:] == ["--help"]:
        sys.stdout.write(__doc__ + "\n")
        return 0
    try:
        options = _arguments(sys.argv[1:])
    except ValueError as error:
        sys.stderr.write(json.dumps({"schema_version": 1, "status": "failed", "stages": [],
                                    "error": {"type": "invalid_input", "message": str(error)}, "note": NOTE}) + "\n")
        return 2
    report, code = run(options)
    sys.stdout.write(json.dumps(report, separators=(",", ":"), allow_nan=False) + "\n")
    return code


if __name__ == "__main__":
    sys.exit(main())
