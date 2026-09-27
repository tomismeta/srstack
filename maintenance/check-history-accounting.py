#!/usr/bin/env python3
"""Focused auction opening/execution accounting regressions; no live RPC."""

import importlib.util
from pathlib import Path
import unittest

SPEC = importlib.util.spec_from_file_location("sr_history_checks", Path(__file__).with_name("check-history.py"))
checks = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(checks)
RPCFixture = checks.RPCFixture


class AuctionAccountingChecks(unittest.TestCase):
    def test_opening_parameter_and_first_execution_are_distinct_with_weighted_sales(self):
        for auction, asset, quantity, total, average in (
            ("license", "STANDARD", "5", "11000000000000000041", {"numerator": "11000000000000000041", "denominator": "5"}),
            ("charter", "ETH", "2", "5000000000000000016", {"numerator": "2500000000000000008", "denominator": "1"}),
        ):
            with self.subTest(auction=auction):
                fixture = RPCFixture(auction)
                activation = fixture.add("AuctionStarted", block=101, day=7, startPrice=5 * 10**18 + 3)
                fixture.add("DayRolled", block=101, index=1, day=7,
                            startPrice=4 * 10**18 + 1, floorPrice=10**18, cap=5)
                # Insert out of order, including two sales in one block: first
                # means checked chain position, not RPC response insertion order.
                last = fixture.purchase(day=7, count=3, price=10**18 + 9, block=102, index=2)
                first = fixture.purchase(day=7, count=2, price=4 * 10**18 + 7, block=102, index=1)
                report = fixture.run(generation="legacy")
                self.assertEqual(report["status"], "ok")
                row = report["rounds"][0]
                self.assertEqual(row["observed_activations"][0]["reported_start_price"],
                                 {"asset": asset, "decimals": 18, "raw": "5000000000000000003", "scaled18": "5.000000000000000003"})
                self.assertEqual(row["observed_activations"][0]["transaction_hash"], activation["transactionHash"])
                self.assertEqual(row["observed_rolls"][0]["reported_start_price"]["raw"], "4000000000000000001")
                self.assertEqual(row["first_observed_purchase"]["unit_price"],
                                 {"asset": asset, "decimals": 18, "raw": "4000000000000000007", "scaled18": "4.000000000000000007"})
                self.assertEqual(row["first_observed_purchase"]["transaction_hash"], first["transactionHash"])
                self.assertEqual(row["last_observed_purchase"]["unit_price"]["raw"], "1000000000000000009")
                self.assertEqual(row["last_observed_purchase"]["transaction_hash"], last["transactionHash"])
                self.assertEqual(row["purchase_quantity"], quantity)
                self.assertEqual(row["consideration"]["total_raw"], total)
                self.assertEqual(row["consideration"]["quantity_weighted_average_raw"], average)
                # RPCFixture rejects transaction-value lookups; only the
                # authenticated purchase fields can supply consideration.
                self.assertFalse(row["complete_round"])
                self.assertEqual(row["sellout"], "not_established")
                self.assertIsNone(row["scheduled_opening"])
                self.assertIsNone(row["time_to_sellout"])

    def test_same_round_identifier_keeps_each_generations_prices_separate(self):
        for auction, roles in (
            ("license", ("licenseAuctionLegacy", "licenseAuctionV11", "licenseAuction")),
            ("charter", ("charterAuctionLegacy", "charterAuction")),
        ):
            with self.subTest(auction=auction):
                fixture = RPCFixture(auction)
                deployment = max(fixture.catalog["contracts"][role].get("deployment_block", 0) for role in roles)
                fixture.head = deployment + 20
                for index, role in enumerate(roles):
                    address = fixture.addresses[role]
                    fixture.add("AuctionStarted", block=deployment + 1, index=index,
                                day=7, startPrice=100 + index)["address"] = address
                    fixture.purchase(day=7, price=10 + index, block=deployment + 2, index=index)["address"] = address
                report = fixture.run(from_block=deployment, to_block=deployment + 9)
                self.assertEqual(report["status"], "ok")
                self.assertEqual({row["address"]: (row["day"],
                                                   row["observed_activations"][0]["reported_start_price"]["raw"],
                                                   row["first_observed_purchase"]["unit_price"]["raw"],
                                                   row["consideration"]["total_raw"])
                                  for row in report["rounds"]},
                                 {fixture.addresses[role]: ("7", str(100 + index), str(10 + index), str(10 + index))
                                  for index, role in enumerate(roles)})

    def test_activation_without_purchase_preserves_missing_execution(self):
        fixture = RPCFixture()
        fixture.add("AuctionStarted", block=101, day=7, startPrice=19)
        row = fixture.run(generation="legacy")["rounds"][0]
        self.assertEqual(row["observed_activations"][0]["reported_start_price"]["raw"], "19")
        self.assertIsNone(row["first_observed_purchase"])
        self.assertIsNone(row["last_observed_purchase"])
        self.assertIsNone(row["consideration"]["quantity_weighted_average_raw"])
        self.assertIsNone(row["reported_round_cap"])
        self.assertFalse(row["complete_round"])

    def test_purchase_without_opener_does_not_invent_opening_price(self):
        fixture = RPCFixture("charter")
        fixture.purchase(price=0)
        row = fixture.run(generation="legacy")["rounds"][0]
        self.assertEqual(row["first_observed_purchase"]["unit_price"],
                         {"asset": "ETH", "decimals": 18, "raw": "0", "scaled18": "0"})
        self.assertEqual(row["observed_activations"], [])
        self.assertEqual(row["observed_rolls"], [])
        self.assertIsNone(row["scheduled_opening"])
        self.assertFalse(row["complete_round"])

    def test_conflicting_activation_prices_remain_separate_observations(self):
        fixture = RPCFixture()
        fixture.add("AuctionStarted", block=101, day=7, startPrice=19)
        fixture.add("AuctionStarted", block=103, day=7, startPrice=17)
        fixture.purchase(price=11, block=104)
        row = fixture.run(generation="legacy")["rounds"][0]
        self.assertEqual([(event["block_number"], event["reported_start_price"]["raw"])
                          for event in row["observed_activations"]], [(101, "19"), (103, "17")])
        self.assertEqual(row["first_observed_purchase"]["unit_price"]["raw"], "11")
        self.assertFalse(row["complete_round"])


if __name__ == "__main__":
    unittest.main()
