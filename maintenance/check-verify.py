"""Offline regressions for installed integrity and bounded fixed smoke execution."""
import contextlib
import importlib.util
import io
import json
import os
import subprocess
import sys
import tempfile
import time
import unittest
from pathlib import Path
from unittest.mock import patch
from urllib.parse import urlsplit


ROOT = Path(__file__).resolve().parents[1]


def load_module(path, name):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    with patch.object(sys, "dont_write_bytecode", True):
        spec.loader.exec_module(module)
    return module


class VerifyChecks(unittest.TestCase):
    def setUp(self):
        environment = patch.dict(os.environ, {}, clear=True)
        environment.start()
        self.addCleanup(environment.stop)
        temporary = tempfile.TemporaryDirectory(prefix="srstack-verify-check-")
        self.addCleanup(temporary.cleanup)
        self.work = Path(temporary.name).resolve()
        self.root = self.work / "installed"
        self.root.mkdir()
        self.package = load_module(ROOT / "maintenance/package.py", "verify_package_fixture")
        self.files = self.package.package_files()
        for name, content in self.files.items():
            target = self.root / name
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_bytes(content)
        self.refresh_manifest()
        self.verify = load_module(self.root / "scripts/verify.py", "installed_verifier_fixture")

    def refresh_manifest(self):
        files = {path.relative_to(self.root).as_posix(): path.read_bytes()
                 for path in self.root.rglob("*") if path.is_file()}
        self.manifest = self.package.make_manifest(files)
        self.save_manifest()

    def save_manifest(self):
        (self.root / "release-manifest.json").write_text(json.dumps(self.manifest))

    def invoke(self, *arguments):
        return subprocess.run(
            [sys.executable, "-B", "-I", str(self.root / "scripts/verify.py"), *arguments],
            stdin=subprocess.DEVNULL, stdout=subprocess.PIPE, stderr=subprocess.PIPE, timeout=70,
        )

    def helper(self, name, content):
        (self.root / "scripts" / name).write_text(content)
        self.refresh_manifest()

    def helper_result(self, name, result):
        self.helper(name, "import json\nprint(json.dumps(" + repr(result) + "))\n")

    def assert_integrity_failure(self):
        with patch.object(self.verify.subprocess, "Popen", side_effect=AssertionError("must not execute a helper")):
            report, code = self.verify.run({"--charter": "1", "--price": True})
        self.assertEqual(4, code)
        self.assertEqual("failed", report["status"])
        self.assertEqual(["failed", "skipped", "skipped"], [stage["status"] for stage in report["stages"]])

    def test_default_checks_all_content_without_child_or_writes(self):
        before = {path.relative_to(self.root).as_posix(): path.read_bytes()
                  for path in self.root.rglob("*") if path.is_file()}
        with patch.object(self.verify.subprocess, "Popen", side_effect=AssertionError("default must not launch helpers")):
            report, code = self.verify.run({})
        self.assertEqual(0, code)
        self.assertEqual("ok", report["status"])
        self.assertEqual(["integrity"], [stage["name"] for stage in report["stages"]])
        self.assertEqual(self.manifest["content_sha256"], report["stages"][0]["content_sha256"])
        self.assertEqual(len(before), report["stages"][0]["files"])
        result = self.invoke()
        self.assertEqual(0, result.returncode, result.stderr.decode() + result.stdout.decode())
        self.assertEqual("ok", json.loads(result.stdout)["status"])
        self.assertEqual(before, {path.relative_to(self.root).as_posix(): path.read_bytes()
                                  for path in self.root.rglob("*") if path.is_file()})

    def test_tampered_unrelated_reference_prevents_live_helpers(self):
        reference = next((self.root / "references").glob("*.md"))
        reference.write_bytes(reference.read_bytes() + b"\ntampered\n")
        self.assert_integrity_failure()

    def test_missing_member_prevents_smoke(self):
        (self.root / "assets/sources.json").unlink()
        self.assert_integrity_failure()

    def test_unexpected_repository_file_and_empty_directory_are_rejected(self):
        for name, directory in (("maintenance", True), (".git", True), ("scripts/__pycache__", True),
                                (".DS_Store", False), ("arbitrary.py", False)):
            with self.subTest(name=name):
                target = self.root / name
                target.mkdir() if directory else target.write_text("unexpected")
                self.assert_integrity_failure()
                target.rmdir() if directory else target.unlink()

    def test_symlink_file_directory_and_manifest_are_rejected(self):
        for name in ("README.md", "assets", "release-manifest.json"):
            with self.subTest(name=name):
                target = self.root / name
                outside = self.work / "outside"
                target.rename(outside)
                target.symlink_to(outside, target_is_directory=outside.is_dir())
                self.assert_integrity_failure()
                target.unlink()
                outside.rename(target)

    def test_root_symlink_is_rejected(self):
        linked = self.work / "linked"
        linked.symlink_to(self.root, target_is_directory=True)
        with patch.object(self.verify, "__file__", str(linked / "scripts/verify.py")):
            self.assert_integrity_failure()

    def test_fifo_never_blocks(self):
        target = self.root / "README.md"
        target.unlink()
        os.mkfifo(target)
        result = self.invoke()
        self.assertEqual(4, result.returncode)
        self.assertEqual("failed", json.loads(result.stdout)["stages"][0]["status"])

    def test_manifest_traversal_absolute_unknown_and_overdeep_members_fail(self):
        for name in ("../escape.json", "/tmp/escape.json", "assets/../escape.json", "assets\\escape.json",
                     "scripts/extra.py", "assets/" + "a/" * 7 + "x.json", "assets/" + "x" * 256 + ".json"):
            with self.subTest(name=name):
                self.manifest["content_files"][name] = "0" * 64
                self.save_manifest()
                self.assert_integrity_failure()
                del self.manifest["content_files"][name]

    def test_manifest_cannot_omit_required_helper_or_change_aggregate_digest(self):
        del self.manifest["content_files"]["scripts/price.py"]
        self.save_manifest()
        self.assert_integrity_failure()
        self.refresh_manifest()
        self.manifest["content_sha256"] = "0" * 64
        self.save_manifest()
        self.assert_integrity_failure()

    def test_duplicate_keys_and_depth_are_rejected_even_with_matching_hashes(self):
        for content in (b'{"key":1,"key":2}', b"[" * 33 + b"0" + b"]" * 33, b'{"n":NaN}',
                        b'{"n":' + b"9" * 81 + b"}"):
            with self.subTest(content=content[:30]):
                (self.root / "assets/sources.json").write_bytes(content)
                self.refresh_manifest()
                self.assert_integrity_failure()
        (self.root / "assets/sources.json").write_bytes(self.files["assets/sources.json"])
        self.refresh_manifest()
        content = json.dumps(self.manifest)
        (self.root / "release-manifest.json").write_text(content[:-1] + ',"name":"srstack"}')
        self.assert_integrity_failure()

    def test_file_manifest_total_and_membership_bounds_fail_closed(self):
        for constant, limit in (("MAX_FILE_BYTES", 1), ("MAX_MANIFEST_BYTES", 1), ("MAX_TOTAL_BYTES", 1),
                                ("MAX_FILES", len(self.manifest["content_files"])), ("MAX_DIRECTORIES", 1)):
            with self.subTest(constant=constant), patch.object(self.verify, constant, limit):
                self.assert_integrity_failure()

    def test_unsupported_host_fails_before_any_child(self):
        with patch.object(self.verify.os, "supports_dir_fd", set()):
            self.assert_integrity_failure()

    def test_file_replacement_between_stat_and_open_is_rejected(self):
        original_open = self.verify.os.open
        replaced = False

        def racing_open(path, flags, *arguments, **keywords):
            nonlocal replaced
            if path == "README.md" and not replaced:
                replaced = True
                target = self.root / "README.md"
                target.rename(self.work / "old-readme")
                target.write_bytes(self.files["README.md"])
            return original_open(path, flags, *arguments, **keywords)

        # Keep the host-capability check independent of the instrumented open.
        supported = self.verify.os.supports_dir_fd | {racing_open}
        with patch.object(self.verify.os, "open", racing_open), patch.object(self.verify.os, "supports_dir_fd", supported):
            self.assert_integrity_failure()
        self.assertTrue(replaced)

    def test_removed_offline_and_invalid_flags_fail_before_integrity(self):
        cases = [("--offline",), ("--offline", "--price"), ("--charter", "1", "--offline"), ("--off",),
                 ("--price", "--price"), ("--charter=1",), ("--root", str(self.root)),
                 ("--charter", "-1"), ("--charter", str(1 << 256)), ("--charter",), ("--help", "--price")]
        for arguments in cases:
            with self.subTest(arguments=arguments), patch.object(sys, "argv", ["verify.py", *arguments]), \
                    patch.object(self.verify, "verify_install", side_effect=AssertionError("must reject before filesystem")), \
                    contextlib.redirect_stderr(io.StringIO()) as error:
                self.assertEqual(2, self.verify.main())
                self.assertEqual("invalid_input", json.loads(error.getvalue())["error"]["type"])

    def test_actual_charter_child_uses_custom_endpoint_before_alchemy(self):
        fixture = load_module(ROOT / "maintenance/check-snapshot.py", "verify_rpc_fixture")
        rpc = fixture.RPCFixture()
        rpc.timestamp = int(time.time()) - 2
        target = "/verify-private-route/rpc?access=verify-private-query"

        def respond(payload):
            return 200, {"Content-Type": "application/json"}, rpc(payload, 10, 40, lambda: 0)

        with fixture.rpc_server(respond) as (origin, requests), \
                patch.dict(os.environ, {"SRSTACK_RPC_URL": origin + target,
                                        "ALCHEMY_API_KEY": "verify-unused-alchemy-key"}, clear=True):
            result = self.invoke("--charter", "7")
        self.assertEqual(result.returncode, 0, result.stdout.decode() + result.stderr.decode())
        self.assertEqual(result.stderr, b"")
        report = json.loads(result.stdout)
        self.assertEqual(report["status"], "ok")
        self.assertEqual([(stage["name"], stage["status"]) for stage in report["stages"]],
                         [("integrity", "ok"), ("charter", "ok")])
        self.assertEqual({path for path, _, _ in requests}, {target})
        methods = {item["method"] for _, batch, _ in requests for item in batch}
        self.assertTrue({"eth_chainId", "eth_getBlockByNumber", "eth_getCode", "eth_call"} <= methods)
        for secret in ("verify-private-route", "verify-private-query", "verify-unused-alchemy-key"):
            self.assertNotIn(secret, result.stdout.decode() + result.stderr.decode())

    def test_actual_charter_child_preserves_custom_http_denial_without_credentials(self):
        fixture = load_module(ROOT / "maintenance/check-snapshot.py", "verify_rpc_denial_fixture")
        route, query, key = "verify-denied-route", "verify-denied-query", "verify-denied-alchemy-key"
        target = "/" + route + "?access=" + query
        body = ("provider denied original request " + " ".join((route, query, key))).encode()
        with fixture.rpc_server(lambda payload: (403, {"X-Request-Id": key}, body)) as (origin, requests), \
                patch.dict(os.environ, {"SRSTACK_RPC_URL": origin + target, "ALCHEMY_API_KEY": key}, clear=True):
            result = self.invoke("--charter", "7", "--price")
        self.assertEqual(result.returncode, 5, result.stdout.decode() + result.stderr.decode())
        report = json.loads(result.stdout)
        self.assertEqual([stage["status"] for stage in report["stages"]], ["ok", "failed", "skipped"])
        error = report["stages"][1]["helper_error"]
        self.assertEqual(error["type"], "snapshot_error")
        diagnostics = error["diagnostics"]
        self.assertEqual(diagnostics["http_status"], 403)
        self.assertIn("provider denied original request", diagnostics["response_excerpt"])
        endpoint = urlsplit(diagnostics["endpoint"])
        self.assertEqual(endpoint.netloc, urlsplit(origin).netloc)
        self.assertEqual(endpoint.query, "")
        self.assertEqual([path for path, _, _ in requests], [target])
        for secret in (route, query, key):
            self.assertNotIn(secret, result.stdout.decode() + result.stderr.decode())

    def test_partial_charter_never_becomes_success_or_runs_price(self):
        self.helper_result("snapshot.py", {"schema_version": 1, "status": "partial", "view": "charter",
                                           "values": {"charter_pending": {"value": "123", "unit": "STANDARD"}},
                                           "errors": {"charter_owner": "unavailable"}})
        self.helper("price.py", "raise SystemExit('price must not run after a partial charter')\n")
        report, code = self.verify.run({"--charter": "1", "--price": True})
        self.assertEqual(5, code)
        self.assertEqual(["ok", "partial", "skipped"], [stage["status"] for stage in report["stages"]])
        self.assertEqual("successful_charter_balance_required", report["stages"][-1]["error"])

    def test_missing_invalid_or_wrong_unit_balance_never_substitutes_zero(self):
        for balance in (None, {"value": None, "unit": "STANDARD"}, {"value": "1", "unit": "ETH"},
                        {"value": "-1", "unit": "STANDARD"}, {"value": "NaN", "unit": "STANDARD"},
                        {"value": 0, "unit": "STANDARD"}):
            with self.subTest(balance=balance):
                values = {"charter_owner": {"value": "0x" + "1" * 40, "unit": "address"}}
                if balance is not None:
                    values["charter_pending"] = balance
                self.helper_result("snapshot.py", {"schema_version": 1, "status": "ok", "view": "charter",
                                                   "values": values, "errors": {}})
                self.helper("price.py", "raise SystemExit('missing balance must not trigger a quote or zero valuation')\n")
                report, code = self.verify.run({"--charter": "1", "--price": True})
                self.assertEqual(5, code)
                self.assertEqual("skipped", report["stages"][-1]["status"])
                self.assertNotIn("helper_exit", report["stages"][-1])

    def test_nonzero_exit_malformed_output_and_partial_price_never_pass(self):
        for source, status in (("raise SystemExit(5)\n", "failed"), ("print('not JSON')\n", "failed"),
                               ("print('{\"schema_version\":1,\"status\":[],\"values\":{},\"errors\":{}}')\n", "failed"),
                               ("print('{\"schema_version\":1,\"status\":\"partial\",\"values\":{},\"errors\":{}}')\n", "partial"),
                               ("print('{\"schema_version\":1,\"status\":\"ok\",\"values\":{},\"errors\":{\"quote\":\"missing\"}}')\n", "partial")):
            with self.subTest(source=source):
                self.helper("price.py", source)
                report, code = self.verify.run({"--price": True})
                self.assertEqual(5, code)
                self.assertEqual(status, report["stages"][-1]["status"])
    def test_structured_failures_preserve_reason_without_other_helper_output(self):
        cases = [("snapshot.py", {"--charter": "1"}, "snapshot_error", "RPC chain ID mismatch"),
                 ("price.py", {"--price": True}, "price_error", "provider temporarily unavailable"),
                 ("price.py", {"--price": True}, "price_error", "provider schema invalid")]
        for script, options, kind, reason in cases:
            with self.subTest(reason=reason):
                payload = {"error": {"type": kind, "message": reason},
                           "values": {"do_not_publish": "financial payload"}}
                self.helper(script, "import json, sys\n"
                            "sys.stderr.write(json.dumps(" + repr(payload) + "))\n"
                            "raise SystemExit(5)\n")
                report, code = self.verify.run(options)
                self.assertEqual(5, code)
                stage = report["stages"][-1]
                self.assertEqual({"type": kind, "message": reason}, stage["helper_error"])
                self.assertNotIn("financial payload", json.dumps(report))

    def test_http_diagnostics_exclude_unsafe_headers_and_bound_untrusted_body(self):
        payload = {"error": {"type": "snapshot_error", "message": "endpoint denied this request",
                            "diagnostics": {
                                "endpoint": "https://rpc.mainnet.chain.robinhood.com/",
                                "http_status": 403, "headers": {
                                    "server": "test-edge", "set-cookie": "private-cookie",
                                    "authorization": "private-token", "x-request-id": "request-123"},
                                "response_excerpt": "\x1b" + "denied " * 1000,
                                "truncated": False, "read_error": None,
                                "unexpected": "private-metadata"}}}
        self.helper("snapshot.py", "import json, sys\nsys.stderr.write(json.dumps(" + repr(payload) + "))\nraise SystemExit(5)\n")
        report, code = self.verify.run({"--charter": "1", "--price": True})
        self.assertEqual(5, code)
        self.assertEqual("skipped", report["stages"][-1]["status"])
        diagnostics = report["stages"][1]["helper_error"]["diagnostics"]
        self.assertEqual(403, diagnostics["http_status"])
        self.assertTrue(diagnostics["truncated"])
        self.assertTrue(diagnostics["untrusted_response"])
        self.assertLessEqual(len(diagnostics["response_excerpt"].encode("utf-8")), 2048)
        self.assertTrue(diagnostics["response_excerpt"].isprintable())
        self.assertNotIn("private-", json.dumps(report))

    def test_unstructured_and_oversized_error_details_are_not_dumped(self):
        self.helper("price.py", "import sys\nsys.stderr.write('raw stderr must not escape')\nraise SystemExit(5)\n")
        report, code = self.verify.run({"--price": True})
        self.assertEqual(5, code)
        self.assertEqual("unstructured_error", report["stages"][-1]["helper_error"]["type"])
        self.assertNotIn("raw stderr must not escape", json.dumps(report))
        payload = {"error": {"type": "price_error", "message": "unavailable\n\x1b" + "x" * 1000}}
        self.helper("price.py", "import json, sys\nsys.stderr.write(json.dumps(" + repr(payload) + "))\nraise SystemExit(5)\n")
        report, code = self.verify.run({"--price": True})
        message = report["stages"][-1]["helper_error"]["message"]
        self.assertEqual(5, code)
        self.assertLessEqual(len(message), self.verify.MAX_ERROR_MESSAGE)
        self.assertTrue(message.isprintable())
        self.assertTrue(message.startswith("unavailable"))

    def test_partial_details_are_counted_bounded_and_exclude_values(self):
        errors = {"field_" + str(index): "unavailable " + "x" * 1000 for index in range(12)}
        self.helper_result("snapshot.py", {"schema_version": 1, "status": "partial", "view": "charter",
                                           "values": {"private_result": "financial payload"}, "errors": errors})
        report, code = self.verify.run({"--charter": "1"})
        self.assertEqual(5, code)
        stage = report["stages"][-1]
        self.assertEqual(12, stage["helper_error_count"])
        self.assertEqual(8, len(stage["helper_errors"]))
        self.assertTrue(stage["helper_errors_truncated"])
        self.assertTrue(all(message.startswith("unavailable") and len(message) <= 240
                            for message in stage["helper_errors"].values()))
        self.assertNotIn("financial payload", json.dumps(report))

    def test_child_timeout_and_combined_output_limit_are_failures(self):
        cases = [("import time\ntime.sleep(5)\n", "CHILD_TIMEOUT", 0.1),
                 ("import sys\nsys.stdout.write('x' * 160)\nsys.stderr.write('x' * 160)\n", "MAX_OUTPUT_BYTES", 256)]
        for source, constant, limit in cases:
            with self.subTest(constant=constant):
                self.helper("price.py", source)
                started = time.monotonic()
                with patch.object(self.verify, constant, limit):
                    report, code = self.verify.run({"--price": True})
                self.assertEqual(5, code)
                self.assertEqual("failed", report["stages"][-1]["status"])
                self.assertLess(time.monotonic() - started, 4)


if __name__ == "__main__":
    unittest.main()
