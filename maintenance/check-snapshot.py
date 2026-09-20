#!/usr/bin/env python3
"""Offline behavioral checks for the bounded snapshot reader (no live RPC)."""

import copy
import importlib.util
import io
import json
import os
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

ROOT = Path(__file__).resolve().parent.parent
SPEC = importlib.util.spec_from_file_location("sr_snapshot", ROOT / "scripts/snapshot.py")
snapshot = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(snapshot)
NOW = 1_789_500_000
WAD = 10 ** 18
HASH = "0x" + "12" * 32


class RPCFixture:
    """Return encoded scalar results keyed by real packaged calldata."""

    def __init__(self):
        self.interface, self.addresses, _ = snapshot._load_package()
        self.calls = {(self.addresses[c["contract"]], snapshot._calldata(c, {"charter_id": 7})): c for c in self.interface["calls"]}
        self.values = {
            "token_decimals": 18, "stream_rate_per_second": WAD + 2,
            "total_branches": 3, "charter_branches": 2,
            "issuance_budget": 100 * WAD, "cumulative_issued": 30 * WAD,
            "token_hard_cap": 200 * WAD, "token_max_supply": 180 * WAD,
            "token_burned_forever": 7 * WAD + 1, "token_ledger_retired": 13 * WAD - 1,
            "buy_tax_percent": 9000, "sell_tax_percent": 6667,
            "license_current_price": 5 * WAD, "license_remaining": 7,
            "license_last_sale_price": 6 * WAD, "license_last_sale_day": 4,
            "license_current_day": 4, "license_paused": False,
            "charter_auction_paused": False, "charter_auction_remaining": 3,
        }
        self.fail = set()
        self.words = {}
        self.code_fail = set()
        self.chain = snapshot.CHAIN_ID
        self.timestamp = NOW - 2
        self.reorg = False
        self.requests = []
        self.mutate_response = None

    def __call__(self, payload, timeout, deadline, monotonic):
        assert 0 < timeout <= snapshot.REQUEST_TIMEOUT
        batch = json.loads(payload)
        assert len(batch) <= snapshot.BATCH_SIZE
        self.requests.extend(batch)
        response = []
        for request in batch:
            method, params = request["method"], request["params"]
            result = None
            error = False
            if method == "eth_chainId":
                result = hex(self.chain)
            elif method == "eth_getBlockByNumber":
                result = {"number": "0x64", "timestamp": hex(self.timestamp), "hash": "0x" + "34" * 32 if self.reorg and params[0] != "latest" else HASH}
            elif method == "eth_getCode":
                result = "0x" if params[0] in self.code_fail else "0x60016000"
            elif method == "eth_call":
                call = self.calls[(params[0]["to"], params[0]["data"])]
                identifier = call["id"]
                error = identifier in self.fail
                if identifier in self.words:
                    result = self.words[identifier]
                else:
                    if "binds_to" in call:
                        value = self.addresses[call["binds_to"]]
                    else:
                        value = self.values.get(identifier, "0x" + "ab" * 20 if call["output_type"] == "address" else True if call["output_type"] == "bool" else 1)
                    result = "0x" + format(int(value, 16) if isinstance(value, str) else int(value), "064x")
            else:
                raise AssertionError("unexpected RPC method")
            item = {"jsonrpc": "2.0", "id": request["id"]}
            item.update({"error": {"code": -32000, "message": "unavailable"}} if error else {"result": result})
            response.append(item)
        if self.mutate_response:
            response = self.mutate_response(response)
        # Reverse ordering deliberately: JSON-RPC batches are unordered.
        return json.dumps(list(reversed(response))).encode()

    def run(self, view="protocol", detail="summary"):
        config = {"schema_version": 1, "view": view, "detail": detail}
        if view == "charter":
            config["charter_id"] = 7
        return snapshot.snapshot(config, transport=self, now=lambda: NOW)


class SnapshotChecks(unittest.TestCase):
    def setUp(self):
        self.rpc = RPCFixture()

    def test_input_denials_precede_transport(self):
        good = {"schema_version": 1, "view": "protocol"}
        bad = [None, [], dict(good, schema_version=True), dict(good, view="raw"), dict(good, detail="trace"),
               dict(good, charter_id=7), {"schema_version": 1, "view": "charter"},
               *({"schema_version": 1, "view": "charter", "charter_id": value} for value in (True, -1, 1.0, "7", 1 << 256))]
        for field in ("rpc_url", "endpoint", "address", "selector", "headers", "wallet", "private_key", "cost_basis", "apr", "path", "funding"):
            bad.append(dict(good, **{field: "external-data"}))
        for config in bad:
            with self.subTest(config=config), self.assertRaises(snapshot.InputError):
                snapshot.snapshot(config, transport=self.rpc)
        self.assertEqual(self.rpc.requests, [])
        with self.assertRaises(ValueError):
            snapshot._json(b'{"view":"protocol","view":"charter"}', 4096)
        with self.assertRaises(ValueError):
            snapshot._json(b" " * 4097, 4096)
        with self.assertRaises(ValueError):
            snapshot._json(b"[" * 13 + b"]" * 13, 4096)

    def cli(self, raw=b"", args=()):
        incoming = unittest.mock.Mock()
        if args:
            incoming.buffer.read.side_effect = AssertionError("explicit CLI read stdin")
        else:
            incoming.buffer = io.BytesIO(raw)
        stdout, stderr = io.StringIO(), io.StringIO()
        with patch.object(snapshot.sys, "argv", ["snapshot.py", *args]), \
                patch.object(snapshot.sys, "stdin", incoming), \
                patch.object(snapshot.sys, "stdout", stdout), \
                patch.object(snapshot.sys, "stderr", stderr), \
                patch.object(snapshot, "_https", self.rpc), \
                patch.object(snapshot.time, "time", return_value=NOW), \
                patch.object(snapshot.time, "monotonic", return_value=0):
            code = snapshot.main()
        return code, stdout.getvalue(), stderr.getvalue()

    def test_cli_views_match_json_without_reading_stdin(self):
        cases = [
            (("protocol",), {"view": "protocol"}),
            (("auctions", "--detail", "full"), {"view": "auctions", "detail": "full"}),
            (("charter", "--detail", "full", "--id", "7"),
             {"view": "charter", "detail": "full", "charter_id": 7}),
            (("charter", "--id", "0"), {"view": "charter", "charter_id": 0}),
            (("charter", "--id", str(snapshot.UINT256_MAX)),
             {"view": "charter", "charter_id": snapshot.UINT256_MAX}),
        ]
        for args, config in cases:
            with self.subTest(args=args):
                self.rpc.calls = {
                    (self.rpc.addresses[call["contract"]],
                     snapshot._calldata(call, dict({"charter_id": 7}, **config))): call
                    for call in self.rpc.interface["calls"]
                }
                expected = self.cli(json.dumps(dict(schema_version=1, **config)).encode())
                actual = self.cli(b"invalid stdin must be ignored", args=args)
                self.assertEqual(actual[0], 0, actual[2])
                self.assertEqual(actual, expected)

    def test_cli_denials_precede_package_reads_and_transport(self):
        cases = [
            ("charter",), ("protocol", "--id", "7"), ("charter", "--id", "-1"),
            ("charter", "--id", str(1 << 256)), ("charter", "--id", "9" * 79),
            ("charter", "--id", "1.0"), ("charter", "--id", "1e2"),
            ("charter", "--id", "７"), ("charter", "--id", "0x7"),
            ("charter", "--id", "+7"), ("charter", "--id", " 7"),
            ("charter", "--id", "7", "--id", "8"),
            ("protocol", "--detail", "full", "--detail", "summary"),
            ("protocol", "--detail"), ("protocol", "--detail", "trace"),
            ("protocol", "--det", "full"), ("protocol", "--detail=full"),
            ("protocol", "--url", "https://bad.invalid"), ("--help", "protocol"),
            ("--detail", "full", "protocol"), ("protocol", "auctions"),
            ("protocol",) * 6, ("x" * 81,),
        ]
        with patch.object(snapshot, "_load_package", side_effect=AssertionError("invalid CLI read package")):
            for args in cases:
                with self.subTest(args=args):
                    code, stdout, stderr = self.cli(args=args)
                    self.assertEqual((code, stdout), (2, ""))
                    self.assertEqual(json.loads(stderr)["error"]["type"], "invalid_input")
            code, stdout, stderr = self.cli(args=("--help",))
            self.assertEqual((code, stderr), (0, ""))
        self.assertEqual(self.rpc.requests, [])

    def test_cli_failure_channels(self):
        for raw, code, error in ((b"{}", 2, None), (b" " * 4097, 2, None),
                                  (b'{"schema_version":1,"view":"protocol"}', 4, snapshot.PackageDataError("invalid")),
                                  (b'{"schema_version":1,"view":"protocol"}', 5, snapshot.SnapshotError("unavailable"))):
            stdout, stderr = io.StringIO(), io.StringIO()
            with patch.object(snapshot.sys, "argv", ["snapshot.py"]), patch.object(snapshot.sys, "stdin", io.TextIOWrapper(io.BytesIO(raw))), patch.object(snapshot.sys, "stdout", stdout), patch.object(snapshot.sys, "stderr", stderr):
                if error:
                    with patch.object(snapshot, "_load_package", side_effect=error):
                        actual = snapshot.main()
                else:
                    actual = snapshot.main()
            self.assertEqual(actual, code)
            self.assertEqual(stdout.getvalue(), "")
            self.assertIn("error", json.loads(stderr.getvalue()))

    def test_package_execution_metadata_rejected(self):
        catalog = json.loads((ROOT / "assets/entities/robinhood.json").read_bytes())
        mutations = [lambda data: data.update(rpc_url="https://user:secret@example.com/"),
                     lambda data: data.update(entity_catalog="../../outside.json"),
                     lambda data: data.update(chain_id=1),
                     lambda data: data["calls"][0].update(mutability="nonpayable"),
                     lambda data: data["calls"][0].update(selector="0xa9059cbb"),
                     lambda data: data["calls"][0].update(profiles=["raw"]),
                     lambda data: data["calls"][0].update(output_type="bytes32"),
                     lambda data: data["calls"][0].update(decimals=18),
                     lambda data: data["calls"].append(copy.deepcopy(data["calls"][0])),
                     lambda data: data["calls"][0].update(function="transfer", signature="transfer()"),
                     lambda data: data["calls"][0].update(profiles=["auctions"])]
        for mutate in mutations:
            interface = copy.deepcopy(self.rpc.interface)
            mutate(interface)
            with self.assertRaises((ValueError, TypeError)):
                snapshot._validate_package(interface, catalog)
        for field, value in (("address", "0x1234"), ("address", snapshot.ZERO_ADDRESS), ("chain_id", 1), ("id", catalog["records"][1]["id"])):
            changed = copy.deepcopy(catalog)
            changed["records"][0][field] = value
            with self.assertRaises(ValueError):
                snapshot._validate_package(self.rpc.interface, changed)

    def test_safe_loader_rejects_links_and_oversized_files(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "scripts").mkdir()
            script = root / "scripts/snapshot.py"
            script.touch()
            (root / "assets").mkdir()
            for folder, name in (("interfaces", "robinhood-reads.json"), ("entities", "robinhood.json")):
                (root / "assets" / folder).mkdir()
                (root / "assets" / folder / name).write_bytes((ROOT / "assets" / folder / name).read_bytes())
            with patch.object(snapshot, "__file__", str(script)):
                snapshot._load_package()
                target = root / "assets/interfaces/robinhood-reads.json"
                target.unlink()
                target.symlink_to(ROOT / "assets/interfaces/robinhood-reads.json")
                with self.assertRaises(snapshot.PackageDataError):
                    snapshot._load_package()
                target.unlink()
                target.write_bytes(b" " * (snapshot.MAX_FILE_BYTES + 1))
                with self.assertRaises(snapshot.PackageDataError):
                    snapshot._load_package()
                target.unlink()
                os.mkfifo(target)
                with self.assertRaises(snapshot.PackageDataError):
                    snapshot._load_package()
                target.unlink()
                (root / "assets/interfaces").rmdir()
                (root / "assets/interfaces").symlink_to(ROOT / "assets/interfaces", target_is_directory=True)
                with self.assertRaises(snapshot.PackageDataError):
                    snapshot._load_package()

    def test_wrong_chain_stale_future_and_reorg_are_fatal(self):
        for field, value in (("chain", 1), ("timestamp", NOW - 301), ("timestamp", NOW + 31), ("reorg", True)):
            rpc = RPCFixture()
            setattr(rpc, field, value)
            with self.subTest(field=field), self.assertRaises(snapshot.SnapshotError):
                rpc.run()
        self.rpc.chain = 1
        with self.assertRaises(snapshot.SnapshotError):
            self.rpc.run()
        self.assertEqual([r["method"] for r in self.rpc.requests], ["eth_chainId"])

    def test_single_block_and_exact_rate_arithmetic(self):
        result = self.rpc.run("charter")
        self.assertEqual(result["status"], "ok")
        self.assertEqual(result["derived"]["global_gross_daily"]["value"], "86400.0000000000001728")
        # Integer division before branch multiplication matters at wei precision.
        expected = snapshot._scaled(((WAD + 2) // 3) * 2 * 86400, 18)
        self.assertEqual(result["derived"]["charter_gross_daily"]["value"], expected)
        self.assertEqual(result["derived"]["remaining_gross_budget"]["value"], "70")
        self.assertEqual(result["values"]["charter_branches"]["value"], 2)
        self.assertIs(result["values"]["emissions_started"]["value"], True)
        for request in self.rpc.requests:
            if request["method"] in ("eth_call", "eth_getCode"):
                self.assertEqual(request["params"][1], "0x64")
        protocol = self.rpc.run()
        self.assertEqual(protocol["derived"]["permanent_removed"]["value"], "20")
        self.assertEqual(protocol["values"]["token_burned_forever"]["value"], "7.000000000000000001")
        self.assertEqual(protocol["values"]["token_ledger_retired"]["value"], "12.999999999999999999")
        self.assertEqual(result["derived"]["permanent_removed"]["value"], "20")
        self.assertEqual(protocol["values"]["sell_tax_percent"]["value"], "66.67")

    def test_inactive_or_unknown_emissions_omit_daily_rates(self):
        for view in ("protocol", "charter"):
            for started in (False, None):
                with self.subTest(view=view, started=started):
                    rpc = RPCFixture()
                    if started is None:
                        rpc.fail.add("emissions_started")
                    else:
                        rpc.values["emissions_started"] = started
                    result = rpc.run(view)
                    self.assertNotIn("global_gross_daily", result["derived"])
                    self.assertNotIn("charter_gross_daily", result["derived"])
                    self.assertEqual(result["values"]["stream_rate_per_second"]["value"], "1.000000000000000002")
                    self.assertEqual(result["derived"]["remaining_gross_budget"]["value"], "70")
                    self.assertEqual(result["status"], "partial" if started is None else "ok")
                    if view == "charter":
                        self.assertEqual(result["values"]["charter_branches"]["value"], 2)

    def test_active_zero_stream_reports_zero_daily_rates(self):
        self.rpc.values["stream_rate_per_second"] = 0
        result = self.rpc.run("charter")
        self.assertEqual(result["derived"]["global_gross_daily"]["value"], "0")
        self.assertEqual(result["derived"]["charter_gross_daily"]["value"], "0")

    def test_rpc_and_decode_failures_preserve_unrelated_results(self):
        self.rpc.fail.add("epoch_number")
        self.rpc.words["stream_rate_per_second"] = "0x01"
        self.rpc.words["emissions_started"] = "0x" + format(2, "064x")
        result = self.rpc.run()
        self.assertEqual(result["status"], "partial")
        self.assertNotIn("epoch_number", result["values"])
        self.assertNotIn("stream_rate_per_second", result["values"])
        self.assertNotIn("global_gross_daily", result["derived"])
        self.assertEqual(result["derived"]["permanent_removed"]["value"], "20")
        self.assertIn("buy_tax_percent", result["values"])

    def test_binding_failure_isolates_role(self):
        self.rpc.values["central_bank_owner"] = "0x" + "cc" * 20
        self.rpc.words["binding_centralBank_standard"] = "0x" + "0" * 64
        result = self.rpc.run()
        central_ids = {call["id"] for call in self.rpc.interface["calls"] if call["contract"] == "centralBank"}
        self.assertFalse(central_ids & result["values"].keys())
        self.assertNotIn("remaining_gross_budget", result["derived"])
        self.assertIn("token_total_supply", result["values"])
        self.assertIn("buy_tax_percent", result["values"])
        self.assertEqual(result["status"], "partial")
        rpc = RPCFixture()
        rpc.fail.add("binding_licenseAuction_bank")
        auction = rpc.run("auctions")
        self.assertNotIn("license_current_price", auction["values"])
        self.assertEqual(auction["derived"]["charter_auction_status"]["value"], "open")

    def test_unavailable_hook_preserves_charter_accounting(self):
        for failure in ("missing_code", "binding_mismatch"):
            with self.subTest(failure=failure):
                rpc = RPCFixture()
                rpc.values["charter_pending"] = 23 * WAD
                if failure == "missing_code":
                    rpc.code_fail.add(rpc.addresses["taxHook"])
                else:
                    rpc.words["binding_taxHook_standard"] = "0x" + "0" * 64
                result = rpc.run("charter")
                self.assertEqual(result["status"], "partial")
                self.assertEqual(result["values"]["charter_branches"]["value"], 2)
                self.assertEqual(result["values"]["charter_pending"]["value"], "23")
                self.assertEqual(result["values"]["token_burned_forever"]["value"], "7.000000000000000001")
                self.assertEqual(result["derived"]["permanent_removed"]["value"], "20")
                for identifier in ("trading_hook_owner", "launch_schedule_active", "hook_pending_owner"):
                    self.assertNotIn(identifier, result["values"])
                    self.assertIn(identifier, result["errors"])

    def test_missing_code_cannot_look_like_valid_zero(self):
        self.rpc.code_fail.add(self.rpc.addresses["licenseAuction"])
        result = self.rpc.run("auctions")
        self.assertNotIn("license_current_price", result["values"])
        self.assertIn("code_licenseAuction", result["errors"])
        self.assertEqual(result["derived"]["charter_auction_status"]["value"], "open")

    def test_decimals_gate_all_standard_amounts_not_eth(self):
        for word in ("0x" + format(6, "064x"), "0x" + format(256, "064x")):
            rpc = RPCFixture()
            rpc.words["token_decimals"] = word
            result = rpc.run()
            self.assertFalse(any(item["unit"].startswith("STANDARD") for item in result["values"].values()))
            self.assertNotIn("global_gross_daily", result["derived"])
            self.assertNotIn("permanent_removed", result["derived"])
            self.assertIn("buy_tax_percent", result["values"])
            auction = rpc.run("auctions")
            self.assertNotIn("license_current_price", auction["values"])
            self.assertIn("charter_auction_current_price", auction["values"])

    def test_owner_and_branch_prerequisites(self):
        for change in ("owner_error", "zero_owner", "zero_total", "excess_branches"):
            rpc = RPCFixture()
            if change == "owner_error":
                rpc.fail.add("charter_owner")
                # ownerOf reverts for a nonexistent token while mapping getters
                # can still return incidental zeros for that same token ID.
                rpc.values.update(charter_branches=0, charter_pending=0)
            elif change == "zero_owner":
                rpc.values["charter_owner"] = snapshot.ZERO_ADDRESS
            elif change == "zero_total":
                rpc.values["total_branches"] = 0
            else:
                rpc.values["charter_branches"] = 4
            result = rpc.run("charter")
            self.assertNotIn("charter_gross_daily", result["derived"])
            self.assertIn("global_gross_daily", result["derived"])
            self.assertEqual(result["status"], "partial")
            if change in ("owner_error", "zero_owner"):
                for identifier in ("charter_branches", "charter_pending"):
                    self.assertNotIn(identifier, result["values"])
                    self.assertIn(identifier, result["errors"])

    def test_failed_pending_omits_balance_without_erasing_charter_rate(self):
        self.rpc.fail.add("charter_pending")
        result = self.rpc.run("charter")
        self.assertEqual(result["status"], "partial")
        self.assertNotIn("charter_pending", result["values"])
        self.assertIn("charter_pending", result["errors"])
        self.assertEqual(result["values"]["charter_branches"]["value"], 2)
        self.assertEqual(result["derived"]["charter_gross_daily"]["value"],
                         snapshot._scaled(((WAD + 2) // 3) * 2 * 86400, 18))
        self.assertEqual(result["derived"]["remaining_gross_budget"]["value"], "70")

    def test_negative_supply_differences_are_not_clamped(self):
        self.rpc.values.update(cumulative_issued=101 * WAD, token_max_supply=201 * WAD)
        result = self.rpc.run()
        for identifier in ("remaining_gross_budget", "permanent_removed"):
            self.assertNotIn(identifier, result["derived"])
            self.assertIn(identifier, result["errors"])

    def test_inconsistent_burn_decomposition_preserves_observations_not_total(self):
        for view in ("protocol", "charter"):
            rpc = RPCFixture()
            rpc.values["token_burned_forever"] += 1
            result = rpc.run(view)
            self.assertEqual(result["status"], "partial")
            self.assertNotIn("permanent_removed", result["derived"])
            self.assertIn("permanent_removed", result["errors"])
            self.assertEqual(result["values"]["token_max_supply"]["value"], "180")
            self.assertEqual(result["values"]["token_burned_forever"]["value"], "7.000000000000000002")
            self.assertEqual(result["values"]["token_ledger_retired"]["value"], "12.999999999999999999")
            self.assertEqual(result["derived"]["remaining_gross_budget"]["value"], "70")

    def test_partial_burn_reads_do_not_redefine_permanent_removed(self):
        self.rpc.fail.add("token_ledger_retired")
        result = self.rpc.run()
        self.assertEqual(result["status"], "partial")
        self.assertIn("token_ledger_retired", result["errors"])
        self.assertNotIn("token_ledger_retired", result["values"])
        self.assertEqual(result["values"]["token_burned_forever"]["value"], "7.000000000000000001")
        self.assertEqual(result["derived"]["permanent_removed"]["value"], "20")
        self.assertNotIn("permanent_removed", result["errors"])
        rpc = RPCFixture()
        rpc.fail.add("token_max_supply")
        unavailable_cap = rpc.run("charter")
        self.assertEqual(unavailable_cap["status"], "partial")
        self.assertIn("token_max_supply", unavailable_cap["errors"])
        self.assertNotIn("permanent_removed", unavailable_cap["derived"])
        self.assertEqual(unavailable_cap["values"]["token_burned_forever"]["value"], "7.000000000000000001")
        self.assertEqual(unavailable_cap["values"]["token_ledger_retired"]["value"], "12.999999999999999999")

    def test_enabled_launch_cap_can_be_inactive(self):
        for view in ("protocol", "charter"):
            rpc = RPCFixture()
            rpc.values.update(launch_holding_cap_enabled=True, launch_holding_cap_active=False,
                              launch_schedule_active=False, pool_manager_gate_enabled=False)
            result = rpc.run(view)
            self.assertEqual(result["status"], "ok")
            self.assertIs(result["values"]["launch_holding_cap_enabled"]["value"], True)
            self.assertIs(result["values"]["launch_holding_cap_active"]["value"], False)
            self.assertIs(result["values"]["launch_schedule_active"]["value"], False)
            self.assertIs(result["values"]["pool_manager_gate_enabled"]["value"], False)

    def test_unavailable_active_cap_is_not_inferred_from_enabled_or_hook(self):
        self.rpc.fail.add("launch_holding_cap_active")
        result = self.rpc.run()
        self.assertEqual(result["status"], "partial")
        self.assertNotIn("launch_holding_cap_active", result["values"])
        self.assertIn("launch_holding_cap_active", result["errors"])
        self.assertIs(result["values"]["launch_holding_cap_enabled"]["value"], True)
        self.assertIs(result["values"]["launch_schedule_active"]["value"], True)
        self.assertEqual(result["derived"]["permanent_removed"]["value"], "20")

    def test_auction_quote_availability_and_closing_price(self):
        for state, fields in (("not_started", {"license_started": False, "license_current_price": 0}),
                              ("paused", {"license_paused": True}),
                              ("sold_out", {"license_remaining": 0})):
            for detail in ("summary", "full"):
                rpc = RPCFixture()
                rpc.values.update(fields)
                result = rpc.run("auctions", detail)
                self.assertEqual(result["derived"]["license_status"]["value"], state)
                self.assertNotIn("license_current_price", result["values"])
                if state == "sold_out":
                    self.assertEqual(result["derived"]["license_closing_price"]["value"], "6")
                else:
                    self.assertNotIn("license_closing_price", result["derived"])
        self.rpc.values.update(license_remaining=0, license_last_sale_day=3)
        self.assertNotIn("license_closing_price", self.rpc.run("auctions")["derived"])
        rpc = RPCFixture()
        rpc.fail.add("license_paused")
        self.assertNotIn("license_current_price", rpc.run("auctions")["values"])
        self.assertEqual(RPCFixture().run("auctions")["values"]["license_current_price"]["value"], "5")

    def test_full_evidence_is_opt_in(self):
        summary = self.rpc.run()
        full = RPCFixture().run(detail="full")
        self.assertEqual(summary["values"], full["values"])
        self.assertNotIn("rpc_exchanges", summary["evidence"])
        evidence = full["evidence"]
        self.assertEqual(evidence["block_hash"], HASH)
        mapped = next(item for item in evidence["call_mapping"] if item["id"] == "sell_tax_percent")
        self.assertEqual(mapped["data"], "0xa578d578" + "0" * 64)
        self.assertTrue(any(request["params"] == ["0x64", False] for exchange in evidence["rpc_exchanges"] for request in exchange["requests"]))

    def test_bounded_response_and_unordered_envelope_integrity(self):
        with self.assertRaises(snapshot.SnapshotError):
            snapshot.snapshot({"schema_version": 1, "view": "protocol"}, transport=lambda *args: b" " * (snapshot.MAX_RESPONSE_BYTES + 1))
        self.rpc.mutate_response = lambda response: response + response
        with self.assertRaises(snapshot.SnapshotError):
            self.rpc.run()
        clock = iter((0, 0, 41))
        with self.assertRaises(snapshot.SnapshotError):
            snapshot.snapshot({"schema_version": 1, "view": "protocol"}, transport=RPCFixture(), now=lambda: NOW, monotonic=lambda: next(clock))

    def test_nonfinite_rpc_evidence_returns_structured_error(self):
        def overflowing_response(payload, *args):
            response = json.loads(self.rpc(payload, *args))
            response[0]["extra"] = "OVERFLOW_MARKER"
            return json.dumps(response).replace('"OVERFLOW_MARKER"', "1e400").encode()

        incoming = unittest.mock.Mock()
        incoming.buffer = io.BytesIO(b'{"schema_version":1,"view":"protocol","detail":"full"}')
        stdout, stderr = io.StringIO(), io.StringIO()
        with patch.object(snapshot, "_https", side_effect=overflowing_response), \
                patch.object(snapshot.time, "time", return_value=NOW), \
                patch.object(snapshot.sys, "argv", ["snapshot.py"]), \
                patch.object(snapshot.sys, "stdin", incoming), \
                patch.object(snapshot.sys, "stdout", stdout), \
                patch.object(snapshot.sys, "stderr", stderr):
            code = snapshot.main()
        self.assertEqual(code, 5)
        self.assertEqual(stdout.getvalue(), "")
        self.assertEqual(json.loads(stderr.getvalue())["error"]["type"], "snapshot_error")
        with self.assertRaises(ValueError):
            snapshot._json(b'{"extra":' + b"9" * 100 + b"}", 4096)

    def test_expired_connection_does_not_send_request(self):
        connection = unittest.mock.Mock()
        with self.assertRaises(snapshot.SnapshotError):
            snapshot._https_request(connection, b"[]", 10, lambda: 11)
        connection.request.assert_not_called()
        connection.close.assert_called_once()

    def test_http_redirect_is_not_followed(self):
        connection = unittest.mock.Mock()
        connection.getresponse.return_value.status = 302
        with patch.object(snapshot.http.client, "HTTPSConnection", return_value=connection) as factory:
            with self.assertRaises(snapshot.SnapshotError):
                snapshot._https(b"[]", 10, 40, lambda: 0)
        self.assertEqual(factory.call_args.args, (snapshot.RPC_HOST,))
        self.assertEqual(connection.request.call_count, 1)
        self.assertEqual(connection.request.call_args.args[:2], ("POST", "/"))
        connection.close.assert_called_once()


if __name__ == "__main__":
    unittest.main()
