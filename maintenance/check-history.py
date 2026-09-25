#!/usr/bin/env python3
"""Deterministic event-accounting and bounded-coverage regressions; no live RPC."""

import copy
from functools import partial
import importlib.util
import io
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

ROOT = Path(__file__).resolve().parent.parent
SPEC = importlib.util.spec_from_file_location("sr_history", ROOT / "scripts/history.py")
history = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(history)
S = history._load_snapshot()
NOW = 1_789_500_000


def block_hash(number):
    return "0x" + format(number + 1, "064x")


class RPCFixture:
    """Encode tiny invented events from reviewed ABI definitions, never observations."""

    def __init__(self, auction="license"):
        self.catalog, interface, addresses, _ = history._load_catalog(S, auction)
        self.role = "licenseAuctionLegacy" if auction == "license" else history.ROLES[auction]
        self.auction = auction
        self.address = addresses[self.role]
        self.addresses = addresses
        self.definitions = {e["abi"]["name"]: e for e in self.catalog["events"] if self.role in e["contracts"]}
        self.logs, self.requests = [], []
        self.start_block = self.catalog["contracts"][self.role].get("deployment_block", 0) + 100
        self.head = self.start_block + 1_999_900
        self.chain_id, self.code = S.CHAIN_ID, "0x6000"
        self.standard_address = addresses["standard"]
        self.binding_address, self.standard_decimals, self.standard_code = self.standard_address, 18, "0x6000"
        self.deny_binding = False
        self.call_definitions = {(addresses[call["contract"]], call["selector"]): call for call in interface["calls"]
                                 if (call["contract"], call["signature"]) in (("contractionVault", "standard()"), ("standard", "decimals()"))}
        self.headers_read = {}
        self.header_mutation = None
        self.logs_mutation = None
        self.denied_from = None
        self.clock = 0
        self.expire_on_logs = False
        self.diagnostics = {"endpoint": S.RPC_URL, "http_status": 403, "headers": {"content-type": "text/plain"},
                            "response_excerpt": "fixture access denial", "excerpt_bytes": 21, "truncated": False,
                            "read_error": None, "untrusted_response": True, "cause": "unconfirmed"}

    def add(self, name, block=None, index=0, **fields):
        block = self.start_block + 2 if block is None else block
        definition = self.definitions[name]
        topics, words = [definition["topic0"]], []
        for item in definition["abi"]["inputs"]:
            value = fields[item["name"]]
            word = format(int(value, 16) if isinstance(value, str) else value, "064x")
            (topics if item["indexed"] else words).append("0x" + word if item["indexed"] else word)
        event = {"address": self.address, "blockNumber": hex(block), "blockHash": block_hash(block),
                 "transactionHash": "0x" + format(10_000_000 + block * 100 + index, "064x"),
                 "transactionIndex": hex(index), "logIndex": hex(index), "topics": topics,
                 "data": "0x" + "".join(words), "removed": False}
        self.logs.append(event)
        return event

    def purchase(self, day=7, count=1, price=1, block=102, index=0):
        if self.auction == "license":
            return self.add("LicensesPurchased", block, index, charterId=1, day=day, count=count, unitPrice=price)
        return self.add("CharterPurchased", block, index, charterId=index + 1, buyer="0x" + "12" * 20, day=day, price=price)

    def __call__(self, payload, timeout, deadline, monotonic):
        requests = json.loads(payload)
        response = []
        for request in requests:
            self.requests.append(request)
            method, params = request["method"], request["params"]
            if method == "eth_chainId":
                result = hex(self.chain_id)
            elif method == "eth_getCode":
                if self.auction == "license" and params[0] == self.addresses["licenseAuction"] and int(params[1], 16) < self.catalog["contracts"]["licenseAuction"]["deployment_block"]:
                    result = "0x"
                else:
                    result = self.standard_code if params[0] == self.standard_address else self.code
            elif method == "eth_call":
                if self.auction != "buybacks":
                    raise AssertionError("auction history cannot issue state calls")
                if self.deny_binding:
                    raise S.SnapshotError("RPC HTTP request failed", diagnostics=self.diagnostics)
                if params[1] != hex(119):
                    raise AssertionError("buyback binding must use the exact scan anchor")
                call = self.call_definitions[(params[0]["to"], params[0]["data"])]
                value = int(self.binding_address, 16) if call["signature"] == "standard()" else self.standard_decimals
                result = "0x" + format(value, "064x")
            elif method == "eth_getBlockByNumber":
                number = self.head if params[0] == "latest" else int(params[0], 16)
                self.headers_read[number] = self.headers_read.get(number, 0) + 1
                result = {"number": hex(number), "hash": block_hash(number), "timestamp": hex(NOW - self.head + number)}
                if self.header_mutation:
                    result = self.header_mutation(number, self.headers_read[number], result)
            elif method == "eth_getLogs":
                start, end = int(params[0]["fromBlock"], 16), int(params[0]["toBlock"], 16)
                if self.denied_from is not None and start >= self.denied_from:
                    raise S.SnapshotError("RPC HTTP request failed", diagnostics=self.diagnostics)
                result = copy.deepcopy([e for e in self.logs if start <= int(e["blockNumber"], 16) <= end])
                if self.logs_mutation:
                    result = self.logs_mutation(start, end, result)
                if self.expire_on_logs:
                    self.clock = history.OVERALL_TIMEOUT + 1
            else:
                raise AssertionError("unexpected non-history RPC method: " + method)
            response.append({"jsonrpc": "2.0", "id": request["id"], "result": result})
        return json.dumps(list(reversed(response))).encode()

    def run(self, **options):
        config = {"schema_version": 1, "kind" if self.auction in history.BUYBACK_KINDS else "auction": self.auction,
                  "from_block": self.start_block, "to_block": self.start_block + 19, "chunk_blocks": 10}
        config.update(options)
        return history.history(config, transport=self, now=lambda: NOW, monotonic=lambda: self.clock)

    def windows(self):
        return [(int(r["params"][0]["fromBlock"], 16), int(r["params"][0]["toBlock"], 16)) for r in self.requests if r["method"] == "eth_getLogs"]


class HistoryChecks(unittest.TestCase):
    def test_final_anchor_denial_marks_rounds_incomplete(self):
        fixture = RPCFixture()
        fixture.purchase(count=2, price=9)
        def mutation(number, count, header):
            if number == 119 and count == 5:
                raise S.SnapshotError("RPC HTTP request failed", diagnostics=fixture.diagnostics)
            return header
        fixture.header_mutation = mutation
        report = fixture.run()
        self.assertEqual(report["status"], "partial")
        self.assertEqual(report["coverage"]["missing"], [])
        self.assertEqual(report["rounds"][0]["purchase_quantity"], "2")
        self.assertIn("requested_window_has_coverage_gaps", report["rounds"][0]["gaps"])
        self.assertEqual(report["errors"]["final_anchor"]["diagnostics"], fixture.diagnostics)

    def test_quantity_weighted_multiple_license_purchases(self):
        fixture = RPCFixture()
        fixture.purchase(count=2, price=9)
        fixture.purchase(count=3, price=2, block=112)
        report = fixture.run()
        self.assertEqual(report["status"], "ok")
        row = report["rounds"][0]
        self.assertEqual((row["purchase_quantity"], row["purchase_event_count"]), ("5", 2))
        self.assertEqual(row["consideration"]["total_raw"], "24")
        self.assertEqual(row["consideration"]["quantity_weighted_average_raw"], {"numerator": "24", "denominator": "5"})
        self.assertEqual(row["consideration"]["asset"], "STANDARD")
        self.assertEqual(row["first_observed_purchase"]["block_number"], 102)
        self.assertEqual(row["last_observed_purchase"]["block_number"], 112)
        self.assertFalse(row["complete_round"])
        self.assertEqual(row["sellout"], "not_established")

    def test_charter_consideration_is_one_quantity_per_event(self):
        fixture = RPCFixture("charter")
        fixture.purchase(price=3)
        fixture.purchase(price=5, block=112)
        row = fixture.run()["rounds"][0]
        self.assertEqual(row["purchase_quantity"], "2")
        self.assertEqual(row["consideration"]["asset"], "ETH")
        self.assertEqual(row["consideration"]["total_raw"], "8")
        self.assertEqual(row["consideration"]["quantity_weighted_average_raw"], {"numerator": "4", "denominator": "1"})

    def test_round_prices_preserve_units_precision_and_last_observed_execution(self):
        for auction, asset in (("license", "STANDARD"), ("charter", "ETH")):
            with self.subTest(auction=auction):
                fixture = RPCFixture(auction)
                start, floor, last = 3 * 10**18 + 7, 10**18 + 1, 2 * 10**18 + 9
                fixture.add("DayRolled", block=101, day=7, startPrice=start, floorPrice=floor, cap=200)
                fixture.purchase(day=7, price=start, block=102)
                fixture.purchase(day=7, price=last, block=112)
                row = fixture.run()["rounds"][0]
                roll = row["observed_rolls"][0]
                self.assertEqual(roll["reported_cap"], "200")
                self.assertEqual(roll["reported_start_price"],
                                 {"asset": asset, "decimals": 18, "raw": str(start), "scaled18": "3.000000000000000007"})
                self.assertEqual(roll["reported_floor_price"],
                                 {"asset": asset, "decimals": 18, "raw": str(floor), "scaled18": "1.000000000000000001"})
                self.assertEqual(row["last_observed_purchase"]["unit_price"],
                                 {"asset": asset, "decimals": 18, "raw": str(last), "scaled18": "2.000000000000000009"})
                self.assertEqual(row["last_observed_purchase"]["block_number"], 112)
                self.assertFalse(row["complete_round"])
                self.assertEqual(row["sellout"], "not_established")

    def test_last_rounds_select_observed_recency_per_generation_and_filter_full_events(self):
        fixture = RPCFixture()
        deployment = fixture.catalog["contracts"]["licenseAuction"]["deployment_block"]
        fixture.head = deployment + 20
        current = fixture.addresses["licenseAuction"]
        for role_address in (fixture.address, current):
            offset = 0 if role_address == fixture.address else 1
            for day, delta in ((99, 1), (2, 3), (5, 5)):
                fixture.purchase(day=day, block=deployment + delta + offset)["address"] = role_address
        fixture.add("LicensesPerDaySet", block=deployment + 8, count=123)
        report = fixture.run(from_block=deployment, to_block=deployment + 9, last_rounds=2, detail="full")
        self.assertEqual(report["status"], "ok")
        for address in (fixture.address, current):
            self.assertEqual([row["day"] for row in report["rounds"] if row["address"] == address], ["5", "2"])
        selection = report["coverage"]["round_selection"]
        self.assertEqual(selection["requested_per_generation"], 2)
        self.assertEqual([(row["observed_rounds"], row["selected_rounds"], row["shortfall"])
                          for row in selection["generations"]], [(3, 2, 0), (3, 2, 0)])
        self.assertEqual([(event["address"], event["fields"]["day"]) for event in report["evidence"]["decoded_events"]],
                         [(fixture.address, 2), (current, 2), (fixture.address, 5), (current, 5)])
        self.assertEqual(fixture.windows(), [(deployment, deployment + 9)])

    def test_current_only_scopes_queries_and_keeps_empty_predeployment_coverage(self):
        fixture = RPCFixture()
        deployment = fixture.catalog["contracts"]["licenseAuction"]["deployment_block"]
        fixture.head = deployment + 20
        current = fixture.addresses["licenseAuction"]
        fixture.purchase(day=0, block=deployment + 1)["address"] = current
        report = fixture.run(from_block=deployment - 1, to_block=deployment + 3,
                             generation="current", last_rounds=1)
        self.assertEqual(report["status"], "ok")
        self.assertEqual(report["coverage"]["completed"][0]["scan_status"], "no_deployed_emitters")
        self.assertEqual(report["coverage"]["completed"][0]["emitter_addresses"], [])
        self.assertEqual(fixture.windows(), [(deployment, deployment + 3)])
        self.assertEqual([r["params"][0] for r in fixture.requests if r["method"] == "eth_getCode"], [current])
        self.assertEqual([r["params"][0]["address"] for r in fixture.requests if r["method"] == "eth_getLogs"], [current])
        self.assertEqual(set(report["evidence"]["license_generations"]), {"licenseAuction"})
        self.assertEqual(report["rounds"][0]["address"], current)

    def test_shortfall_is_not_a_scan_gap_or_invented_zero_sale_round(self):
        fixture = RPCFixture()
        fixture.add("DayRolled", day=8, startPrice=10, floorPrice=2, cap=200)
        report = fixture.run(generation="legacy", last_rounds=3, detail="full")
        self.assertEqual(report["status"], "partial")
        self.assertEqual(report["errors"], {})
        self.assertEqual(report["coverage"]["missing"], [])
        self.assertEqual([row["day"] for row in report["rounds"]], ["8"])
        self.assertIsNone(report["rounds"][0]["last_observed_purchase"])
        self.assertNotIn("requested_window_has_coverage_gaps", report["rounds"][0]["gaps"])
        selection = report["coverage"]["round_selection"]["generations"][0]
        self.assertEqual((selection["observed_rounds"], selection["selected_rounds"], selection["shortfall"]), (1, 1, 2))
        self.assertEqual(selection["status"], "insufficient_observed_rounds")
        empty = RPCFixture().run(generation="legacy", last_rounds=3)
        self.assertEqual(empty["rounds"], [])
        self.assertEqual(empty["coverage"]["round_selection"]["generations"][0]["shortfall"], 3)

    def test_last_rounds_preserve_scan_budget_gaps_even_with_enough_observed_rows(self):
        fixture = RPCFixture()
        fixture.purchase(day=7)
        fixture.purchase(day=8, block=112)
        report = fixture.run(generation="legacy", last_rounds=1, max_chunks=1, detail="full")
        self.assertEqual(report["status"], "partial")
        self.assertEqual([row["day"] for row in report["rounds"]], ["7"])
        self.assertEqual(report["coverage"]["round_selection"]["generations"][0]["shortfall"], 0)
        self.assertEqual(report["coverage"]["missing"][0]["from_block"], 110)
        self.assertIn("requested_window_has_coverage_gaps", report["rounds"][0]["gaps"])
        self.assertEqual(fixture.windows(), [(100, 109)])

    def test_last_rounds_default_stays_a_finite_lookback_not_deployment_history(self):
        fixture = RPCFixture()
        fixture.purchase(day=1, block=fixture.head - history.DEFAULT_LOOKBACK)
        fixture.purchase(day=2, block=fixture.head - 1)
        report = history.history({"schema_version": 1, "auction": "license", "generation": "legacy", "last_rounds": 2},
                                 transport=fixture, now=lambda: NOW, monotonic=lambda: 0)
        self.assertEqual(report["status"], "partial")
        self.assertEqual(report["coverage"]["requested"],
                         {"from_block": fixture.head - history.DEFAULT_LOOKBACK + 1, "to_block": fixture.head})
        self.assertEqual([row["day"] for row in report["rounds"]], ["2"])
        self.assertEqual(report["coverage"]["missing"], [])
        self.assertEqual(fixture.windows()[-1][1], fixture.head)

    def test_day_full_events_exclude_other_rounds_and_roundless_configuration(self):
        fixture = RPCFixture()
        fixture.purchase(day=7)
        fixture.purchase(day=9, block=112)
        fixture.add("LicensesPerDaySet", block=113, count=999)
        report = fixture.run(day=9, detail="full")
        self.assertEqual([(event["event"], event["fields"]["day"]) for event in report["evidence"]["decoded_events"]],
                         [("LicensesPurchased", 9)])

    def test_last_rounds_and_generation_reject_ambiguous_or_unsupported_selection(self):
        for arguments in (["license", "--last-rounds", "0"], ["license", "--last-rounds", "1001"],
                          ["license", "--last-rounds", "1", "--day", "7"],
                          ["buybacks", "--last-rounds", "1"], ["pol-buybacks", "--last-rounds", "1"],
                          ["charter", "--generation", "current"], ["license", "--generation", "v2"]):
            with self.subTest(arguments=arguments), self.assertRaises(history.InputError):
                history._cli_config(arguments)
        fixture = RPCFixture()
        for value in (True, 1.5, "3"):
            with self.subTest(value=value), self.assertRaises(history.InputError):
                fixture.run(last_rounds=value)
        self.assertEqual(fixture.requests, [])

    def test_empty_million_block_default_has_no_synthetic_rounds(self):
        fixture = RPCFixture()
        report = history.history({"schema_version": 1, "auction": "license"}, transport=fixture, now=lambda: NOW, monotonic=lambda: 0)
        self.assertEqual(report["status"], "ok")
        self.assertEqual(report["rounds"], [])
        self.assertEqual(report["coverage"]["missing"], [])
        self.assertEqual(fixture.windows(), [(1_000_001 + n * 10_000, 1_010_000 + n * 10_000) for n in range(100)])
        self.assertEqual(report["coverage"]["requested"], {"from_block": 1_000_001, "to_block": 2_000_000})

    def test_day_filters_round_id_without_claiming_other_windows(self):
        fixture = RPCFixture()
        fixture.purchase(day=7)
        fixture.purchase(day=9, block=112)
        report = fixture.run(day=9)
        self.assertEqual([row["day"] for row in report["rounds"]], ["9"])
        self.assertEqual(report["coverage"]["day_filter"], "9")
        self.assertEqual(fixture.windows(), [(100, 109), (110, 119)])
        self.assertEqual(fixture.run(day=8)["rounds"], [])
        self.assertEqual([row["day"] for row in fixture.run()["rounds"]], ["7", "9"])

    def test_cap_is_only_the_round_named_by_roll(self):
        fixture = RPCFixture()
        fixture.add("AuctionStarted", day=7, startPrice=9)
        fixture.purchase(day=7, block=103)
        fixture.add("DayRolled", block=112, day=8, startPrice=10, floorPrice=2, cap=200)
        fixture.add("LicensesPerDaySet", block=113, count=999)
        rows = fixture.run()["rounds"]
        self.assertIsNone(rows[0]["reported_round_cap"])
        self.assertEqual(rows[1]["reported_round_cap"], "200")
        self.assertEqual(rows[1]["observed_rolls"][0]["block_number"], 112)
        self.assertIsNone(rows[1]["consideration"]["quantity_weighted_average_raw"])
        self.assertIsNone(rows[1]["scheduled_opening"])

    def test_chunk_exhaustion_preserves_committed_purchases_and_gap(self):
        fixture = RPCFixture()
        fixture.purchase(count=2)
        fixture.purchase(count=99, block=112)
        report = fixture.run(max_chunks=1)
        self.assertEqual(report["status"], "partial")
        self.assertEqual(report["rounds"][0]["purchase_quantity"], "2")
        self.assertEqual(fixture.windows(), [(100, 109)])
        self.assertEqual(report["coverage"]["completed"][0]["to_block"], 109)
        self.assertEqual(report["coverage"]["missing"][0]["from_block"], 110)
        self.assertEqual(report["coverage"]["missing"][0]["to_block"], 119)
        self.assertIn("requested_window_has_coverage_gaps", report["rounds"][0]["gaps"])

    def test_denial_is_original_diagnostic_and_never_followed_by_requests(self):
        fixture = RPCFixture()
        fixture.purchase()
        fixture.denied_from = 110
        report = fixture.run()
        self.assertEqual(report["status"], "partial")
        self.assertEqual(report["rounds"][0]["purchase_quantity"], "1")
        self.assertEqual(report["errors"]["window_110"]["diagnostics"], fixture.diagnostics)
        self.assertEqual(fixture.requests[-1]["method"], "eth_getLogs")
        self.assertEqual(fixture.windows(), [(100, 109), (110, 119)])
        self.assertEqual(report["coverage"]["missing"][0]["from_block"], 110)

    def test_removed_log_invalidates_prior_totals_even_when_response_hits_log_limits(self):
        for limit_name in ("MAX_WINDOW_LOGS", "MAX_LOGS"):
            with self.subTest(limit=limit_name), patch.object(history, limit_name, 2):
                fixture = RPCFixture()
                fixture.purchase()
                fixture.purchase(block=112)
                fixture.purchase(block=113, index=1)["removed"] = True
                report = fixture.run()
                self.assertEqual(report["status"], "partial")
                self.assertEqual(report["rounds"], [])
                self.assertEqual(report["coverage"]["completed"], [])
                self.assertEqual(report["coverage"]["missing"][0]["from_block"], 100)
                self.assertEqual(len(report["evidence"]["invalidated_windows"]), 1)
                self.assertEqual(fixture.requests[-1]["method"], "eth_getLogs")

    def test_live_request_pacing_respects_deadline_without_retry(self):
        clock, requests = [0.0], []
        def transport(payload, timeout, deadline, monotonic):
            requests.append(clock[0])
            return b"[]"
        budget = history._Budget(S, transport, lambda: clock[0], pace=True)
        def sleep(delay):
            clock[0] += delay
        payload = b'[{"jsonrpc":"2.0","id":1,"method":"eth_chainId","params":[]}]'
        with patch.object(history.time, "sleep", sleep):
            budget(payload, 10, budget.deadline, lambda: clock[0])
            budget(payload, 10, budget.deadline, lambda: clock[0])
            self.assertGreaterEqual(requests[1] - requests[0], history.MIN_REQUEST_INTERVAL)
            budget.deadline = clock[0] + history.MIN_REQUEST_INTERVAL / 2
            with self.assertRaises(S.SnapshotError):
                budget(payload, 10, budget.deadline, lambda: clock[0])
        self.assertEqual(len(requests), 2)

    def test_request_byte_log_and_time_budgets_stop_without_false_coverage(self):
        for budget_name, limit in (("MAX_REQUESTS", 10), ("MAX_TOTAL_BYTES", S.MAX_RESPONSE_BYTES), ("MAX_LOGS", 1)):
            with self.subTest(budget=budget_name), patch.object(history, budget_name, limit):
                fixture = RPCFixture()
                if budget_name == "MAX_LOGS":
                    fixture.purchase()
                    fixture.purchase(index=1)
                report = fixture.run()
                self.assertEqual(report["status"], "partial")
                self.assertEqual(report["rounds"], [])
                self.assertEqual(report["coverage"]["missing"][0]["from_block"], 110 if budget_name == "MAX_REQUESTS" else 100)
                self.assertIn("budget", next(iter(report["errors"].values()))["message"])
                if budget_name == "MAX_REQUESTS":
                    self.assertLessEqual(len(fixture.requests), limit)
        fixture = RPCFixture()
        fixture.expire_on_logs = True
        report = fixture.run()
        self.assertEqual(report["status"], "partial")
        self.assertEqual(report["coverage"]["completed"], [])
        self.assertEqual(fixture.windows(), [(100, 109)])

    def test_malformed_logs_never_enter_totals_or_skip_window(self):
        changes = {
            "wrong_emitter": lambda e: e.update(address="0x" + "34" * 20),
            "wrong_topic": lambda e: e["topics"].__setitem__(0, "0x" + "ab" * 32),
            "extra_topic": lambda e: e["topics"].append("0x" + "00" * 32),
            "short_data": lambda e: e.update(data=e["data"][:-2]),
            "invalid_position": lambda e: e.update(transactionIndex="0x00"),
            "zero_hash": lambda e: e.update(transactionHash="0x" + "00" * 32),
            "wrong_block_hash": lambda e: e.update(blockHash="0x" + "ab" * 32),
            "out_of_range": lambda e: e.update(blockNumber="0x99"),
            "removed": lambda e: e.update(removed=True),
        }
        for name, mutate in changes.items():
            with self.subTest(case=name):
                fixture = RPCFixture()
                fixture.purchase()
                def mutation(start, end, logs):
                    mutate(logs[0])
                    return logs
                fixture.logs_mutation = mutation
                report = fixture.run()
                self.assertEqual(report["status"], "partial")
                self.assertEqual(report["rounds"], [])
                self.assertEqual(report["coverage"]["completed"], [])
                self.assertEqual(fixture.windows(), [(100, 109)])

    def test_duplicate_and_conflicting_log_positions_are_not_double_counted(self):
        for conflict in (False, True):
            with self.subTest(conflict=conflict):
                fixture = RPCFixture()
                event = fixture.purchase()
                duplicate = copy.deepcopy(event)
                if conflict:
                    duplicate["transactionHash"] = "0x" + "aa" * 32
                fixture.logs.append(duplicate)
                report = fixture.run()
                self.assertEqual(report["status"], "partial")
                self.assertEqual(report["rounds"], [])
                self.assertEqual(report["coverage"]["completed"], [])

    def test_address_abi_padding_is_rejected(self):
        fixture = RPCFixture("charter")
        event = fixture.purchase()
        event["topics"][2] = "0x01" + event["topics"][2][4:]
        report = fixture.run()
        self.assertEqual(report["status"], "partial")
        self.assertEqual(report["rounds"], [])

    def test_used_header_recheck_and_later_anchor_reorg_invalidate(self):
        for used_header in (True, False):
            with self.subTest(used_header=used_header):
                fixture = RPCFixture()
                fixture.purchase()
                fixture.purchase(block=112)
                def mutate(number, count, header):
                    if (used_header and number == 102 and count == 2) or (not used_header and number == 119 and count >= 4):
                        header["hash"] = "0x" + "ef" * 32
                    return header
                fixture.header_mutation = mutate
                report = fixture.run()
                self.assertEqual(report["status"], "partial")
                self.assertEqual(report["rounds"], [])
                self.assertEqual(report["coverage"]["completed"], [])
                self.assertEqual(report["coverage"]["missing"][0]["from_block"], 100)
                self.assertEqual(report["evidence"]["final_anchor_check"], "changed")

    def test_catalog_fingerprint_and_entity_binding_fail_closed(self):
        original = S._read_file
        def changed(directory, filename):
            data, digest = original(directory, filename)
            if filename == "auction-events.json":
                data["events"][0]["topic0"] = "0x" + "00" * 32
            return data, digest
        fixture = RPCFixture()
        with patch.object(S, "_read_file", side_effect=changed):
            report = fixture.run()
        self.assertEqual(report["status"], "partial")
        self.assertEqual(fixture.requests, [])
        self.assertEqual(report["coverage"]["missing"][0]["from_block"], 100)

    def test_sibling_symlink_is_not_executed(self):
        with tempfile.TemporaryDirectory() as directory:
            scripts = Path(directory) / "scripts"
            scripts.mkdir()
            (scripts / "history.py").write_text("# fixture path only\n")
            (scripts / "snapshot.py").symlink_to(ROOT / "scripts/snapshot.py")
            with patch.object(history, "__file__", str(scripts / "history.py")), patch.object(history, "_SNAPSHOT", None):
                with self.assertRaises(history.HistoryError):
                    history._load_snapshot()

    def test_cli_rejects_unbounded_or_ambiguous_selection(self):
        for arguments in (("license", "--from-block", "100"),
                          ("license", "--from-block", "100", "--to-block", "90"),
                          ("license", "--from-block", "100", "--to-block", "110", "--anchor-block", "110"),
                          ("license", "--lookback-blocks", "5000001"),
                          ("license", "--max-chunks", "501"),
                          ("license", "--day", "7", "--day", "8"),
                          ("license", "--rpc-url", "https://example.invalid")):
            with self.subTest(arguments=arguments), self.assertRaises(history.InputError):
                history._cli_config(list(arguments))
        config = history._cli_config(["charter", "--day", "7", "--anchor-block", "2000000", "--lookback-blocks", "1000000"])
        self.assertEqual((config["auction"], config["day"], config["anchor_block"], config["lookback_blocks"]), ("charter", 7, 2_000_000, 1_000_000))

    def test_nonstring_selection_is_input_error_before_network(self):
        fixture = RPCFixture()
        for key in ("kind", "auction"):
            for value in ([], {}, None, 1):
                with self.subTest(field=key, value=value), self.assertRaises(history.InputError):
                    history.history({"schema_version": 1, key: value}, transport=fixture)
        self.assertEqual(fixture.requests, [])

    def test_cross_cutover_round_collision_preserves_both_emitters(self):
        fixture = RPCFixture()
        cutover = fixture.catalog["contracts"]["licenseAuction"]["registry_cutover"]["block_number"]
        fixture.head = cutover + 10
        fixture.purchase(day=0, count=2, price=3, block=cutover - 1)
        replacement = fixture.purchase(day=0, count=3, price=5, block=cutover)
        replacement["address"] = fixture.addresses["licenseAuction"]
        fixture.purchase(day=0, count=5, price=7, block=cutover + 1)
        report = fixture.run(from_block=cutover - 2, to_block=cutover + 2, max_chunks=1, detail="full")
        self.assertEqual(report["status"], "ok")
        rows = {row["address"]: row for row in report["rounds"]}
        self.assertEqual(set(rows), {fixture.address, replacement["address"]})
        self.assertEqual(rows[fixture.address]["day"], rows[replacement["address"]]["day"])
        self.assertEqual(rows[fixture.address]["purchase_quantity"], "7")
        self.assertEqual(rows[fixture.address]["consideration"]["total_raw"], "41")
        self.assertEqual(rows[replacement["address"]]["purchase_quantity"], "3")
        self.assertEqual(rows[replacement["address"]]["entity_id"], "sr-robinhood-license-auction-v1-1")
        self.assertEqual([event["address"] for event in report["evidence"]["decoded_events"]],
                         [fixture.address, replacement["address"], fixture.address])
        self.assertEqual(report["coverage"]["completed"][0]["emitter_addresses"], [fixture.address, replacement["address"]])
        self.assertEqual(report["coverage"]["missing"], [])
        self.assertEqual(fixture.windows(), [(cutover - 2, cutover + 2)])

    def test_deployment_boundary_and_predeployment_anchor(self):
        fixture = RPCFixture()
        deployment = fixture.catalog["contracts"]["licenseAuction"]["deployment_block"]
        fixture.head = deployment + 10
        fixture.purchase(day=0, count=2, block=deployment - 1)
        replacement = fixture.purchase(day=0, count=3, block=deployment)
        replacement["address"] = fixture.addresses["licenseAuction"]
        report = fixture.run(from_block=deployment - 1, to_block=deployment + 1)
        self.assertEqual(report["status"], "ok")
        self.assertEqual(fixture.windows(), [(deployment - 1, deployment - 1), (deployment, deployment + 1)])
        self.assertEqual([window["emitter_addresses"] for window in report["coverage"]["completed"]],
                         [[fixture.address], [fixture.address, replacement["address"]]])
        self.assertEqual({row["address"]: row["purchase_quantity"] for row in report["rounds"]},
                         {fixture.address: "2", replacement["address"]: "3"})
        fixture.requests.clear()
        report = fixture.run(from_block=deployment - 1, to_block=deployment - 1)
        self.assertEqual(report["status"], "ok")
        self.assertEqual([row["address"] for row in report["rounds"]], [fixture.address])
        self.assertEqual([r["params"][0] for r in fixture.requests if r["method"] == "eth_getCode"], [fixture.address])
        self.assertEqual(report["coverage"]["missing"], [])

    def test_current_license_selection_reaches_replacement(self):
        fixture = RPCFixture()
        fixture.head = fixture.catalog["contracts"]["licenseAuction"]["registry_cutover"]["block_number"] + 100
        event = fixture.purchase(day=0, count=4, block=fixture.head - 1)
        event["address"] = fixture.addresses["licenseAuction"]
        report = history.history({"schema_version": 1, "auction": "license", "lookback_blocks": 10},
                                 transport=fixture, now=lambda: NOW, monotonic=lambda: 0)
        self.assertEqual(report["status"], "ok")
        self.assertEqual((report["rounds"][0]["address"], report["rounds"][0]["purchase_quantity"]), (event["address"], "4"))
        self.assertEqual(fixture.windows(), [(fixture.head - 9, fixture.head)])

    def test_generation_boundary_chunk_budget_and_atomic_multi_emitter_failure(self):
        fixture = RPCFixture()
        deployment = fixture.catalog["contracts"]["licenseAuction"]["deployment_block"]
        fixture.head = deployment + 10
        fixture.purchase(day=0, count=2, block=deployment - 1)
        replacement = fixture.purchase(day=0, count=3, block=deployment)
        replacement["address"] = fixture.addresses["licenseAuction"]
        report = fixture.run(from_block=deployment - 1, to_block=deployment + 1, max_chunks=1)
        self.assertEqual(report["status"], "partial")
        self.assertEqual([(row["address"], row["purchase_quantity"]) for row in report["rounds"]], [(fixture.address, "2")])
        self.assertEqual(report["coverage"]["missing"][0]["from_block"], deployment)
        fixture.requests.clear()
        replacement["removed"] = True
        report = fixture.run(from_block=deployment - 1, to_block=deployment + 1, detail="full")
        self.assertEqual(report["status"], "partial")
        self.assertEqual(report["coverage"]["completed"], [])
        self.assertEqual(report["evidence"]["decoded_events"], [])
        self.assertEqual(report["rounds"], [])
        self.assertEqual(report["coverage"]["missing"][0]["from_block"], deployment - 1)
        self.assertEqual(report["evidence"]["invalidated_windows"][0]["emitter_addresses"], [fixture.address])

    def test_two_emitters_share_round_and_log_budgets(self):
        for budget_name, limit in (("MAX_ROUNDS", 1), ("MAX_LOGS", 1)):
            with self.subTest(budget=budget_name), patch.object(history, budget_name, limit):
                fixture = RPCFixture()
                deployment = fixture.catalog["contracts"]["licenseAuction"]["deployment_block"]
                fixture.head = deployment + 10
                fixture.purchase(day=0, block=deployment)
                replacement = fixture.purchase(day=0, block=deployment + 1)
                replacement["address"] = fixture.addresses["licenseAuction"]
                report = fixture.run(from_block=deployment, to_block=deployment + 1)
                self.assertEqual(report["status"], "partial")
                self.assertEqual(report["rounds"], [])
                self.assertEqual(report["coverage"]["completed"], [])
                self.assertEqual(report["coverage"]["missing"][0]["from_block"], deployment)
                self.assertEqual(fixture.windows(), [(deployment, deployment + 1)])

    def test_duplicate_position_across_emitters_is_not_two_rounds(self):
        fixture = RPCFixture()
        deployment = fixture.catalog["contracts"]["licenseAuction"]["deployment_block"]
        fixture.head = deployment + 10
        fixture.purchase(day=0, block=deployment)
        replacement = fixture.purchase(day=0, block=deployment)
        replacement["address"] = fixture.addresses["licenseAuction"]
        report = fixture.run(from_block=deployment, to_block=deployment + 1)
        self.assertEqual(report["status"], "partial")
        self.assertEqual(report["rounds"], [])
        self.assertEqual(report["coverage"]["completed"], [])

    def test_generation_boundary_tampering_fails_before_network(self):
        original = S._read_file
        def changed(directory, filename):
            data, digest = original(directory, filename)
            if filename == "auction-events.json":
                data["contracts"]["licenseAuction"]["deployment_block"] -= 1
            return data, digest
        fixture = RPCFixture()
        with patch.object(S, "_read_file", side_effect=changed):
            report = fixture.run()
        self.assertEqual(report["status"], "partial")
        self.assertEqual(fixture.requests, [])


class BuybackChecks(unittest.TestCase):
    def test_exact_checked_event_accounting_and_units(self):
        fixture = RPCFixture("buybacks")
        fixture.add("BuybackExecuted", block=112, ethSpent=2 * 10**18 + 11, tokensBurned=1)
        fixture.add("BuybackExecuted", ethSpent=10**18 + 7, tokensBurned=(1 << 256) - 1)
        report = fixture.run(detail="full")
        self.assertEqual(report["status"], "ok")
        row = report["buybacks"]
        self.assertEqual(row["event_count"], 2)
        self.assertEqual(row["eth_spent"], {"asset": "ETH", "decimals": 18, "total_raw": "3000000000000000018",
                                           "total": "3.000000000000000018"})
        self.assertEqual(row["standard_burned"], {
            "asset": "STANDARD", "decimals": 18, "total_raw": str(1 << 256),
            "total": "115792089237316195423570985008687907853269984665640564039457.584007913129639936"})
        self.assertEqual(row["first_observed_buyback"]["block_number"], 102)
        self.assertEqual(row["last_observed_buyback"]["block_number"], 112)
        self.assertEqual(row["first_observed_buyback"]["timestamp"], NOW - fixture.head + 102)
        self.assertTrue(row["requested_range_complete"])
        self.assertEqual(row["basis"], "buyback_event_accounting")
        self.assertEqual([event["event"] for event in report["evidence"]["decoded_events"]], ["BuybackExecuted"] * 2)
        self.assertNotIn("rounds", report)
        self.assertNotIn("auction", report)
        self.assertNotIn("day_filter", report["coverage"])

    def test_buyback_selection_rejects_auction_day_before_network(self):
        fixture = RPCFixture("buybacks")
        with self.assertRaises(history.InputError):
            fixture.run(day=7)
        self.assertEqual(fixture.requests, [])
        for arguments in (["buybacks", "--day", "7"], ["buybacks", "--day", "0"],
                          ["buybacks", "--address", fixture.address]):
            with self.subTest(arguments=arguments), self.assertRaises(history.InputError):
                history._cli_config(arguments)
        config = history._cli_config(["buybacks", "--from-block", "100", "--to-block", "119"])
        self.assertEqual(config["kind"], "buybacks")
        self.assertNotIn("auction", config)
        with self.assertRaises(history.InputError):
            history.history({"schema_version": 1, "auction": "buybacks"}, transport=fixture)
        with self.assertRaises(history.InputError):
            history.history({"schema_version": 1, "kind": "buybacks", "auction": "license"}, transport=fixture)
        self.assertEqual(fixture.requests, [])

    def test_empty_scanned_range_and_unknown_are_distinct(self):
        fixture = RPCFixture("buybacks")
        report = fixture.run()
        self.assertEqual(report["status"], "ok")
        self.assertEqual(report["buybacks"]["observation_status"], "no_matches_in_scanned_windows")
        self.assertEqual(report["buybacks"]["event_count"], 0)
        self.assertEqual(report["buybacks"]["eth_spent"]["total_raw"], "0")
        self.assertEqual(report["buybacks"]["standard_burned"]["total_raw"], "0")
        self.assertIsNone(report["buybacks"]["first_observed_buyback"])
        self.assertEqual(report["coverage"]["requested"], {"from_block": 100, "to_block": 119})
        self.assertEqual(fixture.windows(), [(100, 109), (110, 119)])
        fixture = RPCFixture("buybacks")
        fixture.denied_from = 100
        report = fixture.run()
        self.assertEqual(report["buybacks"]["observation_status"], "unavailable")
        self.assertIsNone(report["buybacks"]["event_count"])
        self.assertIsNone(report["buybacks"]["eth_spent"]["total_raw"])
        self.assertIsNone(report["buybacks"]["standard_burned"]["total"])
        self.assertFalse(report["buybacks"]["requested_range_complete"])
        self.assertEqual(report["coverage"]["completed"], [])

    def test_chunk_saturation_and_invalid_range_preserve_only_checked_totals(self):
        for failure in ("chunk", "saturation", "range"):
            with self.subTest(failure=failure), patch.object(history, "MAX_WINDOW_LOGS", 2):
                fixture = RPCFixture("buybacks")
                fixture.add("BuybackExecuted", ethSpent=7, tokensBurned=11)
                fixture.add("BuybackExecuted", block=112, ethSpent=99, tokensBurned=999)
                if failure == "saturation":
                    fixture.add("BuybackExecuted", block=113, index=1, ethSpent=99, tokensBurned=999)
                if failure == "range":
                    def mutation(start, end, logs):
                        if start == 110:
                            logs[0]["blockNumber"] = hex(end + 1)
                        return logs
                    fixture.logs_mutation = mutation
                report = fixture.run(max_chunks=1 if failure == "chunk" else 2)
                self.assertEqual(report["status"], "partial")
                self.assertEqual(report["buybacks"]["event_count"], 1)
                self.assertEqual(report["buybacks"]["eth_spent"]["total_raw"], "7")
                self.assertEqual(report["buybacks"]["standard_burned"]["total_raw"], "11")
                self.assertFalse(report["buybacks"]["requested_range_complete"])
                self.assertEqual([(w["from_block"], w["to_block"]) for w in report["coverage"]["completed"]], [(100, 109)])
                self.assertEqual((report["coverage"]["missing"][0]["from_block"], report["coverage"]["missing"][0]["to_block"]), (110, 119))
                self.assertEqual(fixture.windows(), [(100, 109)] if failure == "chunk" else [(100, 109), (110, 119)])

    def test_buyback_denial_stops_and_preserves_original_diagnostics(self):
        fixture = RPCFixture("buybacks")
        fixture.add("BuybackExecuted", ethSpent=7, tokensBurned=11)
        fixture.denied_from = 110
        report = fixture.run()
        self.assertEqual(report["status"], "partial")
        self.assertEqual(report["buybacks"]["standard_burned"]["total_raw"], "11")
        self.assertEqual(report["errors"]["window_110"]["diagnostics"], fixture.diagnostics)
        self.assertEqual(fixture.requests[-1]["method"], "eth_getLogs")
        self.assertEqual(fixture.windows(), [(100, 109), (110, 119)])
        self.assertEqual(report["coverage"]["missing"][0]["from_block"], 110)

    def test_final_anchor_denial_retains_per_window_totals_without_final_claim(self):
        fixture = RPCFixture("buybacks")
        fixture.add("BuybackExecuted", ethSpent=7, tokensBurned=11)
        def mutation(number, count, header):
            if number == 119 and count == 5:
                raise S.SnapshotError("RPC HTTP request failed", diagnostics=fixture.diagnostics)
            return header
        fixture.header_mutation = mutation
        report = fixture.run()
        self.assertEqual(report["status"], "partial")
        self.assertEqual(report["buybacks"]["eth_spent"]["total_raw"], "7")
        self.assertEqual(report["buybacks"]["standard_burned"]["total_raw"], "11")
        self.assertFalse(report["buybacks"]["requested_range_complete"])
        self.assertEqual(report["coverage"]["missing"], [])
        self.assertEqual([(w["from_block"], w["to_block"]) for w in report["coverage"]["completed"]], [(100, 109), (110, 119)])
        self.assertEqual(report["errors"]["final_anchor"]["diagnostics"], fixture.diagnostics)
        self.assertEqual(fixture.requests[-1]["method"], "eth_getBlockByNumber")
        self.assertEqual(fixture.headers_read[119], 5)

    def test_removed_log_or_anchor_reorg_invalidates_buyback_accounting(self):
        for failure in ("removed", "anchor"):
            with self.subTest(failure=failure):
                fixture = RPCFixture("buybacks")
                fixture.add("BuybackExecuted", ethSpent=7, tokensBurned=11)
                later = fixture.add("BuybackExecuted", block=112, ethSpent=99, tokensBurned=999)
                if failure == "removed":
                    later["removed"] = True
                else:
                    def mutation(number, count, header):
                        if number == 119 and count >= 4:
                            header["hash"] = "0x" + "ef" * 32
                        return header
                    fixture.header_mutation = mutation
                report = fixture.run(detail="full")
                self.assertEqual(report["status"], "partial")
                self.assertIsNone(report["buybacks"]["event_count"])
                self.assertIsNone(report["buybacks"]["standard_burned"]["total_raw"])
                self.assertEqual(report["coverage"]["completed"], [])
                self.assertEqual(report["evidence"]["decoded_events"], [])
                self.assertEqual(report["coverage"]["missing"][0]["from_block"], 100)
                self.assertEqual(report["evidence"]["final_anchor_check"], "changed")
                self.assertEqual(report["evidence"]["invalidated_windows"][0]["from_block"], 100)
                if failure == "removed":
                    self.assertEqual(fixture.requests[-1]["method"], "eth_getLogs")

    def test_wrong_emitter_or_auction_event_cannot_be_buybacks(self):
        for failure in ("emitter", "auction_event"):
            with self.subTest(failure=failure):
                fixture = RPCFixture("buybacks")
                event = fixture.add("BuybackExecuted", ethSpent=7, tokensBurned=11)
                auction = RPCFixture("license")
                if failure == "emitter":
                    event["address"] = auction.address
                else:
                    event["topics"][0] = auction.definitions["LicensesPurchased"]["topic0"]
                report = fixture.run()
                self.assertEqual(report["status"], "partial")
                self.assertEqual(report["coverage"]["completed"], [])
                self.assertIsNone(report["buybacks"]["eth_spent"]["total_raw"])
                self.assertEqual(fixture.windows(), [(100, 109)])
                self.assertEqual(fixture.requests[-1]["method"], "eth_getLogs")

    def test_buyback_chain_and_code_fail_before_logs(self):
        for failure in ("chain", "code"):
            with self.subTest(failure=failure):
                fixture = RPCFixture("buybacks")
                if failure == "chain":
                    fixture.chain_id = 1
                else:
                    fixture.code = "0x0000"
                report = fixture.run()
                self.assertEqual(report["status"], "partial")
                self.assertEqual(fixture.windows(), [])
                self.assertEqual(report["coverage"]["completed"], [])
                self.assertIsNone(report["buybacks"]["event_count"])
                self.assertEqual(fixture.requests[-1]["method"], "eth_chainId" if failure == "chain" else "eth_getCode")

    def test_anchor_token_binding_denomination_and_denial_stop_before_accounting(self):
        for failure in ("binding", "decimals", "uint8_padding", "token_code", "denial"):
            with self.subTest(failure=failure):
                fixture = RPCFixture("buybacks")
                fixture.add("BuybackExecuted", ethSpent=7, tokensBurned=11)
                if failure == "binding":
                    fixture.binding_address = "0x" + "34" * 20
                elif failure == "decimals":
                    fixture.standard_decimals = 6
                elif failure == "uint8_padding":
                    fixture.standard_decimals = 256 + 18
                elif failure == "token_code":
                    fixture.standard_code = "0x0000"
                else:
                    fixture.deny_binding = True
                report = fixture.run()
                self.assertEqual(report["status"], "partial")
                self.assertEqual(fixture.windows(), [])
                self.assertEqual(report["coverage"]["completed"], [])
                self.assertIsNone(report["buybacks"]["eth_spent"]["total_raw"])
                self.assertIsNone(report["buybacks"]["standard_burned"]["total_raw"])
                self.assertNotIn("anchor_standard_binding", report["evidence"])
                self.assertEqual(fixture.requests[-1]["method"], "eth_getCode" if failure == "token_code" else "eth_call")
                if failure == "denial":
                    self.assertEqual(report["errors"]["setup"]["diagnostics"], fixture.diagnostics)
                if failure in ("binding", "denial"):
                    self.assertEqual([r["params"][0]["to"] for r in fixture.requests if r["method"] == "eth_call"], [fixture.address])

    def test_treasury_catalog_and_publisher_binding_fail_before_network(self):
        original_read, original_package = S._read_file, S._load_package
        for failure in ("topic", "identity", "publisher"):
            with self.subTest(failure=failure):
                fixture = RPCFixture("buybacks")
                def changed_read(directory, filename):
                    data, digest = original_read(directory, filename)
                    if filename == "treasury-events.json":
                        if failure == "topic":
                            data["events"][0]["topic0"] = "0x" + "00" * 32
                        elif failure == "identity":
                            data["contracts"]["contractionVault"]["address"] = "0x" + "34" * 20
                    return data, digest
                def changed_package():
                    interface, addresses, hashes = original_package()
                    if failure == "publisher":
                        addresses["contractionVault"] = addresses["licenseAuction"]
                    return interface, addresses, hashes
                with patch.object(S, "_read_file", side_effect=changed_read), patch.object(S, "_load_package", side_effect=changed_package):
                    report = fixture.run()
                self.assertEqual(report["status"], "partial")
                self.assertEqual(fixture.requests, [])
                self.assertIsNone(report["buybacks"]["standard_burned"]["total_raw"])
                self.assertEqual(report["coverage"]["missing"][0]["from_block"], 100)


class POLBuybackChecks(unittest.TestCase):
    def test_raw_output_and_destinations_never_become_burned_standard(self):
        fixture = RPCFixture("pol-buybacks")
        first, second = "0x" + "12" * 20, "0x" + "34" * 20
        fixture.add("BuybackExecuted", ethIn=10**18 + 1, tokensOut=11, destination=first)
        fixture.add("BuybackExecuted", block=fixture.start_block + 12, ethIn=2, tokensOut=(1 << 256) - 1, destination=second)
        fixture.standard_decimals = 6
        fixture.deny_binding = True
        report = fixture.run(detail="full")
        self.assertEqual(report["status"], "ok")
        row = report["pol_buybacks"]
        self.assertEqual(row["eth_in"], {"asset": "ETH", "decimals": 18, "total_raw": "1000000000000000003", "total": "1.000000000000000003"})
        self.assertEqual(row["tokens_out"]["total_raw"], str((1 << 256) + 10))
        self.assertIsNone(row["tokens_out"]["asset"])
        self.assertIsNone(row["tokens_out"]["decimals"])
        self.assertIsNone(row["tokens_out"]["total"])
        self.assertEqual(row["reported_destinations"], [
            {"destination": first, "event_count": 1, "tokens_out_raw": "11"},
            {"destination": second, "event_count": 1, "tokens_out_raw": str((1 << 256) - 1)}])
        self.assertEqual([event["fields"]["destination"] for event in report["evidence"]["decoded_events"]], [first, second])
        self.assertNotIn("standard_burned", row)
        self.assertNotIn("buybacks", report)
        self.assertNotIn("anchor_standard_binding", report["evidence"])
        self.assertEqual([r for r in fixture.requests if r["method"] == "eth_call"], [])

    def test_pol_topic_and_indexed_destination_are_not_contraction_burn_layout(self):
        contraction = RPCFixture("buybacks")
        for failure in ("topic", "padding", "missing_destination", "wrong_emitter"):
            with self.subTest(failure=failure):
                fixture = RPCFixture("pol-buybacks")
                event = fixture.add("BuybackExecuted", ethIn=7, tokensOut=11, destination="0x" + "12" * 20)
                if failure == "topic":
                    event["topics"][0] = contraction.definitions["BuybackExecuted"]["topic0"]
                elif failure == "padding":
                    event["topics"][1] = "0x01" + event["topics"][1][4:]
                elif failure == "missing_destination":
                    event["topics"].pop()
                else:
                    event["address"] = contraction.address
                report = fixture.run()
                self.assertEqual(report["status"], "partial")
                self.assertIsNone(report["pol_buybacks"]["tokens_out"]["total_raw"])
                self.assertIsNone(report["pol_buybacks"]["reported_destinations"])
                self.assertEqual(report["coverage"]["completed"], [])
                self.assertEqual(fixture.requests[-1]["method"], "eth_getLogs")

    def test_partial_and_reorg_accounting_preserve_only_checked_pol_windows(self):
        for failure in ("denial", "removed"):
            with self.subTest(failure=failure):
                fixture = RPCFixture("pol-buybacks")
                fixture.add("BuybackExecuted", ethIn=7, tokensOut=11, destination="0x" + "12" * 20)
                later = fixture.add("BuybackExecuted", block=fixture.start_block + 12, ethIn=99, tokensOut=999, destination="0x" + "34" * 20)
                if failure == "denial":
                    fixture.denied_from = fixture.start_block + 10
                else:
                    later["removed"] = True
                report = fixture.run()
                self.assertEqual(report["status"], "partial")
                self.assertEqual(report["pol_buybacks"]["tokens_out"]["total_raw"], "11" if failure == "denial" else None)
                self.assertFalse(report["pol_buybacks"]["requested_range_complete"])
                self.assertEqual(report["coverage"]["missing"][0]["from_block"], fixture.start_block + (10 if failure == "denial" else 0))
                self.assertEqual(fixture.requests[-1]["method"], "eth_getLogs")
                if failure == "denial":
                    self.assertEqual(report["errors"]["window_" + str(fixture.start_block + 10)]["diagnostics"], fixture.diagnostics)
                else:
                    self.assertEqual(report["coverage"]["completed"], [])

    def test_pol_empty_scan_is_not_unavailable_and_rejects_denomination_flags(self):
        fixture = RPCFixture("pol-buybacks")
        report = fixture.run()
        self.assertEqual(report["pol_buybacks"]["observation_status"], "no_matches_in_scanned_windows")
        self.assertEqual(report["pol_buybacks"]["tokens_out"]["total_raw"], "0")
        self.assertEqual(report["pol_buybacks"]["reported_destinations"], [])
        fixture.requests.clear()
        for arguments in (["pol-buybacks", "--day", "0"], ["pol-buybacks", "--asset", "STANDARD"], ["pol-buybacks", "--decimals", "18"]):
            with self.subTest(arguments=arguments), self.assertRaises(history.InputError):
                history._cli_config(arguments)
        with self.assertRaises(history.InputError):
            fixture.run(asset="STANDARD")
        with self.assertRaises(history.InputError):
            history.history({"schema_version": 1, "auction": "pol-buybacks"}, transport=fixture)
        self.assertEqual(fixture.requests, [])

    def test_deployment_spanning_scan_never_queries_empty_address_filter(self):
        fixture = RPCFixture("pol-buybacks")
        deployment = fixture.catalog["contracts"]["polBuyback"]["deployment_block"]
        fixture.add("BuybackExecuted", block=deployment, ethIn=7, tokensOut=11, destination="0x" + "12" * 20)
        report = fixture.run(from_block=deployment - 2, to_block=deployment + 2)
        self.assertEqual(report["status"], "ok")
        self.assertEqual(fixture.windows(), [(deployment, deployment + 2)])
        self.assertEqual(report["pol_buybacks"]["tokens_out"]["total_raw"], "11")
        self.assertEqual([(row["from_block"], row["to_block"], row["scan_status"], row["emitter_addresses"])
                          for row in report["coverage"]["completed"]],
                         [(deployment - 2, deployment - 1, "no_deployed_emitters", []),
                          (deployment, deployment + 2, "logs_checked", [fixture.address])])
        self.assertEqual(report["coverage"]["missing"], [])
        self.assertEqual(report["evidence"]["final_anchor_check"], "matched")
        self.assertGreaterEqual(fixture.headers_read[deployment - 2], 2)
        self.assertGreaterEqual(fixture.headers_read[deployment - 1], 2)
        self.assertEqual([r["params"][0]["address"] for r in fixture.requests if r["method"] == "eth_getLogs"], [fixture.address])

    def test_entire_predeployment_range_checks_headers_without_code_or_logs(self):
        fixture = RPCFixture("pol-buybacks")
        deployment = fixture.catalog["contracts"]["polBuyback"]["deployment_block"]
        fixture.code = "0x"
        report = fixture.run(from_block=deployment - 2, to_block=deployment - 1)
        self.assertEqual(report["status"], "ok")
        self.assertEqual([r for r in fixture.requests if r["method"] in ("eth_getCode", "eth_getLogs", "eth_call")], [])
        self.assertEqual(report["coverage"]["completed"][0]["scan_status"], "no_deployed_emitters")
        self.assertEqual(report["coverage"]["completed"][0]["emitter_addresses"], [])
        self.assertEqual(report["coverage"]["missing"], [])
        self.assertEqual(report["pol_buybacks"]["observation_status"], "no_deployed_emitters")
        self.assertEqual(report["pol_buybacks"]["tokens_out"]["total_raw"], "0")
        self.assertTrue(report["pol_buybacks"]["requested_range_complete"])
        self.assertEqual(report["evidence"]["final_anchor_check"], "matched")
        self.assertGreaterEqual(fixture.headers_read[deployment - 2], 2)
        self.assertGreaterEqual(fixture.headers_read[deployment - 1], 3)

    def test_predeployment_checked_window_still_obeys_chunk_budget_and_reorg(self):
        for failure in ("chunk", "reorg"):
            with self.subTest(failure=failure):
                fixture = RPCFixture("pol-buybacks")
                deployment = fixture.catalog["contracts"]["polBuyback"]["deployment_block"]
                if failure == "reorg":
                    def mutate(number, count, header):
                        if number == deployment - 1 and count == 2:
                            header["hash"] = "0x" + "ef" * 32
                        return header
                    fixture.header_mutation = mutate
                report = fixture.run(from_block=deployment - 2, to_block=deployment + 2, max_chunks=1)
                self.assertEqual(report["status"], "partial")
                self.assertEqual(fixture.windows(), [])
                self.assertFalse(report["pol_buybacks"]["requested_range_complete"])
                self.assertEqual(report["coverage"]["missing"][0]["from_block"], deployment if failure == "chunk" else deployment - 2)
                self.assertEqual(report["pol_buybacks"]["tokens_out"]["total_raw"], "0" if failure == "chunk" else None)


class HistoryMainChecks(unittest.TestCase):
    def cli(self, fixture, arguments):
        class NoStdin:
            def __getattribute__(self, name):
                raise AssertionError("history CLI must not access stdin")

        stdout, stderr = io.StringIO(), io.StringIO()
        # Inject only transport and clocks; retain actual validation, collection,
        # event accounting and coverage decisions behind the entrypoint.
        collect = partial(history.history, transport=fixture, now=lambda: NOW,
                          monotonic=lambda: fixture.clock)
        with patch.object(history.sys, "argv", ["history.py", *arguments]), \
                patch.object(history.sys, "stdin", NoStdin()), \
                patch.object(history.sys, "stdout", stdout), \
                patch.object(history.sys, "stderr", stderr), \
                patch.object(history, "history", collect):
            code = history.main()
        return code, stdout.getvalue(), stderr.getvalue()

    def test_current_last_rounds_cli_reports_only_requested_generation(self):
        fixture = RPCFixture()
        deployment = fixture.catalog["contracts"]["licenseAuction"]["deployment_block"]
        fixture.head = deployment + 20
        fixture.purchase(day=1, block=deployment + 1)["address"] = fixture.addresses["licenseAuction"]
        fixture.purchase(day=2, block=deployment + 2)["address"] = fixture.addresses["licenseAuction"]
        code, stdout, stderr = self.cli(fixture, [
            "license", "--generation", "current", "--last-rounds", "1",
            "--anchor-block", str(deployment + 3), "--lookback-blocks", "4", "--detail", "full"])
        self.assertEqual((code, stderr), (0, ""))
        report = json.loads(stdout)
        self.assertEqual([(row["contract_role"], row["day"]) for row in report["rounds"]], [("licenseAuction", "2")])
        self.assertEqual([event["fields"]["day"] for event in report["evidence"]["decoded_events"]], [2])
        self.assertEqual(report["coverage"]["missing"], [])

    def test_charter_last_rounds_shortfall_is_stdout_exit_four_without_scan_gap(self):
        fixture = RPCFixture("charter")
        fixture.purchase(day=7, price=3)
        code, stdout, stderr = self.cli(fixture, [
            "charter", "--last-rounds", "2", "--from-block", "100", "--to-block", "119"])
        self.assertEqual((code, stderr), (4, ""))
        report = json.loads(stdout)
        self.assertEqual(report["coverage"]["missing"], [])
        self.assertEqual(report["errors"], {})
        self.assertEqual(report["coverage"]["round_selection"]["generations"][0]["shortfall"], 1)
        self.assertEqual(report["rounds"][0]["last_observed_purchase"]["unit_price"]["asset"], "ETH")

    def test_complete_checked_window_is_stdout_exit_zero(self):
        fixture = RPCFixture()
        fixture.purchase(count=2, price=9)
        fixture.purchase(count=3, price=2, block=112)
        code, stdout, stderr = self.cli(fixture, [
            "license", "--from-block", "100", "--to-block", "119", "--chunk-blocks", "10"])
        self.assertEqual((code, stderr), (0, ""))
        report = json.loads(stdout)
        self.assertEqual(report["status"], "ok")
        self.assertEqual(report["coverage"]["missing"], [])
        self.assertEqual([(w["from_block"], w["to_block"], w["scan_status"])
                          for w in report["coverage"]["completed"]],
                         [(100, 109, "logs_checked"), (110, 119, "logs_checked")])
        self.assertEqual(report["evidence"]["final_anchor_check"], "matched")
        self.assertEqual(report["rounds"][0]["purchase_quantity"], "5")
        self.assertEqual(report["rounds"][0]["consideration"]["total_raw"], "24")

    def test_retained_partial_coverage_is_stdout_exit_four(self):
        fixture = RPCFixture()
        fixture.purchase(count=2, price=9)
        fixture.purchase(count=99, block=112)
        fixture.denied_from = 110
        code, stdout, stderr = self.cli(fixture, [
            "license", "--from-block", "100", "--to-block", "119", "--chunk-blocks", "10"])
        self.assertEqual((code, stderr), (4, ""))
        report = json.loads(stdout)
        self.assertEqual(report["status"], "partial")
        self.assertEqual([(w["from_block"], w["to_block"]) for w in report["coverage"]["completed"]],
                         [(100, 109)])
        self.assertEqual([(w["from_block"], w["to_block"]) for w in report["coverage"]["missing"]],
                         [(110, 119)])
        self.assertEqual(report["rounds"][0]["purchase_quantity"], "2")
        self.assertEqual(report["rounds"][0]["consideration"]["total_raw"], "18")
        self.assertEqual(report["errors"]["window_110"]["diagnostics"], fixture.diagnostics)
        self.assertEqual(fixture.requests[-1]["method"], "eth_getLogs")

    def test_setup_unavailable_is_stdout_exit_four_without_observations(self):
        fixture = RPCFixture()
        fixture.chain_id = 1
        code, stdout, stderr = self.cli(fixture, [
            "license", "--from-block", "100", "--to-block", "119"])
        self.assertEqual((code, stderr), (4, ""))
        report = json.loads(stdout)
        self.assertEqual(report["status"], "partial")
        self.assertEqual(report["rounds"], [])
        self.assertEqual(report["coverage"]["completed"], [])
        self.assertEqual([(w["from_block"], w["to_block"]) for w in report["coverage"]["missing"]],
                         [(100, 119)])
        self.assertEqual(set(report["errors"]), {"setup"})
        self.assertEqual([request["method"] for request in fixture.requests], ["eth_chainId"])

    def test_invalid_input_is_stdout_exit_two_before_network(self):
        for arguments in ([], ["license", "--from-block", "100", "--to-block", "90"],
                          ["license", "--day", "7", "--day", "8"], ["--help", "license"]):
            with self.subTest(arguments=arguments):
                fixture = RPCFixture()
                code, stdout, stderr = self.cli(fixture, arguments)
                self.assertEqual((code, stderr), (2, ""))
                report = json.loads(stdout)
                self.assertEqual(report["status"], "error")
                self.assertEqual(report["error"]["kind"], "input")
                self.assertNotIn("coverage", report)
                self.assertEqual(fixture.requests, [])

    def test_help_is_plain_stdout_exit_zero_without_network(self):
        fixture = RPCFixture()
        code, stdout, stderr = self.cli(fixture, ["--help"])
        self.assertEqual((code, stderr), (0, ""))
        with self.assertRaises(json.JSONDecodeError):
            json.loads(stdout)
        self.assertEqual(fixture.requests, [])


if __name__ == "__main__":
    unittest.main()
