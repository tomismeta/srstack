#!/usr/bin/env python3
"""Deterministic event-accounting and bounded-coverage regressions; no live RPC."""

import copy
import importlib.util
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
        self.catalog, addresses, _ = history._load_catalog(S)
        self.role = history.ROLES[auction]
        self.auction = auction
        self.address = addresses[self.role]
        self.definitions = {e["abi"]["name"]: e for e in self.catalog["events"] if self.role in e["contracts"]}
        self.logs, self.requests = [], []
        self.head = 2_000_000
        self.headers_read = {}
        self.header_mutation = None
        self.logs_mutation = None
        self.denied_from = None
        self.clock = 0
        self.expire_on_logs = False
        self.diagnostics = {"endpoint": S.RPC_URL, "http_status": 403, "headers": {"content-type": "text/plain"},
                            "response_excerpt": "fixture access denial", "excerpt_bytes": 21, "truncated": False,
                            "read_error": None, "untrusted_response": True, "cause": "unconfirmed"}

    def add(self, name, block=102, index=0, **fields):
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
                result = hex(S.CHAIN_ID)
            elif method == "eth_getCode":
                result = "0x6000"
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
        config = {"schema_version": 1, "auction": self.auction, "from_block": 100, "to_block": 119, "chunk_blocks": 10}
        config.update(options)
        return history.history(config, transport=self, now=lambda: NOW, monotonic=lambda: self.clock)

    def windows(self):
        return [(int(r["params"][0]["fromBlock"], 16), int(r["params"][0]["toBlock"], 16)) for r in self.requests if r["method"] == "eth_getLogs"]


class HistoryChecks(unittest.TestCase):
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


if __name__ == "__main__":
    unittest.main()
