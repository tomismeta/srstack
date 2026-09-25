#!/usr/bin/env python3
"""Offline behavioral checks for the bounded snapshot reader (no live RPC)."""

import base64
import contextlib
import copy
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
import importlib.util
import io
import json
import os
from pathlib import Path
import tempfile
import threading
import unittest
from unittest.mock import patch
from urllib.parse import quote, urlsplit

ROOT = Path(__file__).resolve().parent.parent
SPEC = importlib.util.spec_from_file_location("sr_snapshot", ROOT / "scripts/snapshot.py")
snapshot = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(snapshot)
NOW = 1_789_500_000
WAD = 10 ** 18
HASH = "0x" + "12" * 32
ASSET = "0x" + "a1" * 20


class RPCFixture:
    """Return encoded static results keyed by real packaged calldata."""

    def __init__(self):
        self.interface, self.addresses, _ = snapshot._load_package()
        self.calls = {(self.addresses[c["contract"]], snapshot._calldata(c, {"charter_id": 7, "reserve_asset": ASSET})): c for c in self.interface["calls"]}
        self.values = {
            "token_decimals": 18, "stream_rate_per_second": WAD + 2,
            "total_branches": 3, "charter_branches": 2,
            "issuance_budget": 100 * WAD, "cumulative_issued": 30 * WAD,
            "token_hard_cap": 200 * WAD, "token_max_supply": 180 * WAD,
            "token_burned_forever": 7 * WAD + 1, "token_ledger_retired": 13 * WAD - 1,
            "buy_tax_percent": 9000, "sell_tax_percent": 6667,
            "license_current_price": 5 * WAD, "license_remaining": 7,
            "license_last_sale_price": 6 * WAD, "license_last_sale_round": 4,
            "license_current_round": 4, "license_paused": False,
            "license_auction_anchor": NOW - 2 - 4 * 43200, "license_round_seconds": 43200,
            "license_cap_window_seconds": 86400, "license_cap_window_index": 2,
            "license_max_per_charter_per_window": 3, "license_licenses_per_round": 50,
            "license_decay_half_life_seconds": 7200, "license_round_half_life_seconds": 7200,
            "license_round_cap": 50, "license_sold": 43,
            "charter_auction_current_day": 4, "charter_auction_day_seconds": 86400,
            "charter_auction_anchor": NOW - 2 - 4 * 86400,
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
                    if call["output_type"] == "tuple":
                        value = self.values.get(identifier, {
                            component["name"]: ("0x" + "ab" * 20 if component["output_type"] == "address"
                                                else True if component["output_type"] == "bool" else 1)
                            for component in call["components"]})
                        words = [value[component["name"]] for component in call["components"]]
                    else:
                        words = [value]
                    result = "0x" + "".join(format((int(word, 16) if isinstance(word, str) else int(word)) % (1 << 256), "064x")
                                              for word in words)
            else:
                raise AssertionError("unexpected RPC method")
            item = {"jsonrpc": "2.0", "id": request["id"]}
            item.update({"error": {"code": -32000, "message": "unavailable"}} if error else {"result": result})
            response.append(item)
        if self.mutate_response:
            response = self.mutate_response(response)
        # Reverse ordering deliberately: JSON-RPC batches are unordered.
        return json.dumps(list(reversed(response))).encode()

    def run(self, view="protocol", detail="summary", asset=None):
        config = {"schema_version": 1, "view": view, "detail": detail}
        if view == "charter":
            config["charter_id"] = 7
        if asset is not None:
            config["reserve_asset"] = asset
        return snapshot.snapshot(config, transport=self, now=lambda: NOW)


@contextlib.contextmanager
def rpc_server(respond):
    requests = []

    class Handler(BaseHTTPRequestHandler):
        def do_POST(self):
            payload = self.rfile.read(int(self.headers["Content-Length"]))
            requests.append((self.path, json.loads(payload), dict(self.headers)))
            status, headers, body = respond(payload)
            self.send_response(status)
            for name, value in headers.items():
                self.send_header(name, value)
            self.send_header("Content-Length", str(len(body)))
            self.end_headers()
            self.wfile.write(body)

        def log_message(self, *args):
            pass

    server = ThreadingHTTPServer(("127.0.0.1", 0), Handler)
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()
    try:
        yield "http://127.0.0.1:" + str(server.server_port), requests
    finally:
        server.shutdown()
        server.server_close()
        thread.join()


class SnapshotChecks(unittest.TestCase):
    def setUp(self):
        environment = patch.dict(os.environ, {}, clear=True)
        environment.start()
        self.addCleanup(environment.stop)
        self.rpc = RPCFixture()

    def test_input_denials_precede_transport(self):
        good = {"schema_version": 1, "view": "protocol"}
        bad = [None, [], dict(good, schema_version=True), dict(good, view="raw"), dict(good, detail="trace"),
               dict(good, charter_id=7), {"schema_version": 1, "view": "charter"},
               *({"schema_version": 1, "view": "charter", "charter_id": value} for value in (True, -1, 1.0, "7", 1 << 256))]
        bad.extend(dict(schema_version=1, view="treasury", reserve_asset=value)
                   for value in (None, 0, True, [], {}, snapshot.ZERO_ADDRESS, "0x1234",
                                 ASSET + " ", " " + ASSET, ASSET + "/path", "0X" + ASSET[2:]))
        bad.extend(dict(good, reserve_asset=ASSET) for good in (
            {"schema_version": 1, "view": "protocol"}, {"schema_version": 1, "view": "auctions"},
            {"schema_version": 1, "view": "charter", "charter_id": 7}))
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
            (("treasury",), {"view": "treasury"}),
            (("treasury", "--asset", ASSET, "--detail", "full"),
             {"view": "treasury", "reserve_asset": ASSET, "detail": "full"}),
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
                     snapshot._calldata(call, dict({"charter_id": 7, "reserve_asset": ASSET}, **config))): call
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
            ("protocol", "--asset", ASSET), ("charter", "--asset", ASSET),
            ("treasury", "--id", "7"), ("treasury", "--asset", snapshot.ZERO_ADDRESS),
            ("treasury", "--asset", "0x1234"), ("treasury", "--asset", ASSET, "--asset", ASSET),
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
        result = self.rpc.run("charter", "full")
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
                    result = rpc.run(view, "full")
                    self.assertNotIn("global_gross_daily", result["derived"])
                    self.assertNotIn("charter_gross_daily", result["derived"])
                    self.assertEqual(result["values"]["stream_rate_per_second"]["value"], "1.000000000000000002")
                    self.assertEqual(result["derived"]["remaining_gross_budget"]["value"], "70")
                    self.assertEqual(result["status"], "partial" if started is None else "ok")
                    if view == "charter":
                        self.assertEqual(result["values"]["charter_branches"]["value"], 2)

    def test_active_zero_stream_reports_zero_daily_rates(self):
        self.rpc.values["stream_rate_per_second"] = 0
        result = self.rpc.run("charter", "full")
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

    def test_queued_policy_remains_separate_from_active_policy(self):
        self.rpc.values.update(base_issuance_per_day=3 * WAD, epoch_days=9,
                               queued_base_issuance_per_day={"value": 91 * WAD + 1, "pending": False},
                               queued_epoch_days={"value": 17, "pending": True})
        result = self.rpc.run()
        queued = result["values"]["queued_base_issuance_per_day"]
        self.assertEqual(queued["unit"], "queued-policy")
        self.assertEqual(queued["value"]["value"],
                         {"value": "91.000000000000000001", "unit": "STANDARD/day", "type": "uint256"})
        self.assertIs(queued["value"]["pending"]["value"], False)
        self.assertEqual(result["values"]["base_issuance_per_day"]["value"], "3")
        self.assertEqual(result["values"]["epoch_days"]["value"], 9)
        self.assertEqual(result["values"]["queued_epoch_days"]["value"]["value"]["value"], 17)
        self.assertEqual(result["derived"]["global_gross_daily"]["value"], "86400.0000000000001728")
        self.rpc.values["token_decimals"] = 6
        unscaled = self.rpc.run()
        self.assertNotIn("queued_base_issuance_per_day", unscaled["values"])
        self.assertIn("queued_epoch_days", unscaled["values"])
        self.assertNotIn("queued_epoch_days", self.rpc.run("charter")["values"])
        self.rpc.values.update(fee_team_share_percent=2500, fee_pol_share_percent=7500,
                               fee_queued_shares={"teamBps": 1000, "polBps": 9000, "pending": False},
                               contraction_tick_pool_percent=200, contraction_effective_tick_pool_percent=100)
        treasury = self.rpc.run("treasury")
        self.assertEqual(treasury["values"]["fee_team_share_percent"], {"value": "25", "unit": "percent"})
        self.assertEqual(treasury["values"]["fee_queued_shares"]["value"]["teamBps"],
                         {"value": "10", "unit": "percent", "type": "uint256"})
        self.assertIs(treasury["values"]["fee_queued_shares"]["value"]["pending"]["value"], False)
        self.assertEqual(treasury["values"]["contraction_tick_pool_percent"]["value"], "2")
        self.assertEqual(treasury["values"]["contraction_effective_tick_pool_percent"]["value"], "1")

    def test_invalid_tuple_lengths_and_boolean_do_not_publish_queued_policy(self):
        for word in ("0x" + "0" * 64, "0x" + "0" * 192,
                     "0x" + format(7, "064x") + format(2, "064x")):
            rpc = RPCFixture()
            rpc.words["queued_epoch_days"] = word
            result = rpc.run()
            self.assertNotIn("queued_epoch_days", result["values"])
            self.assertIn("queued_epoch_days", result["errors"])
            self.assertIn("epoch_days", result["values"])

    def test_static_pool_tuple_enforces_padding_and_signed_boundaries(self):
        pool = {"currency0": snapshot.ZERO_ADDRESS, "currency1": ASSET,
                "fee": (1 << 24) - 1, "tickSpacing": -(1 << 23),
                "hooks": snapshot.ZERO_ADDRESS}
        for ticks in (-(1 << 23), (1 << 23) - 1):
            rpc = RPCFixture()
            rpc.values["expansion_reserve_pool"] = dict(pool, tickSpacing=ticks)
            result = rpc.run("treasury", asset=ASSET)
            self.assertEqual(result["values"]["expansion_reserve_pool"]["value"]["tickSpacing"],
                             {"value": ticks, "unit": "ticks", "type": "int24"})
            self.assertEqual(result["values"]["expansion_reserve_pool"]["value"]["fee"]["value"], (1 << 24) - 1)
        valid = [0, int(ASSET, 16), 3000, 60, 0]
        for index, invalid in ((0, 1 << 160), (2, 1 << 24),
                               (3, (1 << 24) - 1), (3, (1 << 256) - (1 << 23) - 1)):
            rpc = RPCFixture()
            words = list(valid)
            words[index] = invalid
            rpc.words["expansion_reserve_pool"] = "0x" + "".join(format(x, "064x") for x in words)
            result = rpc.run("treasury", asset=ASSET)
            self.assertNotIn("expansion_reserve_pool", result["values"])
            self.assertIn("expansion_reserve_pool", result["errors"])
            self.assertIn("expansion_holdings", result["values"])

    def test_treasury_asset_approval_gates_reads_without_borrowing_token_scale(self):
        self.rpc.values.update(expansion_holdings=1234567, token_decimals=6)
        approved = self.rpc.run("treasury", asset=ASSET)
        self.assertEqual(approved["reserve_asset"], ASSET)
        self.assertEqual(approved["values"]["expansion_holdings"],
                         {"value": 1234567, "unit": "reserve-token-raw-units"})
        self.assertNotIn("incentives_vault_standard_balance", approved["values"])
        self.assertTrue(all(request["params"][0]["to"] != ASSET for request in self.rpc.requests
                            if request["method"] == "eth_call"))
        for approval in (False, None):
            rpc = RPCFixture()
            if approval is None:
                rpc.fail.add("expansion_is_reserve_asset")
            else:
                rpc.values["expansion_is_reserve_asset"] = approval
            result = rpc.run("treasury", asset=ASSET)
            self.assertNotIn("expansion_holdings", result["values"])
            self.assertNotIn("expansion_reserve_pool", result["values"])
            self.assertIn("fee_team_share_percent", result["values"])
            observed = {rpc.calls[(request["params"][0]["to"], request["params"][0]["data"])]["id"]
                        for request in rpc.requests if request["method"] == "eth_call"}
            self.assertFalse(snapshot.ASSET_DETAILS & observed)
        rpc = RPCFixture()
        without_asset = rpc.run("treasury")
        self.assertNotIn("reserve_asset", without_asset)
        self.assertFalse(any("$reserve_asset" in rpc.calls[(request["params"][0]["to"], request["params"][0]["data"])]["args"]
                             for request in rpc.requests if request["method"] == "eth_call"))

    def test_treasury_failed_prerequisites_cannot_authenticate_dependents(self):
        for failure in ("bank_binding", "standard_code", "registry_code"):
            rpc = RPCFixture()
            if failure == "bank_binding":
                rpc.words["binding_centralBank_standard"] = "0x" + "0" * 64
            else:
                rpc.code_fail.add(rpc.addresses["standard" if failure == "standard_code" else "registry"])
            result = rpc.run("treasury", asset=ASSET)
            for identifier in ("fee_team_share_percent", "contraction_tick_pool_percent"):
                self.assertNotIn(identifier, result["values"])
                self.assertIn(identifier, result["errors"])
            if failure == "registry_code":
                self.assertNotIn("expansion_holdings", result["values"])
            else:
                self.assertIn("expansion_holdings", result["values"])

    def test_binding_failure_rejects_transitive_dependents(self):
        self.rpc.values["central_bank_owner"] = "0x" + "cc" * 20
        self.rpc.words["binding_centralBank_standard"] = "0x" + "0" * 64
        result = self.rpc.run()
        central_ids = {call["id"] for call in self.rpc.interface["calls"] if call["contract"] == "centralBank"}
        self.assertFalse(central_ids & result["values"].keys())
        self.assertNotIn("remaining_gross_budget", result["derived"])
        self.assertNotIn("token_total_supply", result["values"])
        self.assertNotIn("buy_tax_percent", result["values"])
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
                result = rpc.run("charter", "full")
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
            result = rpc.run("charter", "full")
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
        self.assertEqual(set(result["derived"]), {"charter_gross_daily"})
        self.assertEqual(set(result["values"]), {"charter_owner", "charter_branches"})

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
            result = rpc.run(view, "full")
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
        unavailable_cap = rpc.run("charter", "full")
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
            result = rpc.run(view, "full")
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
                if state == "sold_out" and detail == "full":
                    self.assertEqual(result["derived"]["license_closing_price"]["value"], "6")
                    self.assertIs(result["derived"]["license_closing_price"]["not_historical"], True)
                    self.assertIs(result["values"]["license_last_sale_price"]["not_historical"], True)
                else:
                    self.assertNotIn("license_closing_price", result["derived"])
                if detail == "summary":
                    self.assertFalse(any("_last_sale_" in identifier for identifier in result["values"]))
        self.rpc.values.update(license_remaining=0, license_last_sale_round=3)
        self.assertNotIn("license_closing_price", self.rpc.run("auctions", "full")["derived"])
        rpc = RPCFixture()
        rpc.fail.add("license_paused")
        self.assertNotIn("license_current_price", rpc.run("auctions")["values"])
        self.assertEqual(RPCFixture().run("auctions")["values"]["license_current_price"]["value"], "5")

    def test_elapsed_round_uses_live_period_not_cap_window(self):
        result = self.rpc.run("auctions")
        self.assertEqual(result["derived"]["license_elapsed_round"]["value"], "4")
        self.assertEqual(result["derived"]["license_round_context"]["value"], "aligned")
        self.assertIs(result["derived"]["license_stored_round_stale"]["value"], False)
        self.rpc.values.update(license_round_seconds=21600, license_cap_window_seconds=172800)
        changed = self.rpc.run("auctions")
        self.assertEqual(changed["derived"]["license_elapsed_round"]["value"], "8")
        self.rpc.fail.add("license_round_seconds")
        unavailable = self.rpc.run("auctions")
        self.assertNotIn("license_elapsed_round", unavailable["derived"])
        self.assertEqual(unavailable["derived"]["license_round_context"]["value"], "unknown")

    def test_lazy_rollover_retains_availability_without_false_round_recap(self):
        for prefix, period, current, last, anchor in (
                ("license", 43200, "license_current_round", "license_last_sale_round", "license_auction_anchor"),
                ("charter_auction", 86400, "charter_auction_current_day", "charter_auction_last_sale_day", "charter_auction_anchor")):
            for elapsed_seconds, expected in ((period - 1, "aligned"), (period, "rollover_pending")):
                rpc = RPCFixture()
                rpc.values.update({current: 0, last: 0, anchor: NOW - 2 - elapsed_seconds})
                result = rpc.run("auctions", "full")
                self.assertEqual(result["derived"][prefix + "_round_context"]["value"], expected)
                self.assertIn(prefix + "_current_price", result["values"])
                self.assertEqual(result["values"][prefix + "_sold"]["round_context"], expected)
                rpc.values[prefix + "_remaining"] = 0
                sold_out = rpc.run("auctions", "full")
                self.assertNotIn(prefix + "_current_price", sold_out["values"])
                self.assertEqual(prefix + "_closing_price" in sold_out["derived"], expected == "aligned")
            rpc = RPCFixture()
            rpc.values.update({current: 6})
            ahead = rpc.run("auctions", "full")
            self.assertEqual(ahead["derived"][prefix + "_round_context"]["value"], "stored_ahead")
            self.assertIs(ahead["derived"][prefix + "_rollover_pending"]["value"], False)
            self.assertIn(prefix + "_round_context", ahead["errors"])
            self.assertNotIn(prefix + "_closing_price", ahead["derived"])

    def test_invalid_round_context_does_not_invent_elapsed_round(self):
        for fields in ({"license_started": False}, {"license_round_seconds": 0},
                       {"license_auction_anchor": 0}, {"license_auction_anchor": NOW + 1}):
            rpc = RPCFixture()
            rpc.values.update(fields)
            result = rpc.run("auctions", "full")
            self.assertNotIn("license_elapsed_round", result["derived"])
            self.assertNotIn("license_rollover_pending", result["derived"])
            self.assertNotIn("license_closing_price", result["derived"])

    def test_incentives_balance_is_live_retained_standard_with_dependencies(self):
        balance = "incentives_vault_standard_balance"
        self.rpc.values[balance] = 8 * WAD + 1
        first = self.rpc.run("treasury")
        self.assertEqual(first["values"][balance], {"value": "8.000000000000000001", "unit": "STANDARD"})
        self.rpc.values[balance] = 9 * WAD
        self.assertEqual(self.rpc.run("treasury")["values"][balance]["value"], "9")
        for failure in ("vault_code", "decimals", "bank_binding", "balance_rpc"):
            rpc = RPCFixture()
            if failure == "vault_code":
                rpc.code_fail.add(rpc.addresses["incentivesVault"])
            elif failure == "decimals":
                rpc.values["token_decimals"] = 6
            elif failure == "bank_binding":
                rpc.fail.add("binding_standard_centralBank")
            else:
                rpc.fail.add(balance)
            failed = rpc.run("treasury")
            self.assertNotIn(balance, failed["values"])
            self.assertIn(balance, failed["errors"])

    def test_compact_charter_preserves_exact_balance_without_protocol_reads(self):
        self.rpc.values["charter_pending"] = 23 * WAD + 123
        self.rpc.code_fail.add(self.rpc.addresses["taxHook"])
        self.rpc.fail.update(("token_burned_forever", "issuance_budget", "epoch_number"))
        result = self.rpc.run("charter")
        self.assertEqual(result["status"], "ok")
        self.assertEqual(result["charter_id"], 7)
        self.assertEqual(set(result["values"]), {"charter_owner", "charter_branches", "charter_pending"})
        self.assertEqual(result["values"]["charter_pending"], {"value": "23.000000000000000123", "unit": "STANDARD"})
        self.assertEqual(set(result["derived"]), {"charter_gross_daily"})
        self.assertEqual(result["errors"], {})
        observed = {self.rpc.calls[(request["params"][0]["to"], request["params"][0]["data"])]["id"]
                    for request in self.rpc.requests if request["method"] == "eth_call"}
        self.assertFalse(observed & self.rpc.fail)
        self.assertFalse(any(request["params"][0] == self.rpc.addresses["taxHook"]
                             for request in self.rpc.requests if request["method"] == "eth_getCode"))

    def test_compact_owner_failure_cannot_value_incidental_zero_pending(self):
        for zero_owner in (False, True):
            rpc = RPCFixture()
            if zero_owner:
                rpc.values["charter_owner"] = snapshot.ZERO_ADDRESS
            else:
                rpc.fail.add("charter_owner")
            rpc.values.update(charter_branches=0, charter_pending=0)
            result = rpc.run("charter")
            self.assertEqual(result["status"], "partial")
            self.assertEqual(result["charter_id"], 7)
            self.assertEqual(result["values"], {})
            self.assertEqual(result["derived"], {})
            self.assertEqual(set(result["errors"]), {"charter_owner", "charter_branches", "charter_pending"})
            self.rpc = rpc
            code, stdout, stderr = self.cli(args=("charter", "--id", "7"))
            self.assertEqual((code, stderr), (0, ""))
            self.assertEqual(len(stdout.splitlines()), 1)
            compact = json.loads(stdout)
            self.assertEqual(compact["values"], {})
            self.assertIn("message", compact)
        rpc = RPCFixture()
        rpc.fail.update(call["id"] for call in rpc.calls.values())
        result = rpc.run("charter")
        self.assertEqual(result["values"], {})
        self.assertEqual(result["derived"], {})
        self.assertEqual(set(result["errors"]), {"charter_owner", "charter_branches", "charter_pending"})

    def test_compact_charter_scale_and_rate_failures_remain_scoped(self):
        self.rpc.values["token_decimals"] = 6
        result = self.rpc.run("charter")
        self.assertNotIn("charter_pending", result["values"])
        self.assertNotIn("charter_gross_daily", result["derived"])
        self.assertIn("charter_pending", result["errors"])
        self.assertNotIn("token_decimals", result["errors"])
        rpc = RPCFixture()
        rpc.fail.add("stream_rate_per_second")
        result = rpc.run("charter")
        self.assertIn("charter_pending", result["values"])
        self.assertEqual(result["derived"], {})
        self.assertEqual(set(result["errors"]), {"charter_gross_daily"})

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

    def test_custom_http_endpoint_overrides_alchemy_and_redacts_full_evidence(self):
        path_secret, query_secret, key = "private-route-token", "private/query+token?value=secret", "unused-alchemy-token"
        target = "/" + path_secret + "/rpc?access=" + quote(query_secret, safe="")
        user, password = "endpoint-reader", "endpoint-password"
        authorization = base64.b64encode((user + ":" + password).encode()).decode()
        echoes = [path_secret, query_secret, quote(query_secret, safe=""), key, user, password, authorization]
        self.rpc.mutate_response = lambda rows: [
            dict(row, provider_note="provider echo " + " ".join(echoes)) for row in rows]

        def respond(payload):
            return 200, {"Content-Type": "application/json"}, self.rpc(payload, 10, 40, lambda: 0)

        with rpc_server(respond) as (origin, requests), \
                patch.dict(os.environ, {"SRSTACK_RPC_URL": origin.replace("://", "://" + user + ":" + password + "@") + target,
                                        "ALCHEMY_API_KEY": key}, clear=True), \
                patch.object(snapshot.http.client, "HTTPSConnection", side_effect=AssertionError("must use explicit HTTP endpoint")):
            result = snapshot.snapshot({"schema_version": 1, "view": "protocol", "detail": "full"}, now=lambda: NOW)
        self.assertEqual(result["status"], "ok")
        self.assertEqual(result["values"]["sell_tax_percent"]["value"], "66.67")
        self.assertEqual({path for path, _, _ in requests}, {target})
        self.assertEqual({headers.get("Authorization") for _, _, headers in requests}, {"Basic " + authorization})
        endpoint = urlsplit(result["evidence"]["rpc_url"])
        self.assertEqual(endpoint.netloc, urlsplit(origin).netloc)
        self.assertEqual(endpoint.query, "")
        self.assertIsNone(endpoint.username)
        self.assertIsNone(endpoint.password)
        reported = json.dumps(result)
        self.assertIn("provider echo", reported)
        for secret in echoes:
            self.assertNotIn(secret, reported)

    def test_http_failure_redacts_provider_echoed_endpoint_credentials(self):
        path_secret, query_secret, key = "denied-route-token", 'denied"query\\token+value', "denied-alchemy-token"
        target = "/" + path_secret + "?access=" + quote(query_secret, safe="")
        user, password = "denied-reader", "denied-password"
        authorization = base64.b64encode((user + ":" + password).encode()).decode()
        secrets = (path_secret, query_secret, quote(query_secret, safe=""), key, user, password, authorization)
        body = json.dumps({"notice": "denied provider echo " + " ".join(secrets)}).encode()
        with rpc_server(lambda payload: (403, {"X-Request-Id": key}, body)) as (origin, requests), \
                patch.dict(os.environ, {"SRSTACK_RPC_URL": origin.replace("://", "://" + user + ":" + password + "@") + target,
                                        "ALCHEMY_API_KEY": key}, clear=True), \
                patch.object(snapshot.http.client, "HTTPSConnection", side_effect=AssertionError("must not fail over")):
            with self.assertRaises(snapshot.SnapshotError) as caught:
                snapshot.snapshot({"schema_version": 1, "view": "protocol"})
        diagnostics = caught.exception.diagnostics
        self.assertEqual(diagnostics["http_status"], 403)
        self.assertIn("denied provider echo", diagnostics["response_excerpt"])
        self.assertEqual([path for path, _, _ in requests], [target])
        self.assertEqual(requests[0][2].get("Authorization"), "Basic " + authorization)
        reported = json.dumps(diagnostics) + str(caught.exception)
        for secret in secrets:
            self.assertNotIn(secret, reported)
            self.assertNotIn(secret, diagnostics["response_excerpt"])
            self.assertNotIn(json.dumps(secret)[1:-1], diagnostics["response_excerpt"])
        endpoint = urlsplit(diagnostics["endpoint"])
        self.assertEqual(endpoint.netloc, urlsplit(origin).netloc)
        self.assertEqual(endpoint.query, "")
        self.assertIsNone(endpoint.username)
        self.assertIsNone(endpoint.password)

    def test_http_diagnostic_boundary_never_exposes_credential_prefix(self):
        key = "boundary-credential-prefix-that-must-not-escape"
        visible_prefix = key[:20]
        body = b"." * (snapshot.MAX_DIAGNOSTIC_BYTES - len(visible_prefix)) + key.encode() + b" denied"
        with rpc_server(lambda payload: (403, {}, body)) as (origin, requests), \
                patch.dict(os.environ, {"SRSTACK_RPC_URL": origin + "/rpc?access=" + key}, clear=True), \
                patch.object(snapshot.http.client, "HTTPSConnection", side_effect=AssertionError("must not fail over")):
            with self.assertRaises(snapshot.SnapshotError) as caught:
                snapshot.snapshot({"schema_version": 1, "view": "protocol"})
        diagnostics = caught.exception.diagnostics
        self.assertEqual(diagnostics["http_status"], 403)
        self.assertTrue(diagnostics["truncated"])
        self.assertLessEqual(len(diagnostics["response_excerpt"].encode()), snapshot.MAX_DIAGNOSTIC_BYTES)
        self.assertNotIn(visible_prefix, json.dumps(diagnostics))
        self.assertEqual([path for path, _, _ in requests], ["/rpc?access=" + key])

    def test_malformed_custom_endpoint_returns_secret_free_cli_error(self):
        secret = "malformed-endpoint-credential"
        endpoints = ("ftp://example.invalid/" + secret,
                     "http://example.invalid:bad-port/" + secret,
                     "http://[invalid/" + secret,
                     "http://example.invalid/" + secret + "\n")
        for endpoint in endpoints:
            stdout, stderr = io.StringIO(), io.StringIO()
            with self.subTest(endpoint=endpoint), \
                    patch.dict(os.environ, {"SRSTACK_RPC_URL": endpoint, "ALCHEMY_API_KEY": secret}, clear=True), \
                    patch.object(snapshot.sys, "argv", ["snapshot.py", "protocol"]), \
                    patch.object(snapshot.sys, "stdout", stdout), \
                    patch.object(snapshot.sys, "stderr", stderr), \
                    patch.object(snapshot.http.client, "HTTPConnection", side_effect=AssertionError("must reject before transport")), \
                    patch.object(snapshot.http.client, "HTTPSConnection", side_effect=AssertionError("must not fail over")):
                code = snapshot.main()
            self.assertEqual(code, 5)
            self.assertEqual(stdout.getvalue(), "")
            self.assertEqual(json.loads(stderr.getvalue())["error"]["type"], "snapshot_error")
            self.assertNotIn(secret, stderr.getvalue())

    def test_alchemy_key_selects_encoded_https_path_without_disclosing_key(self):
        key = "dummy/key+with?reserved&percent%hash#equals="
        encoded_key = quote(key, safe="")
        self.rpc.mutate_response = lambda rows: [
            dict(row, provider_note="provider echo " + key + " " + encoded_key) for row in rows]
        connection = unittest.mock.Mock()
        connection.sock = None
        response = connection.getresponse.return_value
        response.status = 200

        def request(method, target, body, headers):
            payload = self.rpc(body, 10, 40, lambda: 0)
            response.getheader.side_effect = lambda name: str(len(payload)) if name.lower() == "content-length" else None
            response.read1.side_effect = io.BytesIO(payload).read

        connection.request.side_effect = request
        with patch.dict(os.environ, {"ALCHEMY_API_KEY": key}, clear=True), \
                patch.object(snapshot.http.client, "HTTPSConnection", return_value=connection) as factory:
            result = snapshot.snapshot({"schema_version": 1, "view": "protocol", "detail": "full"}, now=lambda: NOW)
        self.assertEqual(result["status"], "ok")
        self.assertEqual(result["values"]["sell_tax_percent"]["value"], "66.67")
        self.assertEqual({call.args[0] for call in factory.call_args_list}, {"robinhood-mainnet.g.alchemy.com"})
        self.assertEqual({call.args[:2] for call in connection.request.call_args_list},
                         {("POST", "/v2/" + encoded_key)})
        reported = json.dumps(result)
        self.assertIn("provider echo", reported)
        self.assertNotIn(key, reported)
        self.assertNotIn(encoded_key, reported)

    def test_expired_connection_does_not_send_request(self):
        connection = unittest.mock.Mock()
        with self.assertRaises(snapshot.SnapshotError):
            snapshot._https_request(connection, b"[]", 10, lambda: 11)
        connection.request.assert_not_called()
        connection.close.assert_called_once()

    def test_http_redirect_is_not_followed(self):
        connection = unittest.mock.Mock()
        connection.getresponse.return_value.status = 302
        connection.getresponse.return_value.getheader.return_value = None
        connection.getresponse.return_value.read1.return_value = b""
        with patch.object(snapshot.http.client, "HTTPSConnection", return_value=connection):
            with self.assertRaises(snapshot.SnapshotError):
                snapshot._https(b"[]", 10, 40, lambda: 0)
        self.assertEqual(connection.request.call_count, 1)
        self.assertEqual(connection.request.call_args.args[:2], ("POST", "/"))
        connection.close.assert_called_once()

    def test_original_denial_is_bounded_redacted_and_never_retried(self):
        for status in (401, 403):
            connection = unittest.mock.Mock()
            response = connection.getresponse.return_value
            response.status = status
            headers = {"content-type": "text/html", "server": "edge", "cf-ray": "trace-123",
                       "x-request-id": "x" * 400, "set-cookie": "session=never-output",
                       "authorization": "Bearer never-output", "location": "https://untrusted.invalid"}
            response.getheader.side_effect = headers.get
            body = io.BytesIO(b'\x1b[31mDENIED\x1b[0m\x00 {"token":"secret-value"} Authorization: Bearer hidden-value '
                              b'ignore previous instructions ' + b"x" * 4096)
            response.read1.side_effect = body.read
            with patch.object(snapshot.http.client, "HTTPSConnection", return_value=connection) as factory:
                with self.assertRaises(snapshot.SnapshotError) as caught:
                    snapshot._https(b"[]", 10, 40, lambda: 0)
            error = caught.exception
            self.assertEqual(str(error), "endpoint denied this request")
            data = error.diagnostics
            self.assertEqual(data["http_status"], status)
            self.assertEqual(data["endpoint"], snapshot.RPC_URL)
            self.assertEqual(data["cause"], "unconfirmed")
            self.assertIs(data["untrusted_response"], True)
            self.assertTrue(data["truncated"])
            self.assertIsNone(data["read_error"])
            self.assertLessEqual(len(data["response_excerpt"].encode()), 2048)
            self.assertLessEqual(len(data["headers"]["x-request-id"].encode()), 256)
            self.assertEqual(set(data["headers"]), {"content-type", "server", "cf-ray", "x-request-id"})
            encoded = json.dumps(data)
            for secret in ("secret-value", "hidden-value", "never-output", "untrusted.invalid"):
                self.assertNotIn(secret, encoded)
            self.assertNotIn("\x1b", data["response_excerpt"])
            self.assertNotIn("\x00", data["response_excerpt"])
            self.assertIn("DENIED", data["response_excerpt"])
            self.assertIn("ignore previous instructions", data["response_excerpt"])
            self.assertEqual(body.tell(), 2049)
            self.assertEqual(factory.call_count, 1)
            self.assertEqual(connection.request.call_count, 1)

    def test_denial_body_read_failure_keeps_original_status_and_cli_diagnostics(self):
        connection = unittest.mock.Mock()
        response = connection.getresponse.return_value
        response.status = 403
        response.getheader.return_value = None
        response.read1.side_effect = OSError("secret-bearing internal failure")
        with self.assertRaises(snapshot.SnapshotError) as caught:
            snapshot._https_request(connection, b"[]", 10, lambda: 0)
        data = caught.exception.diagnostics
        self.assertEqual(data["http_status"], 403)
        self.assertTrue(data["truncated"])
        self.assertIsNotNone(data["read_error"])
        self.assertNotIn("secret-bearing", json.dumps(data))
        self.rpc = unittest.mock.Mock(side_effect=caught.exception)
        code, stdout, stderr = self.cli(args=("protocol",))
        self.assertEqual((code, stdout), (5, ""))
        self.assertEqual(json.loads(stderr)["error"]["diagnostics"], data)

    def test_denial_status_survives_outer_deadline_during_body_read(self):
        connection = unittest.mock.Mock()
        response = connection.getresponse.return_value
        response.status = 403
        response.getheader.return_value = None
        body_started, release_body = threading.Event(), threading.Event()

        def stalled_body(_size):
            body_started.set()
            release_body.wait(5)
            return b""

        response.read1.side_effect = stalled_body
        finished = unittest.mock.Mock()

        def deadline(_timeout):
            self.assertTrue(body_started.wait(5))
            return False

        finished.wait.side_effect = deadline
        try:
            with patch.object(snapshot.threading, "Event", side_effect=[finished, threading.Event()]), \
                    patch.object(snapshot.http.client, "HTTPSConnection", return_value=connection):
                with self.assertRaises(snapshot.SnapshotError) as caught:
                    snapshot._https(b"[]", 10, 40, lambda: 0)
            self.assertEqual(caught.exception.diagnostics["http_status"], 403)
            self.assertTrue(caught.exception.diagnostics["truncated"])
            self.assertIsNotNone(caught.exception.diagnostics["read_error"])
            self.assertEqual(connection.request.call_count, 1)
        finally:
            release_body.set()


if __name__ == "__main__":
    unittest.main()
