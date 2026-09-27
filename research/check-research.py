"""Offline consumer-visible regressions for optional bundled helpers.

Run with `python3 -B research/check-research.py` from the skill source checkout.
Fixtures are fictional, never retrieved chain data. No transport or ABI decoding.
"""

from copy import deepcopy
from decimal import Context, Decimal, ROUND_DOWN, localcontext
from fractions import Fraction
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

SCRIPTS = Path(__file__).resolve().parents[1] / "scripts"
sys.path.insert(0, str(SCRIPTS))

from calculations import (estimate_workload, gap_to_floor_scenario,
                          pending_delta_pace, summarize_rounds, weighted_price)


FIXTURE = Path(__file__).with_name("fixtures") / "round-v1.json"


class AccountingChecks(unittest.TestCase):
    def test_weighted_quantity_and_raw_precision(self):
        result = weighted_price([(2, "1000000000000000001"), (1, "1000000000000000002")])
        self.assertEqual(result["quantity"], 3)
        self.assertEqual(result["consideration_raw"], 3000000000000000004)
        self.assertEqual(result["average_raw"], Fraction(3000000000000000004, 3))
        self.assertEqual((result["quotient_raw"], result["remainder"]), (1000000000000000001, 1))

    def test_no_sale_is_not_zero_average(self):
        for rows in ([], [(0, 50)]):
            result = weighted_price(rows)
            self.assertIsNone(result["average_raw"])
            self.assertIsNone(result["quotient_raw"])
            self.assertIsNone(result["remainder"])
        self.assertEqual(weighted_price([(1, 0)])["average_raw"], 0)

    def test_invalid_financial_integers(self):
        for value in (1.0, True, -1, "1.0", "01", "unknown"):
            with self.subTest(value=value), self.assertRaises(ValueError):
                weighted_price([(value, 2)])

    def test_signed_observed_pace_and_compatible_scale(self):
        kwargs = dict(opening_asset="fictional-a", closing_asset="fictional-a",
                      opening_scale=100, closing_scale=100, period_seconds=60)
        result = pending_delta_pace(1000, 850, 100, 140, **kwargs)
        self.assertEqual(result["raw_per_second"], Fraction(-15, 4))
        self.assertEqual(result["amount_per_period"], Fraction(-9, 4))
        self.assertEqual(pending_delta_pace(850, 1000, 100, 140, **kwargs)["amount_per_second"], Fraction(3, 80))
        for patch in ({"closing_scale": 10}, {"opening_scale": 0},
                      {"closing_asset": "fictional-b"},
                      {"opening_asset": None, "closing_asset": None},
                      {"opening_asset": "unknown", "closing_asset": "unknown"},
                      {"period_seconds": 0}):
            with self.subTest(patch=patch), self.assertRaises(ValueError):
                pending_delta_pace(1000, 850, 100, 140, **(kwargs | patch))
        for start, end in ((100, 100), (101, 100), ("unknown", 100)):
            with self.subTest(start=start, end=end), self.assertRaises(ValueError):
                pending_delta_pace(1000, 850, start, end, **kwargs)


class EvidenceChecks(unittest.TestCase):
    def setUp(self):
        self.document = json.loads(FIXTURE.read_text())

    def primary(self, result):
        return next(group for group in result["rounds"]
                    if group["key"] == (999999, "fictional-auction-a", 7, "fictional-payment-a", 18))

    def test_sorted_deduped_emitters_units_and_routed_transactions(self):
        result = summarize_rounds(self.document)
        self.document["events"].append(deepcopy(self.document["events"][1]))
        self.document["events"].reverse()
        self.assertEqual(result, summarize_rounds(self.document))
        self.assertEqual([group["key"] for group in result["rounds"]], [
            (999999, "fictional-auction-a", 7, "fictional-payment-a", 18),
            (999999, "fictional-auction-a", 7, "fictional-payment-b", 6),
            (999999, "fictional-auction-b", 7, "fictional-payment-a", 18)])
        group = self.primary(result)
        self.assertEqual(group["uncontested_totals"]["quantity"], 3)
        self.assertEqual(group["events"][0]["transaction"]["to"], "fictional-router")
        self.assertEqual(group["first_observed"][0]["timestamp"], "1000")
        self.assertEqual(group["uncontested_minimum_unit_price_raw"], 1000000000000000001)
        self.assertIsNone(group["observed_span_seconds"])
        self.assertEqual(group["last_observed"][0]["event"]["block_number"], "101")
        self.assertEqual(result["removed_events"], [self.document["events"][1]])

    def test_conflicts_retained_not_counted_and_last_position_ties(self):
        conflict = deepcopy(self.document["events"][1])
        conflict["decoded"]["quantity"] = "99"
        self.document["events"].append(conflict)
        tied = deepcopy(self.document["events"][0])
        tied["transaction_hash"] = "0x" + "6" * 64
        self.document["events"].append(tied)
        result = summarize_rounds(self.document)
        self.assertEqual(result["conflicts"][0]["variants"], sorted(
            [conflict, self.document["events"][1]], key=lambda row: json.dumps(row, sort_keys=True, separators=(",", ":"))))
        group = self.primary(result)
        self.assertEqual(group["uncontested_totals"]["quantity"], 0)
        self.assertEqual({item["event"]["transaction_hash"] for item in group["last_observed"]},
                         {tied["transaction_hash"], self.document["events"][0]["transaction_hash"]})
        self.document["events"].reverse()
        self.assertEqual(result, summarize_rounds(self.document))

    def test_missing_records_unknown_times_and_receipt_scope_stay_partial(self):
        partial = deepcopy(self.document["events"][0])
        partial["decoded"]["quantity"] = "unknown"
        self.document["events"].append(partial)
        result = summarize_rounds(self.document)
        self.assertEqual(result["deferred_events"][0]["event"], partial)
        self.assertEqual(self.primary(result)["last_observed"][0]["timestamp"], "unknown")
        result["coverage"]["failed"].clear()
        self.assertEqual(self.document["coverage"]["failed"][0]["from_block"], "102")
        self.assertEqual(self.primary(result)["uncontested_totals"]["quantity"], 2)

    def test_provenance_enrichment_counts_once_without_losing_checks(self):
        enriched = deepcopy(self.document["events"][1])
        enriched["source_refs"] = ["synthetic", "another-fictional-source"]
        enriched["receipt_checks"] = [{"status": "not_checked"}]
        self.document["events"].append(enriched)
        result = summarize_rounds(self.document)
        self.assertEqual(result["conflicts"], [])
        self.assertEqual(self.primary(result)["uncontested_totals"]["quantity"], 3)
        self.assertIn(enriched, self.primary(result)["events"])
        enriched["receipt_checks"] = [{"status": "mismatched"}]
        result = summarize_rounds(self.document)
        self.assertEqual(self.primary(result)["uncontested_totals"]["quantity"], 1)

    def test_noncanonical_header_and_reverted_receipt_are_not_counted(self):
        event = self.document["events"][0]
        header = self.document["headers"][f"{event['chain_id']}:{event['block_hash']}"]
        header["canonicality"] = "noncanonical"
        result = summarize_rounds(self.document)
        self.assertEqual(self.primary(result)["uncontested_totals"]["quantity"], 2)
        self.assertEqual(result["disputed_events"][0]["variants"], [event])
        header["canonicality"] = "unknown"
        event["receipt_checks"] = [{"status": "matched", "transaction_status": "reverted"}]
        self.assertEqual(self.primary(summarize_rounds(self.document))["uncontested_totals"]["quantity"], 2)

    def test_header_hash_reuse_conflicting_time_and_missing_header(self):
        result = summarize_rounds(self.document)
        known = [item for group in result["rounds"] for item in group["last_observed"]
                 if item["event"]["block_number"] == "100"]
        self.assertEqual([item["timestamp"] for item in known], ["1000", "1000"])
        header = self.document["headers"][known[0]["header_ref"]]
        alternative = deepcopy(header)
        alternative["timestamp"] = "1001"
        header["alternatives"] = [alternative]
        result = summarize_rounds(self.document)
        self.assertTrue(all(item["timestamp"] == "unknown" for group in result["rounds"] for item in group["last_observed"]))
        self.document["headers"] = {}
        self.assertTrue(all(item["timestamp"] == "unknown" for group in summarize_rounds(self.document)["rounds"] for item in group["last_observed"]))

    def test_scale_chain_and_unknown_denomination_are_separate(self):
        for index, patch in enumerate(({"denomination": {"asset": "fictional-payment-a", "decimals": "6"}},
                                       {"denomination": "unknown"}, {"chain_id": "999998"})):
            event = deepcopy(self.document["events"][0])
            event.update(patch)
            event["transaction_hash"] = "0x" + str(index + 6) * 64
            self.document["events"].append(event)
        keys = {group["key"] for group in summarize_rounds(self.document)["rounds"]}
        self.assertIn((999999, "fictional-auction-a", 7, "fictional-payment-a", 6), keys)
        self.assertIn((999999, "fictional-auction-a", 7, "unknown", None), keys)
        self.assertIn((999998, "fictional-auction-a", 7, "fictional-payment-a", 18), keys)
        unknown = next(group for group in summarize_rounds(self.document)["rounds"]
                       if group["key"][3] == "unknown")
        self.assertIsNone(unknown["uncontested_totals"]["average_raw"])

    def test_removed_variant_and_competing_log_slot_do_not_inflate_totals(self):
        for removed in (False, True):
            with self.subTest(removed=removed):
                document = deepcopy(self.document)
                variant = deepcopy(document["events"][0])
                if removed:
                    variant["removed"] = True
                else:
                    variant["transaction_hash"] = "0x" + "6" * 64
                document["events"].append(variant)
                result = summarize_rounds(document)
                self.assertEqual(self.primary(result)["uncontested_totals"]["quantity"], 2)
                disputed_hashes = {row["transaction_hash"] for item in result["disputed_events"]
                                   for row in item["variants"]}
                self.assertIn(document["events"][0]["transaction_hash"], disputed_hashes)

    def test_competing_block_hashes_require_reconciliation_not_double_counting(self):
        replacement = deepcopy(self.document["events"][0])
        replacement["block_hash"] = "0x" + "c" * 64
        replacement["transaction_hash"] = "0x" + "6" * 64
        self.document["events"].append(replacement)
        result = summarize_rounds(self.document)
        self.assertEqual(self.primary(result)["uncontested_totals"]["quantity"], 2)
        original = self.document["events"][0]
        self.document["headers"][f"{original['chain_id']}:{original['block_hash']}"]["canonicality"] = "noncanonical"
        result = summarize_rounds(self.document)
        self.assertEqual(self.primary(result)["uncontested_totals"]["quantity"], 3)

    def test_observed_span_uses_header_times_and_retains_unknowns(self):
        final_event = self.document["events"][0]
        header = self.document["headers"][f"{final_event['chain_id']}:{final_event['block_hash']}"]
        header["timestamp"] = "1040"
        result = summarize_rounds(self.document)
        self.assertEqual(self.primary(result)["observed_span_seconds"], 40)
        header["timestamp"] = "bad timestamp"
        result = summarize_rounds(self.document)
        self.assertEqual(self.primary(result)["last_observed"][0]["event"], final_event)
        self.assertEqual(self.primary(result)["last_observed"][0]["timestamp"], "unknown")
        self.assertIsNone(self.primary(result)["observed_span_seconds"])

    def test_empty_observations_do_not_create_zero_price_round(self):
        self.document["events"] = []
        result = summarize_rounds(self.document)
        self.assertEqual(result["rounds"], [])


class WorkloadChecks(unittest.TestCase):
    def test_inclusive_workload_and_normalized_union(self):
        self.assertEqual(estimate_workload([(10, 10), (0, 4)], 2)["range_requests"], 4)
        normalized = estimate_workload([(5, 10), (0, 5), (2, 3), (11, 12)], 5, overlaps="normalize")
        self.assertEqual(normalized["ranges"], [(0, 12)])
        self.assertEqual((normalized["blocks"], normalized["range_requests"]), (13, 3))
        self.assertEqual(estimate_workload([], 10)["range_requests"], 0)
        self.assertEqual(estimate_workload([(0, 10 ** 30)], 100)["range_requests"], 10 ** 28 + 1)

    def test_overlap_and_malformed_endpoints(self):
        for ranges in ([(0, 5), (5, 9)], [(0, 2), (0, 2)], [(3, 2)], [(-1, 2)],
                       [(True, 3)], [(0.0, 3)], [(0,)], [(0, 1, 2)], ["12"]):
            with self.subTest(ranges=ranges), self.assertRaises(ValueError):
                estimate_workload(ranges, 10)
        for span in (0, -1, 1.5):
            with self.subTest(span=span), self.assertRaises(ValueError):
                estimate_workload([(0, 1)], span)
        with self.assertRaises(ValueError):
            estimate_workload([(0, 1)], 10, overlaps="ignore")


class ScenarioChecks(unittest.TestCase):
    def test_nonzero_floor_time_zero_half_life_and_flat_curve(self):
        for opening, floor, elapsed, expected in ((110, 10, 0, 110), (110, 10, 7, 60),
                                                   (110, 10, 14, 35), (10, 10, 3, 10), (0, 0, 3, 0)):
            result = gap_to_floor_scenario(opening, floor, 7, elapsed, precision=32)
            self.assertEqual(result["value"], Decimal(expected))
            self.assertEqual(result["lower_bound"], Decimal(expected))
            self.assertEqual(result["upper_bound"], Decimal(expected))
            self.assertEqual(result["absolute_error_bound"], 0)

    def test_fractional_half_life_enclosure_and_context_independence(self):
        result = gap_to_floor_scenario(110, 10, 2, 1, precision=32)
        context = Context(prec=100)
        reference = context.add(Decimal(10), context.multiply(Decimal(50), context.sqrt(Decimal(2))))
        self.assertLessEqual(result["lower_bound"], reference)
        self.assertGreaterEqual(result["upper_bound"], reference)
        self.assertLess(result["absolute_error_bound"], Decimal("1e-29"))
        with localcontext() as ambient:
            ambient.prec = 3
            ambient.rounding = ROUND_DOWN
            self.assertEqual(result, gap_to_floor_scenario(110, 10, 2, 1, precision=32))
        self.assertEqual(gap_to_floor_scenario(110, 10, 1, 10000, precision=16)["value"], Decimal(10))

    def test_scenario_domain_precision_and_limits(self):
        for arguments in ((9, 10, 1, 0), (10, -1, 1, 0), (10, 0, 0, 0),
                          (10, 0, 1, -1), (10.0, 0, 1, 0), ("NaN", 0, 1, 0),
                          (10, 0, 1, 10001), ("1e1001", 0, 1, 0),
                          (10, 0, "1e-1001", 0)):
            with self.subTest(arguments=arguments), self.assertRaises(ValueError):
                gap_to_floor_scenario(*arguments, precision=32)
        for precision in (15, 201, True, 32.0):
            with self.subTest(precision=precision), self.assertRaises(ValueError):
                gap_to_floor_scenario(10, 0, 1, 1, precision=precision)


class CommandChecks(unittest.TestCase):
    def invoke(self, command, document, *, file_input=False):
        with tempfile.TemporaryDirectory() as directory:
            arguments = [sys.executable, "-I", "-B", str(SCRIPTS / "research.py"), command]
            if file_input:
                source = Path(directory) / "supplied evidence.json"
                source.write_text(document, encoding="utf-8")
                arguments.extend(["--input", str(source)])
            return subprocess.run(arguments, input=None if file_input else document,
                                  text=True, capture_output=True, cwd=directory, timeout=15)

    def test_wire_accounting_retains_large_integer_remainder_and_no_sale(self):
        process = self.invoke("weighted-price", '{"rows":[[2,"1000000000000000001"],[1,"1000000000000000002"]]}')
        self.assertEqual(process.returncode, 0, process.stderr)
        result = json.loads(process.stdout)
        self.assertEqual(result["consideration_raw"], "3000000000000000004")
        self.assertEqual(result["average_raw"], {"numerator": "3000000000000000004", "denominator": "3"})
        self.assertEqual((result["quotient_raw"], result["remainder"]), ("1000000000000000001", "1"))
        empty = self.invoke("weighted-price", '{"rows":[]}')
        self.assertEqual(empty.returncode, 0, empty.stderr)
        self.assertIsNone(json.loads(empty.stdout)["average_raw"])

    def test_file_decimal_scenario_avoids_binary_float_rounding(self):
        process = self.invoke("curve", '{"opening":110.1,"floor":10.1,"half_life":7,"elapsed":7,"precision":32}',
                              file_input=True)
        self.assertEqual(process.returncode, 0, process.stderr)
        result = json.loads(process.stdout)
        self.assertEqual(result["value"], "60.1")
        self.assertEqual(Decimal(result["absolute_error_bound"]), 0)

    def test_ambiguous_or_invalid_input_emits_no_calculation(self):
        for document in ('{"rows":[],"rows":[[1,2]]}', '{"rows":[[NaN,2]]}',
                         '{"rows":[[1.0,2]]}', '{"rows":[[true,2]]}', '[]', '{"rows":'):
            with self.subTest(document=document):
                process = self.invoke("weighted-price", document)
                self.assertEqual(process.returncode, 2)
                self.assertEqual(process.stdout, "")
                self.assertIn("error", json.loads(process.stderr))


if __name__ == "__main__":
    unittest.main()
