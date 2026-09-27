#!/usr/bin/env python3
"""Synthetic contract-state discovery against a strict ten-block log provider."""
import importlib.util
import json
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parent.parent
SPEC = importlib.util.spec_from_file_location("history_fixtures", ROOT / "maintenance/check-history.py")
fixtures = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(fixtures)
history, S = fixtures.history, fixtures.S


class StateFixture(fixtures.RPCFixture):
    def __init__(self, auction="license", generation="current"):
        super().__init__(auction)
        self.role = history.GENERATIONS[auction][generation]
        self.generation = generation
        self.address = self.addresses[self.role]
        self.definitions = {e["abi"]["name"]: e for e in self.catalog["events"] if self.role in e["contracts"]}
        self.deployment = self.catalog["contracts"][self.role].get("deployment_block", 0)
        self.start_block = self.deployment + 100
        self.head = self.start_block + 100_000
        interface = S._load_package()[0]
        self.selectors = {c["selector"]: c["function"] for c in interface["calls"]
                          if c["contract"] == history.ROLES[auction]}
        self.observations = []
        self.state_override = None
        self.archive_error = False
        self.deny_state = False

    def add(self, name, block=None, index=0, **fields):
        event = super().add(name, block, index, **fields)
        self.observations.append((int(event["blockNumber"], 16), index, name, fields, self.address))
        return event

    def values(self, address, number):
        events = [row for row in sorted(self.observations) if row[0] <= number and row[4] == address]
        rounds = [row[3]["day"] for row in events if "day" in row[3]]
        day = rounds[-1] if rounds else 0
        purchases = [row[3] for row in events if row[2] in ("LicensesPurchased", "CharterPurchased")]
        value = {"started": any(row[2] == "AuctionStarted" for row in events), "currentDay": day,
                 "soldToday": sum(p.get("count", 1) for p in purchases if p["day"] == day),
                 "lastSaleDay": purchases[-1]["day"] if purchases else 0,
                 "lastSalePrice": purchases[-1].get("unitPrice", purchases[-1].get("price")) if purchases else 0}
        return self.state_override(number, value) if self.state_override else value

    def __call__(self, payload, timeout, deadline, monotonic):
        responses = []
        for request in json.loads(payload):
            method, params = request["method"], request["params"]
            if method == "eth_call":
                self.requests.append(request)
                if self.deny_state:
                    raise S.SnapshotError("endpoint denied this request", diagnostics=self.diagnostics)
                tag = params[1]
                assert tag["requireCanonical"] is True
                number = int(tag["blockHash"], 16) - 1
                assert number >= self.deployment
                if self.archive_error:
                    responses.append({"jsonrpc": "2.0", "id": request["id"],
                                      "error": {"code": -32000, "message": "historical state unavailable"}})
                else:
                    value = self.values(params[0]["to"], number)[self.selectors[params[0]["data"]]]
                    responses.append({"jsonrpc": "2.0", "id": request["id"], "result": "0x" + format(value, "064x")})
            else:
                if method == "eth_getLogs":
                    assert int(params[0]["toBlock"], 16) - int(params[0]["fromBlock"], 16) + 1 <= 10
                responses.extend(json.loads(super().__call__(json.dumps([request]).encode(), timeout, deadline, monotonic)))
        return json.dumps(responses).encode()

    def collect(self, **options):
        config = {"schema_version": 1, "auction": self.auction, "generation": self.generation,
                  "from_block": self.start_block, "to_block": self.head}
        config.update(options)
        return history.history(config, transport=self, now=lambda: fixtures.NOW, monotonic=lambda: self.clock)

    def sparse_round(self):
        self.add("AuctionStarted", block=self.start_block + 50, day=0, startPrice=30)
        self.purchase(day=0, count=2, price=13, block=self.start_block + 1000)
        self.purchase(day=0, count=3, price=7, block=self.start_block + 50_000)
        self.purchase(day=0, count=1, price=5, block=self.start_block + 50_000, index=1)


class StateChecks(unittest.TestCase):
    def test_sparse_default_reads_contracts_first_and_recovers_weighted_executions(self):
        fixture = StateFixture()
        fixture.sparse_round()
        report = fixture.collect()
        self.assertEqual(report["errors"], {})
        row = report["rounds"][0]
        self.assertEqual(row["purchase_quantity"], "6")
        self.assertEqual(row["consideration"]["quantity_weighted_average_raw"], {"numerator": "26", "denominator": "3"})
        self.assertEqual(row["observed_activations"][0]["reported_start_price"]["raw"], "30")
        self.assertEqual(row["first_observed_purchase"]["unit_price"]["raw"], "13")
        self.assertEqual(row["last_observed_purchase"]["unit_price"]["raw"], "5")
        methods = [request["method"] for request in fixture.requests]
        self.assertLess(methods.index("eth_call"), methods.index("eth_getLogs"))
        self.assertLess(len(fixture.windows()), 12)  # Blind ten-block paging needs 10,001 windows.
        self.assertEqual(report["status"], "partial")
        self.assertFalse(report["coverage"]["requested_range_complete"])
        self.assertIn("state_discovery_intervals_unsearched", row["gaps"])
        self.assertFalse(row["complete_round"])
        self.assertEqual(report["evidence"]["final_anchor_check"], "matched")

    def test_equal_endpoints_with_hidden_activity_never_claim_empty_or_complete(self):
        fixture = StateFixture()
        fixture.sparse_round()
        fixture.state_override = lambda n, values: {name: False if name == "started" else 0 for name in values}
        report = fixture.collect()
        self.assertEqual(report["status"], "partial")
        self.assertEqual(report["rounds"], [])
        self.assertEqual(report["coverage"]["completed"], [])
        self.assertEqual([(w["from_block"], w["to_block"]) for w in report["coverage"]["unsearched"]],
                         [(fixture.start_block, fixture.head)])
        self.assertFalse(report["coverage"]["requested_range_complete"])

    def test_round_reset_preserves_old_and_new_prices(self):
        fixture = StateFixture()
        fixture.sparse_round()
        fixture.add("DayRolled", block=fixture.head - 1000, day=1, startPrice=20, floorPrice=2, cap=4)
        fixture.purchase(day=1, count=1, price=17, block=fixture.head - 500)
        report = fixture.collect()
        self.assertEqual([(r["day"], r["purchase_quantity"]) for r in report["rounds"]], [("0", "6"), ("1", "1")])
        self.assertEqual(report["rounds"][1]["first_observed_purchase"]["unit_price"]["raw"], "17")

    def test_all_supported_generations_use_independent_event_prices(self):
        for auction, generations in history.GENERATIONS.items():
            for generation in generations:
                with self.subTest(auction=auction, generation=generation):
                    fixture = StateFixture(auction, generation)
                    fixture.sparse_round()
                    report = fixture.collect()
                    self.assertEqual(report["errors"], {})
                    row = report["rounds"][0]
                    self.assertEqual(row["address"], fixture.address)
                    self.assertEqual(row["consideration"]["asset"], "ETH" if auction == "charter" else "STANDARD")
                    self.assertEqual(row["purchase_quantity"], "3" if auction == "charter" else "6")

    def test_archive_error_or_denial_stops_without_logs_or_fallback(self):
        for field in ("archive_error", "deny_state"):
            fixture = StateFixture()
            setattr(fixture, field, True)
            report = fixture.collect()
            self.assertEqual(report["status"], "partial")
            self.assertEqual(fixture.windows(), [])
            self.assertEqual(report["rounds"], [])
            self.assertTrue(report["errors"])
            if field == "deny_state":
                self.assertEqual(sum(r["method"] == "eth_call" for r in fixture.requests), 1)
                self.assertEqual(report["errors"]["setup"]["diagnostics"]["http_status"], 403)

    def test_state_probe_reorg_invalidates_all_accounting(self):
        fixture = StateFixture()
        fixture.sparse_round()
        probe = fixture.start_block - 1
        def mutate(number, count, header):
            if number == probe and count > 1:
                return {**header, "hash": "0x" + "ab" * 32}
            return header
        fixture.header_mutation = mutate
        report = fixture.collect()
        self.assertEqual(report["evidence"]["final_anchor_check"], "changed")
        self.assertEqual(report["rounds"], [])
        self.assertEqual(report["coverage"]["completed"], [])
        self.assertEqual(report["coverage"]["unsearched"], [])

    def test_budget_failure_retains_only_committed_event_windows(self):
        fixture = StateFixture()
        fixture.sparse_round()
        report = fixture.collect(max_chunks=1)
        self.assertEqual(report["status"], "partial")
        self.assertEqual(len(fixture.windows()), 1)
        self.assertTrue(report["coverage"]["missing"])
        self.assertFalse(report["coverage"]["requested_range_complete"])
        self.assertEqual(report["rounds"][0]["purchase_quantity"], "0")

    def test_last_rounds_stops_after_newest_observed_group_with_explicit_gaps(self):
        fixture = StateFixture()
        fixture.sparse_round()
        fixture.purchase(day=1, count=1, price=17, block=fixture.head - 500)
        report = fixture.collect(last_rounds=1)
        self.assertEqual(report["coverage"]["stop_reason"], "last_rounds_observed")
        self.assertEqual([(r["day"], r["purchase_quantity"]) for r in report["rounds"]], [("1", "1")])
        self.assertIn("earlier_selected_round_events_deliberately_unsearched", report["rounds"][0]["gaps"])
        self.assertTrue(all(first > fixture.start_block + 50_000 for first, _ in fixture.windows()))
        self.assertFalse(report["coverage"]["requested_range_complete"])

    def test_tiny_explicit_window_still_reads_state_before_complete_log_window(self):
        fixture = StateFixture()
        fixture.purchase(day=0, count=2, price=3, block=fixture.start_block + 2)
        report = fixture.collect(to_block=fixture.start_block + 9)
        self.assertEqual(report["status"], "ok")
        self.assertTrue(report["coverage"]["requested_range_complete"])
        self.assertEqual(report["rounds"][0]["consideration"]["total_raw"], "6")
        self.assertEqual(fixture.windows(), [(fixture.start_block, fixture.start_block + 9)])


if __name__ == "__main__":
    unittest.main()
