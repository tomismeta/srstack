"""Behavioral regression checks for the bundled planner; not runtime package content."""
import hashlib
import json
import shutil
import subprocess
import sys
import tempfile
import unittest
from decimal import Decimal, localcontext
from pathlib import Path

SCRIPT = Path(__file__).resolve().parents[1] / "scripts/scenario.py"
PARAMETER_NAMES = ("participation.json", "monetary.json", "launch.json")


def copy_package(directory):
    """Use an isolated installed-layout copy; never mutate the active package."""
    root = Path(directory) / "package"
    (root / "scripts").mkdir(parents=True)
    shutil.copy2(SCRIPT, root / "scripts/scenario.py")
    destination = root / "assets/parameters"
    destination.mkdir(parents=True)
    for name in PARAMETER_NAMES:
        shutil.copy2(SCRIPT.parents[1] / "assets/parameters" / name, destination / name)
    return root / "scripts/scenario.py"


def parameter_record(document, identifier):
    return next(record for record in document["records"] if record["id"] == identifier)


def inputs(**changes):
    data = {
        "schema_version": 1, "mode": "stress", "detail": "full",
        "assumptions_acknowledged": True, "days": 2,
        "initial_branches": 1, "initial_credits": "0", "other_branches": 99,
        "max_branches": 10, "daily_license_limit": 3,
        "base_daily_issuance": "100", "remaining_issuance_budget": "10000",
        "initial_token_price_eth": "1", "entry_cost_eth": "10", "entry_gas_eth": "1",
        "license_cost_tokens": "2", "license_gas_eth": "1", "expansion_budget_eth": "8",
        "buy_cost_markup_pct": "0", "sale_fee_pct": "10", "sale_slippage_pct": "10",
        "exit_gas_eth": "1", "funding": "external", "selective_target": 3,
        "selective_interval_days": 7, "exit_mode": "all",
        "scenarios": [{"id": "fixture", "name": "Fictional arithmetic case", "multiplier": "1",
                       "other_branch_growth_pct": "0", "price_growth_pct": "0",
                       "resolution_fee_pct": "20", "sale_tax_pct": "25"}],
    }
    data.update(changes)
    return data


def invoke(data=None, raw=None, script=SCRIPT, forbidden_reads=()):
    payload = json.dumps(data).encode() if raw is None else raw
    command = [sys.executable, "-B", "-I", str(script)]
    if forbidden_reads:
        # Python's audit event fires before open. An escaped-file read is a distinct
        # failure even if the loader would subsequently reject that file's contents.
        guard = """
import os
import runpy
import sys
from pathlib import Path
script = sys.argv[1]
forbidden = [Path(path).absolute() for path in sys.argv[2:]]
def audit(event, args):
    if event == "open" and isinstance(args[0], (str, bytes, os.PathLike)):
        path = Path(os.fsdecode(args[0])).absolute()
        if any(path == blocked or blocked in path.parents for blocked in forbidden):
            os._exit(86)
sys.addaudithook(audit)
sys.argv = [script]
runpy.run_path(script, run_name="__main__")
"""
        command = [sys.executable, "-B", "-I", "-c", guard, str(script),
                   *(str(path) for path in forbidden_reads)]
    return subprocess.run(command, input=payload, capture_output=True, timeout=20, check=False)


def calculate(data, script=SCRIPT):
    result = invoke(data, script=script)
    if result.returncode != 0:
        raise AssertionError(result.stderr.decode())
    if result.stderr:
        raise AssertionError(result.stderr.decode())
    return json.loads(result.stdout)


def strategy(result, name, scenario=0):
    return next(r for r in result["scenarios"][scenario]["results"] if r["strategy"] == name)


class PlannerContract(unittest.TestCase):

    def assert_success_warnings(self, result):
        for scenario in result["scenarios"]:
            self.assertEqual(scenario["warning"], result["warning"])
            for row in scenario["results"]:
                self.assertEqual(row["warning"], result["warning"])

    def assert_error(self, result, code, kind):
        self.assertEqual(result.returncode, code, result.stderr.decode(errors="replace"))
        self.assertEqual(result.stdout, b"")
        payload = json.loads(result.stderr)
        self.assertEqual(payload["error"]["type"], kind)
        self.assertNotIn("scenarios", payload)
        return payload

    def assert_report(self, report, mode, status):
        self.assertEqual(report["mode"], mode)
        self.assertEqual(report["status"], status)
        self.assertFalse(report["contract_verified"])
        for count, collection in (("checked", "constraints"), ("conflicts", "conflicts"),
                                  ("unresolved", "unresolved")):
            self.assertEqual(report["counts"][count], len(report[collection]))


class PlannerAccounting(PlannerContract):
    def near(self, actual, expected):
        with localcontext() as context:
            context.prec = 70
            a, b = Decimal(actual), Decimal(expected)
            self.assertLessEqual(abs(a - b), Decimal("1e-45") * max(Decimal(1), abs(b)))

    def test_cash_budget_self_dilution_and_sequential_sale_costs(self):
        result = calculate(inputs())
        keep, expand = strategy(result, "keep"), strategy(result, "aggressive")
        self.assertEqual(expand["licenses_bought"], 2)
        self.assertEqual(expand["branches_before_exit"], 3)
        self.assertEqual(expand["skipped_attempts"], 4)
        self.near(expand["expansion_eth_spent"], "6")
        self.near(keep["credits_released"], "2")
        self.near(keep["wallet_tokens_before_sale"], "1.6")
        self.near(keep["sale_tax_eth"], "0.4")
        self.near(keep["sale_fee_eth"], "0.12")
        self.near(keep["sale_slippage_eth"], "0.108")
        self.near(keep["estimated_eth_recovered"], "0.972")
        self.near(keep["net_cash_eth"], "-11.028")
        with localcontext() as context:
            context.prec = 70
            self.near(expand["credits_released"], Decimal(200) * 3 / 102)
            self.near(expand["estimated_eth_recovered"], Decimal(200) * 3 / 102 * Decimal("0.486"))
            self.near(expand["delta_vs_keep_eth"], Decimal(expand["net_cash_eth"]) - Decimal(keep["net_cash_eth"]))

    def test_credits_cannot_spend_future_accrual_or_create_external_tokens(self):
        result = calculate(inputs(funding="credits", license_cost_tokens="1", license_gas_eth="0",
                                  expansion_budget_eth="0"))
        row = strategy(result, "aggressive")
        self.assertEqual(row["branches_before_exit"], 2)
        self.assertEqual([p["day"] for p in row["purchases"]], [2])
        self.near(row["credits_spent"], "1")
        self.near(row["license_tokens_purchased"], "0")
        self.near(row["expansion_eth_spent"], "0")
        with localcontext() as context:
            context.prec = 70
            self.near(row["credits_before_exit"], Decimal(200) / 101)
            self.near(row["credits_accrued"], Decimal(1) + Decimal(200) / 101)

    def test_partial_and_no_exit_do_not_liquidate_retained_position(self):
        for mode, retired, balance in [("one", 1, "80"), ("none", 0, "120")]:
            result = calculate(inputs(initial_branches=3, initial_credits="120", base_daily_issuance="0",
                                      daily_license_limit=0, exit_mode=mode))
            row = strategy(result, "keep")
            self.assertEqual(row["branches_retired"], retired)
            self.assertEqual(row["branches_after_exit"], 3 - retired)
            self.assertTrue(row["charter_retained"])
            self.near(row["credits_retained"], balance)
            self.assertIsNone(row["break_even_price_eth"])
            self.near(row["total_outlay_eth"], "12" if retired else "11")
            if mode == "none":
                self.near(row["estimated_eth_recovered"], "0")
                self.near(row["net_cash_eth"], "-11")
        full = strategy(calculate(inputs(initial_branches=3, initial_credits="120",
                                         base_daily_issuance="0", daily_license_limit=0)), "keep")
        self.assertFalse(full["charter_retained"])
        self.near(full["credits_retained"], "0")
        self.assertEqual(full["branches_after_exit"], 0)

    def test_issuance_budget_and_purchase_timing_are_independent_of_strategies(self):
        data = inputs(days=8, remaining_issuance_budget="50", license_cost_tokens="0",
                      license_gas_eth="0", expansion_budget_eth="0", include_history=True)
        result = calculate(data)
        self.near(strategy(result, "keep")["credits_accrued"], "0.5")
        self.assertEqual(strategy(result, "selective")["purchases"][0]["day"], 8)
        self.assertEqual(strategy(result, "aggressive")["licenses_bought"], 9)
        self.assertEqual(strategy(result, "aggressive")["history"][0]["branches"], 4)
        self.assertEqual(strategy(result, "aggressive")["history"][2]["branches"], 10)
        with localcontext() as context:
            context.prec = 70
            self.near(strategy(result, "aggressive")["credits_accrued"], Decimal(200) / Decimal(103))
        data = inputs(days=1, other_branches=0, daily_license_limit=0)
        data["scenarios"][0]["price_growth_pct"] = "10"
        result = calculate(data)
        self.near(result["scenarios"][0]["final_token_price_eth"], "1.1")
        self.near(strategy(result, "keep")["credits_accrued"], "100")

    def test_zero_and_total_haircuts_have_explicit_results(self):
        for field in ["resolution_fee_pct", "sale_tax_pct"]:
            data = inputs(mode="stress")
            data["scenarios"][0][field] = "100"
            for row in calculate(data)["scenarios"][0]["results"]:
                self.near(row["estimated_eth_recovered"], "0")
                self.assertIsNone(row["break_even_price_eth"])
        for field in ["sale_fee_pct", "sale_slippage_pct"]:
            for row in calculate(inputs(**{field: "100"}))["scenarios"][0]["results"]:
                self.near(row["estimated_eth_recovered"], "0")
                self.assertIsNone(row["break_even_price_eth"])
        for row in calculate(inputs(remaining_issuance_budget="0"))["scenarios"][0]["results"]:
            self.near(row["credits_accrued"], "0")
        for row in calculate(inputs(daily_license_limit=0))["scenarios"][0]["results"]:
            self.assertEqual(row["licenses_bought"], 0)

    def test_invalid_cli_input_has_no_success_output(self):
        invalid = []
        for field, value in [("schema_version", 2), ("mode", "automatic"),
                             ("mode", None), ("mode", True),
                             ("days", True), ("entry_cost_eth", "NaN"), ("funding", "wallet"),
                             ("days", 1.5), ("initial_credits", "1e-19"),
                             ("initial_credits", "1.123456789012345678901234567890")]:
            data = inputs(); data[field] = value; invalid.append(json.dumps(data).encode())
        for field in ("entry_cost_eth", "mode"):
            missing = inputs(); del missing[field]; invalid.append(json.dumps(missing).encode())
        unknown = inputs(); unknown["filename"] = "/not-an-input"; invalid.append(json.dumps(unknown).encode())
        forged = inputs(); forged["conformance"] = {"status": "within_checked_rules"}
        invalid.append(json.dumps(forged).encode())
        duplicate = json.dumps(inputs()).replace('"days": 2', '"days": 2, "days": 3')
        invalid.extend([duplicate.encode(), b'{"schema_version":NaN}', b'[' * 9 + b']' * 9,
                        b' ' * 65537, b'\xff'])
        for raw in invalid:
            with self.subTest(raw=raw[:70]):
                result = invoke(raw=raw)
                self.assert_error(result, 2, "invalid_input")

    def test_documented_example_conserves_credits(self):
        path = SCRIPT.parents[1] / "assets/examples/planning.json"
        example = json.loads(path.read_text())
        summary = calculate(example)
        self.assert_success_warnings(summary)
        result = calculate({**example, "detail": "full"})
        self.assertEqual(result["classification"], "hypothetical")
        for scenario in result["scenarios"]:
            for row in scenario["results"]:
                with localcontext() as context:
                    context.prec = 70
                    self.near(Decimal(result["assumptions"]["initial_credits"]) + Decimal(row["credits_accrued"]) - Decimal(row["credits_spent"]),
                              Decimal(row["credits_released"]) + Decimal(row["credits_retained"]))


class PlannerConformance(PlannerContract):
    def test_documented_conflicts_block_and_stress_preserves_departures(self):
        cases = [
            ({"max_branches": 11}, None, {"max_branches"}),
            ({"initial_branches": 11, "max_branches": 11, "selective_target": 11},
             None, {"initial_branches", "max_branches", "selective_target"}),
            ({"max_branches": 11, "selective_target": 11}, None,
             {"max_branches", "selective_target"}),
            ({"daily_license_limit": 4}, None, {"daily_license_limit"}),
            ({"remaining_issuance_budget": "900000001"}, None, {"remaining_issuance_budget"}),
            ({}, "0.19", {"scenarios.0.multiplier"}),
            ({}, "1.26", {"scenarios.0.multiplier"}),
        ]
        for changes, multiplier, expected_paths in cases:
            with self.subTest(changes=changes, multiplier=multiplier):
                data = inputs(mode="documented", **changes)
                if multiplier is not None:
                    data["scenarios"][0]["multiplier"] = multiplier
                blocked = self.assert_error(invoke(data), 3, "documented_rule_conflict")
                report = blocked["conformance"]
                self.assert_report(report, "documented", "blocked")
                self.assertEqual({row["input_path"] for row in report["conflicts"]}, expected_paths)
                self.assertNotIn("results", report)
                data["mode"] = "stress"
                result = calculate(data)
                self.assert_success_warnings(result)
                allowed = result["conformance"]
                self.assert_report(allowed, "stress", "conflicts_allowed_in_stress")
                self.assertEqual(allowed["conflicts"], report["conflicts"])
                supplied = {row["path"]: row for row in allowed["inputs"]}
                for path in expected_paths:
                    self.assertEqual(supplied[path]["classification"], "inconsistent")
                # The known-rule departure is not silently clamped before arithmetic.
                with localcontext() as context:
                    context.prec = 70
                    expected = (Decimal(200) * Decimal(data["scenarios"][0]["multiplier"])
                                * data["initial_branches"] / (99 + data["initial_branches"]))
                    self.assertAlmostEqual(Decimal(strategy(result, "keep")["credits_accrued"]),
                                           expected, places=40)

    def test_stress_does_not_clamp_branch_or_daily_license_departures(self):
        data = inputs(initial_branches=10, max_branches=20, selective_target=20,
                      daily_license_limit=4, license_cost_tokens="0", license_gas_eth="0")
        result = calculate(data)
        aggressive = strategy(result, "aggressive")
        self.assertEqual(aggressive["branches_before_exit"], 18)
        self.assertEqual(aggressive["licenses_bought"], 8)
        self.assertEqual({row["input_path"] for row in result["conformance"]["conflicts"]},
                         {"max_branches", "selective_target", "daily_license_limit"})

    def test_documented_boundaries_compute_without_certifying_unresolved_inputs(self):
        for multiplier in ("0.2", "1.25"):
            with self.subTest(multiplier=multiplier):
                data = inputs(mode="documented", remaining_issuance_budget="900000000",
                              funding="credits")
                data["scenarios"][0]["multiplier"] = multiplier
                result = calculate(data)
                self.assertEqual((result["schema_version"], result["model_version"]), (1, "1"))
                self.assert_success_warnings(result)
                report = result["conformance"]
                self.assert_report(report, "documented", "within_checked_rules")
                self.assertEqual(report["conflicts"], [])
                entries = {row["path"]: row for row in report["inputs"]}
                for path in ("base_daily_issuance", "license_cost_tokens", "sale_fee_pct",
                             "entry_cost_eth", "funding", "scenarios.0.multiplier",
                             "scenarios.0.resolution_fee_pct", "scenarios.0.sale_tax_pct"):
                    self.assertEqual(entries[path]["classification"], "unresolved", path)
                    self.assertIsNotNone(entries[path]["value"], path)
                self.assertEqual(entries["remaining_issuance_budget"]["classification"], "user_selected")
                self.assertEqual(Decimal(strategy(result, "keep")["credits_accrued"]),
                                 Decimal(2) * Decimal(multiplier))
                constraints = entries["scenarios.0.multiplier"]["constraints"]
                self.assertEqual({row["parameter_id"] for row in constraints},
                                 {"multiplier-floor", "multiplier-ceiling"})
                self.assertTrue(all(row["conforms"] for row in constraints))

    def test_published_rate_and_fee_envelopes_block_without_changing_stress_math(self):
        cases = [
            ({"base_daily_issuance": "700001", "remaining_issuance_budget": "900000000"},
             None, "base_daily_issuance", "11200.016"),
            ({}, "1.99", "scenarios.0.resolution_fee_pct", "1.9602"),
            ({}, "60.01", "scenarios.0.resolution_fee_pct", "0.7998"),
        ]
        for changes, fee, path, wallet in cases:
            with self.subTest(path=path, fee=fee):
                data = inputs(mode="documented", **changes)
                if fee is not None:
                    data["scenarios"][0]["resolution_fee_pct"] = fee
                blocked = self.assert_error(invoke(data), 3, "documented_rule_conflict")
                self.assertEqual({row["input_path"] for row in blocked["conformance"]["conflicts"]},
                                 {path})
                result = calculate({**data, "mode": "stress"})
                entries = {row["path"]: row for row in result["conformance"]["inputs"]}
                self.assertEqual(entries[path]["classification"], "inconsistent")
                self.assertEqual(Decimal(strategy(result, "keep")["wallet_tokens_before_sale"]),
                                 Decimal(wallet))
        for fee in ("2", "60"):
            data = inputs(mode="documented", base_daily_issuance="700000",
                          remaining_issuance_budget="900000000")
            data["scenarios"][0]["resolution_fee_pct"] = fee
            result = calculate(data)
            self.assert_report(result["conformance"], "documented", "within_checked_rules")
            entries = {row["path"]: row for row in result["conformance"]["inputs"]}
            self.assertEqual(entries["base_daily_issuance"]["classification"], "unresolved")
            self.assertEqual(entries["scenarios.0.resolution_fee_pct"]["classification"], "unresolved")
            self.assertEqual(Decimal(strategy(result, "keep")["wallet_tokens_before_sale"]),
                             Decimal(14000) * (1 - Decimal(fee) / 100))

    def test_discretionary_caps_and_actual_position_are_not_publisher_verified(self):
        for changes, expected in [
            ({"max_branches": 10, "daily_license_limit": 3}, "source_backed"),
            ({"max_branches": 5, "daily_license_limit": 1}, "user_selected"),
        ]:
            with self.subTest(changes=changes):
                report = calculate(inputs(mode="documented", **changes))["conformance"]
                entries = {row["path"]: row for row in report["inputs"]}
                for path in ("max_branches", "daily_license_limit"):
                    self.assertEqual(entries[path]["classification"], expected)
                self.assertEqual(entries["initial_branches"]["classification"], "user_selected")
        result = calculate(inputs(mode="documented", initial_branches=10, selective_target=10))
        entries = {row["path"]: row for row in result["conformance"]["inputs"]}
        self.assertEqual(entries["initial_branches"]["classification"], "user_selected")

    def test_report_accounts_for_every_supplied_economic_and_decision_input(self):
        data = inputs(mode="documented", include_history=True)
        data["scenarios"].append({**data["scenarios"][0], "id": "second", "multiplier": "0.5"})
        result = calculate(data)
        self.assert_success_warnings(result)
        excluded = {"schema_version", "mode", "detail", "assumptions_acknowledged", "include_history", "scenarios"}
        expected = {path: value for path, value in data.items() if path not in excluded}
        for index, scenario in enumerate(data["scenarios"]):
            expected.update({f"scenarios.{index}.{key}": value
                             for key, value in scenario.items() if key not in {"id", "name"}})
        entries = result["conformance"]["inputs"]
        self.assertEqual(len(entries), len(expected))
        self.assertEqual({row["path"] for row in entries}, set(expected))
        for row in entries:
            self.assertEqual(row["origin"], "user_supplied")
            self.assertIn(row["classification"], {"source_backed", "user_selected", "unresolved"})
            value = expected[row["path"]]
            if row["path"] in {"funding", "exit_mode"}:
                self.assertEqual(row["value"], value)
            else:
                self.assertEqual(Decimal(str(row["value"])), Decimal(str(value)), row["path"])
        backed = {row["path"] for row in entries if row["classification"] == "source_backed"}
        self.assertEqual(backed, {"max_branches", "daily_license_limit"})

    def test_report_identifies_exact_packaged_parameter_bytes_and_source_evidence(self):
        report = calculate(inputs(mode="documented"))["conformance"]
        files = {row["path"]: row for row in report["parameter_files"]}
        self.assertEqual(set(files), {"assets/parameters/" + name for name in PARAMETER_NAMES})
        records = {}
        for path, provenance in files.items():
            raw = (SCRIPT.parents[1] / path).read_bytes()
            document = json.loads(raw)
            self.assertEqual(provenance["sha256"], hashlib.sha256(raw).hexdigest())
            self.assertEqual(provenance["reviewed_at"], document["reviewed_at"])
            records.update({row["id"]: row for row in document["records"]})
        for row in report["constraints"]:
            record = records[row["parameter_id"]]
            for field in ("unit", "status", "source_ids", "locator"):
                self.assertEqual(row[field], record[field])
            self.assertTrue(row["conforms"])

    def test_stress_still_rejects_computationally_invalid_inputs(self):
        for changes in ({"max_branches": 101}, {"daily_license_limit": 101},
                        {"days": 366}, {"remaining_issuance_budget": "1000000000000001"}):
            with self.subTest(changes=changes):
                self.assert_error(invoke(inputs(**changes)), 2, "invalid_input")


class PlannerDetail(PlannerContract):
    def test_summary_preserves_strategy_outcomes_across_funding_and_exit_modes(self):
        required = {
            "strategy", "warning", "branches_before_exit", "branches_retired",
            "branches_after_exit", "charter_retained", "credits_accrued", "credits_spent",
            "credits_retained", "wallet_tokens_before_sale", "expansion_eth_spent",
            "total_outlay_eth", "estimated_eth_recovered", "net_cash_eth",
            "delta_vs_keep_eth", "break_even_price_eth", "licenses_bought", "skipped_attempts",
        }
        for funding, exit_mode in (("external", "all"), ("credits", "one"), ("credits", "none")):
            with self.subTest(funding=funding, exit_mode=exit_mode):
                data = inputs(funding=funding, exit_mode=exit_mode, days=8,
                              initial_credits="20", expansion_budget_eth="40")
                data["scenarios"].append({**data["scenarios"][0], "id": "second",
                                          "multiplier": "0.5", "price_growth_pct": "-10"})
                full = calculate(data)
                del data["detail"]
                summary = calculate(data)
                self.assert_success_warnings(summary)
                self.assertEqual(summary["detail"], "summary")
                self.assertEqual(full["detail"], "full")
                self.assertEqual(summary["conformance"]["status"], full["conformance"]["status"])
                for summarized, complete in zip(summary["scenarios"], full["scenarios"]):
                    self.assertEqual({k: v for k, v in summarized.items() if k != "results"},
                                     {k: v for k, v in complete.items() if k != "results"})
                    for row, original in zip(summarized["results"], complete["results"]):
                        self.assertEqual(set(row), required)
                        self.assertEqual(row, {field: original[field] for field in required})

    def test_compact_report_preserves_all_classifications_unknowns_and_conflict_evidence(self):
        data = inputs(funding="credits", initial_branches=11, max_branches=12,
                      selective_target=12, daily_license_limit=4)
        data["scenarios"][0]["multiplier"] = "1.26"
        data["scenarios"].append({**data["scenarios"][0], "id": "second", "multiplier": "0.5"})
        full = calculate(data)
        summary = calculate({**data, "detail": "summary"})
        report, original = summary["conformance"], full["conformance"]
        self.assert_report(report, "stress", "conflicts_allowed_in_stress")
        self.assertEqual(report["inputs"],
                         [{"path": row["path"], "classification": row["classification"]}
                          for row in original["inputs"]])
        excluded = {"schema_version", "mode", "detail", "assumptions_acknowledged",
                    "include_history", "scenarios"}
        expected_paths = set(data) - excluded
        expected_paths.update(f"scenarios.{index}.{field}"
                              for index, scenario in enumerate(data["scenarios"])
                              for field in scenario if field not in {"id", "name"})
        self.assertEqual({row["path"] for row in report["inputs"]}, expected_paths)
        for row in original["inputs"]:
            value = summary["assumptions"]
            for part in row["path"].split("."):
                value = value[int(part)] if isinstance(value, list) else value[part]
            self.assertEqual(value, row["value"])
            self.assertEqual(row["origin"], "user_supplied")
        for collection in ("constraints", "conflicts"):
            reconstructed = [
                {**row, **report["evidence"][row["parameter_id"]]}
                for row in report[collection]
            ]
            self.assertEqual(reconstructed, original[collection])
        self.assertEqual({row["input_path"] for row in report["conflicts"]},
                         {"initial_branches", "max_branches", "selective_target",
                          "daily_license_limit", "scenarios.0.multiplier"})
        reconstructed = []
        for row in report["unresolved"]:
            reconstructed.append({
                "path": row["path"], "explanation": row["explanation"],
                "evidence": [{"parameter_id": identifier, **report["evidence"][identifier]}
                             for identifier in row["parameter_ids"]],
            })
        self.assertEqual(reconstructed,
                         [{key: value for key, value in row.items() if key != "value"}
                          for row in original["unresolved"]])
        self.assertEqual(report["parameter_files"], original["parameter_files"])
        self.assertNotIn("assumptions", report)
        self.assertNotIn("limitations", report)
        self.assertNotIn("value", report["inputs"][0])
        self.assertNotIn("documented_value", report["constraints"][0])
        self.assertNotIn("evidence", report["unresolved"][0])

    def test_documented_block_preserves_input_values_with_selected_report_detail(self):
        for detail in ("summary", "full"):
            with self.subTest(detail=detail):
                data = inputs(mode="documented", detail=detail, max_branches=11,
                              funding="credits", license_cost_tokens="7.5")
                blocked = self.assert_error(invoke(data), 3, "documented_rule_conflict")
                report = blocked["conformance"]
                self.assertEqual(blocked["detail"], detail)
                self.assert_report(report, "documented", "blocked")
                self.assertEqual(blocked["assumptions"]["max_branches"], 11)
                self.assertEqual(blocked["assumptions"]["funding"], "credits")
                self.assertEqual(blocked["assumptions"]["license_cost_tokens"], "7.5")
                allowed = calculate({**data, "mode": "stress"})
                self.assertEqual(report["inputs"], allowed["conformance"]["inputs"])
                self.assertEqual(report["conflicts"], allowed["conformance"]["conflicts"])
                if detail == "summary":
                    self.assertEqual(report["evidence"], allowed["conformance"]["evidence"])
                    self.assertNotIn("assumptions", report)
                else:
                    self.assertIn("assumptions", report)

    def test_unknown_detail_and_hidden_history_fail_without_results(self):
        for detail in ("verbose", "", None, True, 1, ["full"]):
            with self.subTest(detail=detail):
                self.assert_error(invoke(inputs(detail=detail)), 2, "invalid_input")
        explicit = inputs(detail="summary", include_history=True)
        implicit = inputs(include_history=True)
        del implicit["detail"]
        for data in (explicit, implicit):
            self.assert_error(invoke(data), 2, "invalid_input")
        result = calculate(inputs(detail="full", include_history=True))
        history = strategy(result, "aggressive")["history"]
        self.assertEqual([day["day"] for day in history], [1, 2])
        self.assertEqual(history[-1]["branches"],
                         strategy(result, "aggressive")["branches_before_exit"])


class PlannerPackageData(PlannerContract):
    def test_missing_safe_read_capability_fails_without_traceback(self):
        probe = (
            "import os,runpy,sys; os.supports_dir_fd=set(); "
            "sys.argv=[sys.argv[1]]; runpy.run_path(sys.argv[0],run_name='__main__')"
        )
        for mode in ("documented", "stress"):
            result = subprocess.run(
                [sys.executable, "-B", "-I", "-c", probe, str(SCRIPT)],
                input=json.dumps(inputs(mode=mode)).encode(), capture_output=True,
                timeout=20, check=False,
            )
            self.assert_error(result, 4, "package_data_error")

    def assert_package_failure(self, script, forbidden_reads=()):
        for mode in ("documented", "stress"):
            with self.subTest(mode=mode):
                self.assert_error(invoke(inputs(mode=mode), script=script,
                                         forbidden_reads=forbidden_reads),
                                  4, "package_data_error")

    def test_missing_malformed_and_oversize_fixed_resources_fail_closed(self):
        for name in PARAMETER_NAMES:
            for damage in ("missing", "malformed", "oversize", "directory"):
                with self.subTest(file=name, damage=damage), tempfile.TemporaryDirectory() as directory:
                    script = copy_package(directory)
                    path = script.parents[1] / "assets/parameters" / name
                    if damage == "missing":
                        path.unlink()
                    elif damage == "malformed":
                        path.write_bytes(b'{"records":')
                    elif damage == "oversize":
                        # Otherwise valid JSON must fail solely for exceeding the byte bound.
                        raw = path.read_bytes()
                        path.write_bytes(raw + b" " * (65537 - len(raw)))
                    else:
                        path.unlink()
                        path.mkdir()
                    self.assert_package_failure(script)

    def test_symlinked_resource_and_ancestor_never_open_escaped_files(self):
        for target in ("file", "internal_file", "parameter_directory"):
            with self.subTest(target=target), tempfile.TemporaryDirectory() as directory:
                script = copy_package(directory)
                parameters = script.parents[1] / "assets/parameters"
                if target in {"file", "internal_file"}:
                    path = parameters / "participation.json"
                    outside = (parameters / "unlisted.json" if target == "internal_file"
                               else Path(directory) / "outside.json")
                    shutil.copy2(path, outside)
                    path.unlink()
                    path.symlink_to(outside)
                else:
                    path = parameters
                    outside = Path(directory) / "outside"
                    parameters.rename(outside)
                    parameters.symlink_to(outside, target_is_directory=True)
                self.assert_package_failure(script, forbidden_reads=(path, outside))

    def test_malformed_parameter_schema_and_known_constraints_fail_closed(self):
        cases = [
            ("duplicate_key", "participation.json", None, None, None),
            ("schema", "participation.json", None, None, 2),
            ("duplicate_id", "participation.json", "maximum-branches", None, None),
            ("missing_record", "launch.json", "whitelist-liquidity-fee", None, None),
            ("record", "participation.json", "maximum-branches", None, None),
            ("field", "participation.json", "maximum-branches", "unit", "STANDARD"),
            ("field", "participation.json", "maximum-branches", "status", "not-established"),
            ("field", "participation.json", "maximum-branches", "value", True),
            ("field", "participation.json", "maximum-branches", "value", None),
            ("field", "participation.json", "maximum-branches", "value", 0),
            ("field", "participation.json", "maximum-branches", "value", 10.5),
            ("field", "participation.json", "licenses-per-charter-per-day", "value", -1),
            ("field", "participation.json", "licenses-per-charter-per-day", "value", 3.5),
            ("field", "monetary.json", "issuance-budget", "value", "NaN"),
            ("field", "monetary.json", "base-issuance", "value", None),
            ("field", "monetary.json", "base-issuance", "status", "not-established"),
            ("missing_record", "participation.json", "resolution-fee-floor", None, None),
            ("field", "participation.json", "resolution-fee-floor", "value", 61),
            ("field", "participation.json", "resolution-fee-ceiling", "value", 101),
            ("field", "participation.json", "resolution-fee-ceiling", "unit", "fraction"),
            ("missing_record", "monetary.json", "multiplier-floor", None, None),
            ("field", "monetary.json", "multiplier-floor", "value", None),
            ("field", "monetary.json", "multiplier-floor", "value", -0.2),
            ("field", "monetary.json", "multiplier-floor", "value", 1.5),
            ("field", "monetary.json", "multiplier-ceiling", "unit", "percent"),
            ("field", "monetary.json", "multiplier-ceiling", "status", "not-established"),
        ]
        for damage, name, identifier, field, value in cases:
            with self.subTest(damage=damage, id=identifier, field=field, value=value):
                with tempfile.TemporaryDirectory() as directory:
                    script = copy_package(directory)
                    path = script.parents[1] / "assets/parameters" / name
                    document = json.loads(path.read_bytes())
                    if damage == "duplicate_key":
                        raw = json.dumps(document).replace('"schema_version": 1',
                                                          '"schema_version": 1, "schema_version": 1', 1)
                    else:
                        if damage == "schema":
                            document["schema_version"] = value
                        elif damage == "duplicate_id":
                            document["records"].append(dict(parameter_record(document, identifier)))
                        elif damage == "missing_record":
                            document["records"] = [row for row in document["records"] if row["id"] != identifier]
                        elif damage == "record":
                            document["records"][0] = []
                        else:
                            parameter_record(document, identifier)[field] = value
                        raw = json.dumps(document)
                    path.write_text(raw, encoding="utf-8")
                    self.assert_package_failure(script)

    def test_changed_canonical_cap_controls_rules_and_report_digest(self):
        with tempfile.TemporaryDirectory() as directory:
            script = copy_package(directory)
            path = script.parents[1] / "assets/parameters/participation.json"
            original = path.read_bytes()
            document = json.loads(original)
            parameter_record(document, "maximum-branches")["value"] = 12
            path.write_text(json.dumps(document), encoding="utf-8")
            result = calculate(inputs(mode="documented", initial_branches=12,
                                      max_branches=12, selective_target=12), script=script)
            self.assert_report(result["conformance"], "documented", "within_checked_rules")
            entries = {row["path"]: row for row in result["conformance"]["inputs"]}
            self.assertEqual(entries["max_branches"]["classification"], "source_backed")
            self.assertEqual(strategy(result, "keep")["branches_before_exit"], 12)
            for row in result["conformance"]["constraints"]:
                if row["parameter_id"] == "maximum-branches":
                    self.assertEqual(Decimal(str(row["documented_value"])), Decimal(12))
            provenance = next(row for row in result["conformance"]["parameter_files"]
                              if row["path"] == "assets/parameters/participation.json")
            self.assertEqual(provenance["sha256"], hashlib.sha256(path.read_bytes()).hexdigest())
            self.assertNotEqual(provenance["sha256"], hashlib.sha256(original).hexdigest())
            blocked = self.assert_error(invoke(inputs(mode="documented", max_branches=13),
                                               script=script), 3, "documented_rule_conflict")
            self.assertEqual({row["input_path"] for row in blocked["conformance"]["conflicts"]},
                             {"max_branches"})

    def test_canonical_multiplier_bounds_control_rules_without_clamping(self):
        with tempfile.TemporaryDirectory() as directory:
            script = copy_package(directory)
            path = script.parents[1] / "assets/parameters/monetary.json"
            document = json.loads(path.read_bytes())
            parameter_record(document, "multiplier-floor")["value"] = "0.4"
            parameter_record(document, "multiplier-ceiling")["value"] = "1.5"
            path.write_text(json.dumps(document), encoding="utf-8")
            data = inputs(mode="documented")
            data["scenarios"][0]["multiplier"] = "0.3"
            blocked = self.assert_error(invoke(data, script=script), 3,
                                       "documented_rule_conflict")
            self.assertEqual({row["parameter_id"] for row in blocked["conformance"]["conflicts"]},
                             {"multiplier-floor"})
            stress = calculate({**data, "mode": "stress"}, script=script)
            entry = next(row for row in stress["conformance"]["inputs"]
                         if row["path"] == "scenarios.0.multiplier")
            self.assertEqual(entry["classification"], "inconsistent")
            self.assertEqual({row["parameter_id"]: row["conforms"] for row in entry["constraints"]},
                             {"multiplier-floor": False, "multiplier-ceiling": True})
            self.assertEqual(Decimal(strategy(stress, "keep")["credits_accrued"]), Decimal("0.6"))
            # The caller's in-range multiplier is used without replacement or clamping.
            data["scenarios"][0]["multiplier"] = "1.4"
            result = calculate(data, script=script)
            self.assert_report(result["conformance"], "documented", "within_checked_rules")
            self.assertEqual(Decimal(strategy(result, "keep")["credits_accrued"]), Decimal("2.8"))

    def test_published_base_ceiling_controls_bound_without_becoming_a_default(self):
        with tempfile.TemporaryDirectory() as directory:
            script = copy_package(directory)
            path = script.parents[1] / "assets/parameters/monetary.json"
            document = json.loads(path.read_bytes())
            parameter_record(document, "base-issuance")["value"] = "12345"
            path.write_text(json.dumps(document), encoding="utf-8")
            result = calculate(inputs(mode="documented"), script=script)
            report = result["conformance"]
            entry = next(row for row in report["inputs"] if row["path"] == "base_daily_issuance")
            self.assertEqual(entry["classification"], "unresolved")
            self.assertEqual(Decimal(str(entry["value"])), Decimal(100))
            self.assertEqual(Decimal(strategy(result, "keep")["credits_accrued"]), Decimal(2))
            blocked = self.assert_error(invoke(inputs(mode="documented", base_daily_issuance="12346"),
                                               script=script), 3, "documented_rule_conflict")
            self.assertEqual({row["parameter_id"] for row in blocked["conformance"]["conflicts"]},
                             {"base-issuance"})
            missing = inputs(mode="documented")
            del missing["base_daily_issuance"]
            self.assert_error(invoke(missing, script=script), 2, "invalid_input")


if __name__ == "__main__":
    unittest.main()
