#!/usr/bin/env python3
"""Hypothetical, offline scenario planner; Python 3 standard library only.

Usage: python3 -B -I scripts/scenario.py  (provide one JSON object on stdin)
Numeric inputs use JSON-number syntax, at most 80 characters, at most 30
Decimal coefficient digits, and a Decimal exponent from -18 through 18.
The input is limited to 65536 UTF-8 bytes and eight JSON nesting levels.
Arithmetic uses 50 significant decimal digits, not EVM integer arithmetic.
Only three fixed bundled parameter JSON files are read, once per simulation.
No network, environment, wallet, or transaction access is performed.
"""

import hashlib
import json
import os
import re
import stat
import sys
import unicodedata
from datetime import datetime
from pathlib import Path
from decimal import (
    Context, Decimal, DecimalException, DivisionByZero, InvalidOperation,
    Overflow, ROUND_HALF_EVEN, localcontext,
)


MAX_INPUT_BYTES = 65536
MAX_PARAMETER_BYTES = 65536
WARNING = "Hypothetical—not contract-verified or a forecast."
MAX_DEPTH = 8
PRECISION = 50
ZERO = Decimal(0)
ONE = Decimal(1)
HUNDRED = Decimal(100)
NUMBER = re.compile(r"-?(?:0|[1-9][0-9]*)(?:\.[0-9]+)?(?:[eE][+-]?[0-9]+)?\Z")
IDENTIFIER = re.compile(r"[a-z0-9-]{1,40}\Z")

INTEGER_FIELDS = {
    "schema_version": (1, 1),
    "days": (1, 365),
    "initial_branches": (1, 100),
    "other_branches": (0, 1000000000),
    "max_branches": (1, 100),
    "daily_license_limit": (0, 100),
    "selective_target": (1, 100),
    "selective_interval_days": (1, 365),
}
DECIMAL_FIELDS = {
    "initial_credits": (0, 10**12),
    "base_daily_issuance": (0, 10**12),
    "remaining_issuance_budget": (0, 10**15),
    "initial_token_price_eth": (0, 1000),
    "entry_cost_eth": (0, 10**6),
    "entry_gas_eth": (0, 100),
    "license_cost_tokens": (0, 10**12),
    "license_gas_eth": (0, 100),
    "expansion_budget_eth": (0, 10**6),
    "buy_cost_markup_pct": (0, 10000),
    "sale_fee_pct": (0, 100),
    "sale_slippage_pct": (0, 100),
    "exit_gas_eth": (0, 100),
}
SCENARIO_DECIMALS = {
    "multiplier": (0, 100),
    "other_branch_growth_pct": (-20, 20),
    "price_growth_pct": (-20, 20),
    "resolution_fee_pct": (0, 100),
    "sale_tax_pct": (0, 100),
}
REQUIRED_KEYS = frozenset(INTEGER_FIELDS) | frozenset(DECIMAL_FIELDS) | {
    "assumptions_acknowledged", "mode", "funding", "exit_mode", "scenarios"
}
SCENARIO_KEYS = frozenset(SCENARIO_DECIMALS) | {"id", "name"}
LIMITATIONS = [
    "Economic inputs are user assumptions. Checked rules are partial packaged "
    "publisher statements, not live quotes or contract verification.",
    "The engine reads only three fixed bundled parameter JSON files, once per "
    "simulation. It does not read environment variables, contracts, or the "
    "network, and does not sign, submit, or simulate real transactions.",
    "Arithmetic uses 50 significant Decimal digits, not EVM-exact integer "
    "accounting. Inputs allow at most 30 coefficient digits, exponent -18..18, "
    "and 80 numeric characters; CLI JSON is at most 65536 bytes and depth 8.",
    "Strategies are independent counterfactuals on the same exogenous daily "
    "price, external-branch, and gross issuance-budget paths. Global issuance "
    "depletes once daily; burns and cancellations never replenish its budget.",
    "Purchases precede daily accrual. Day 1 uses the initial price and external "
    "branch count; both compound at each day end. Terminal sales use the "
    "post-final-day price. External branches are a fractional approximation.",
    "External funding buys license tokens at the marked-up start-of-day price; "
    "credits funding uses only already accrued or initial credits and external "
    "gas, with no token top-ups. Skipped attempts incur no charge.",
    "The expansion budget includes license acquisition cash and license gas, "
    "but excludes entry and exit costs. Free licenses remain subject to caps.",
    "Resolution releases a pro-rata share of credits, then deducts the assumed "
    "resolution fee. All released wallet tokens are assumed sold. Sale tax, "
    "regular sale fee, and slippage are sequential haircuts, a model assumption "
    "rather than an asserted protocol tax formula.",
    "Retained charter branches and credits receive no residual valuation. "
    "Partial-exit and no-exit cash P&L are not total returns. Break-even price "
    "is reported only for exit_mode all with a positive net token denominator.",
    "No probability, strategy recommendation, future liquidity guarantee, "
    "or realized return is implied. Entry cost and initial credits are supplied "
    "by the caller; no entry price or per-branch price is inferred.",
    "Matching a publisher cap does not verify a live position or establish "
    "protocol feasibility. The displayed frontend policy range is not a "
    "verified on-chain multiplier bound.",
    "The model does not check global auction inventory, endogenous external "
    "branch growth, continuous policy/accrual, fee redistribution, dormancy, "
    "or whether credits can actually pay for licenses.",
    "Acquisition context, license pricing, resolution and sale fee/tax bases "
    "and their application remain unchecked assumptions, even in documented mode.",
]
SUMMARY_LIMITATIONS = [
    "All economic values are user assumptions; publisher checks are partial, "
    "not live quotes, contract verification, or proof of feasibility.",
    "Offline Decimal counterfactuals, not EVM accounting or executable transactions; "
    "shared exogenous price, external-branch and gross issuance paths exclude "
    "endogenous growth, continuous accrual, dormancy and fee redistribution.",
    "Acquisition and license prices, auction inventory, resolution and sale fee/tax "
    "bases, continuous policy and credits-payment feasibility remain unchecked; "
    "the frontend multiplier range is not an on-chain bound. Sequential sale "
    "haircuts are a model assumption.",
    "Retained branches and credits have no residual valuation; partial/no-exit "
    "cash P&L is not total return. No forecast, recommendation or liquidity guarantee.",
]
SUMMARY_STRATEGY_FIELDS = (
    "strategy", "warning", "branches_before_exit", "branches_retired",
    "branches_after_exit", "charter_retained", "credits_accrued", "credits_spent",
    "credits_retained", "wallet_tokens_before_sale", "expansion_eth_spent",
    "total_outlay_eth", "estimated_eth_recovered", "net_cash_eth",
    "delta_vs_keep_eth", "break_even_price_eth", "licenses_bought", "skipped_attempts",
)


class InputError(ValueError):
    """A bounded, user-facing input validation error."""


class PackageDataError(ValueError):
    """The fixed packaged rule catalog cannot be safely used."""


class ConformanceError(ValueError):
    """Documented mode was blocked before computing any strategy."""

    def __init__(self, report, assumptions):
        super().__init__("inputs conflict with checked packaged publisher statements")
        self.warning = WARNING
        self.report = _serialize(report)
        self.assumptions = _serialize(assumptions)
        self.detail = assumptions["detail"]


def _decimal(value, field):
    if isinstance(value, bool) or not isinstance(value, (str, int, float, Decimal)):
        raise InputError(field + " must be a number or numeric string, not a boolean")
    if isinstance(value, int) and value.bit_length() > 100:
        raise InputError(field + " exceeds the 30-digit numeric input limit")
    if isinstance(value, Decimal):
        number = value
    else:
        text = str(value)
        if len(text) > 80 or not NUMBER.fullmatch(text):
            raise InputError(field + " must use JSON-number syntax in at most 80 characters")
        try:
            number = Decimal(text)
        except DecimalException:
            raise InputError(field + " is not a representable decimal") from None
    if not number.is_finite():
        raise InputError(field + " must be finite (NaN and Infinity are forbidden)")
    parts = number.as_tuple()
    if len(parts.digits) > 30 or not -18 <= parts.exponent <= 18:
        raise InputError(field + " requires at most 30 coefficient digits and exponent -18..18")
    return number


def _bounded_number(value, field, limits, integer=False):
    number = _decimal(value, field)
    low, high = limits
    if number < low or number > high:
        raise InputError(field + " must be between " + str(low) + " and " + str(high))
    if integer:
        if number != number.to_integral_value():
            raise InputError(field + " must be an integer")
        return int(number)
    return number


def _keys(value, required, optional, field):
    if not isinstance(value, dict):
        raise InputError(field + " must be an object")
    if any(not isinstance(key, str) for key in value):
        raise InputError(field + " keys must be strings")
    unknown = value.keys() - required - optional
    if unknown:
        raise InputError(field + " contains unknown keys")
    missing = required - value.keys()
    if missing:
        raise InputError(field + " is missing required keys: " + ", ".join(sorted(missing)))


def _validate(config):
    _keys(config, REQUIRED_KEYS, {"include_history", "detail"}, "config")
    if config["assumptions_acknowledged"] is not True:
        raise InputError("assumptions_acknowledged must be true")
    normalized = {"assumptions_acknowledged": True}
    for field, limits in INTEGER_FIELDS.items():
        normalized[field] = _bounded_number(config[field], field, limits, integer=True)
    for field, limits in DECIMAL_FIELDS.items():
        normalized[field] = _bounded_number(config[field], field, limits)
    if normalized["max_branches"] < normalized["initial_branches"]:
        raise InputError("max_branches must be at least initial_branches")
    if not normalized["initial_branches"] <= normalized["selective_target"] <= normalized["max_branches"]:
        raise InputError("selective_target must be between initial_branches and max_branches")
    for field, choices in (
        ("mode", ("documented", "stress")),
        ("funding", ("external", "credits")),
        ("exit_mode", ("all", "one", "none")),
    ):
        if not isinstance(config[field], str) or config[field] not in choices:
            raise InputError(field + " must be one of: " + ", ".join(choices))
        normalized[field] = config[field]
    detail = config.get("detail", "summary")
    if not isinstance(detail, str) or detail not in ("summary", "full"):
        raise InputError("detail must be one of: summary, full")
    normalized["detail"] = detail
    include_history = config.get("include_history", False)
    if not isinstance(include_history, bool):
        raise InputError("include_history must be a boolean")
    if include_history and detail != "full":
        raise InputError("include_history true requires detail full")
    normalized["include_history"] = include_history
    scenarios = config["scenarios"]
    if not isinstance(scenarios, list) or not 1 <= len(scenarios) <= 9:
        raise InputError("scenarios must be an array containing 1..9 scenarios")
    normalized["scenarios"] = []
    identifiers = set()
    for index, scenario in enumerate(scenarios):
        prefix = "scenarios[" + str(index) + "]"
        _keys(scenario, SCENARIO_KEYS, set(), prefix)
        identifier = scenario["id"]
        if not isinstance(identifier, str) or not IDENTIFIER.fullmatch(identifier):
            raise InputError(prefix + ".id must match [a-z0-9-]{1,40}")
        if identifier in identifiers:
            raise InputError("scenario ids must be unique")
        identifiers.add(identifier)
        name = scenario["name"]
        if not isinstance(name, str) or not 1 <= len(name) <= 80 or any(
            unicodedata.category(character).startswith("C") for character in name
        ):
            raise InputError(prefix + ".name must contain 1..80 plain characters without controls")
        item = {"id": identifier, "name": name}
        for field, limits in SCENARIO_DECIMALS.items():
            item[field] = _bounded_number(scenario[field], prefix + "." + field, limits)
        normalized["scenarios"].append(item)
    return normalized


def _text(number):
    if not number:
        return "0"
    return format(number.normalize(), "f")


def _serialize(value):
    if isinstance(value, Decimal):
        return _text(value)
    if isinstance(value, dict):
        return {key: _serialize(item) for key, item in value.items()}
    if isinstance(value, list):
        return [_serialize(item) for item in value]
    return value


# Only these canonical IDs have reviewed application semantics. No economic
# values are duplicated here, and future formula values do not become rules.
PARAMETER_IDS = {
    "participation.json": (
        "maximum-branches", "licenses-per-charter-per-day",
        "license-floor-formula", "resolution-fee-formula",
    ),
    "monetary.json": (
        "issuance-budget", "frontend-policy-range", "base-issuance",
        "trading-fee", "multiplier-update-rule",
    ),
    "launch.json": ("launch-trading-tax-curve", "whitelist-liquidity-fee"),
}
CAP_UNITS = {
    "maximum-branches": "branches per charter",
    "licenses-per-charter-per-day": "licenses per charter per day",
    "issuance-budget": "STANDARD cumulative issuance",
}
CONTEXT_UNITS = {
    "base-issuance": "STANDARD per day",
    "license-floor-formula": "STANDARD price rule",
    "resolution-fee-formula": "fee rule",
    "trading-fee": "fee rate; basis not disclosed",
    "multiplier-update-rule": "policy rule",
    "launch-trading-tax-curve": "complete applied fee rule",
    "whitelist-liquidity-fee": "ETH per whitelist mint",
}
PARAMETER_STATUSES = frozenset((
    "documented-visible", "documented-approximate", "redacted",
    "not-established", "announced",
    "observed frontend publication, not deployed configuration",
))


def _plain_text(value):
    return isinstance(value, str) and bool(value) and not any(
        unicodedata.category(character).startswith("C") for character in value
    )


def _record_schema(record):
    _keys(record, {"id", "value", "unit", "status", "source_ids", "locator", "limits"},
          {"history"}, "parameter record")
    if not isinstance(record["id"], str) or not IDENTIFIER.fullmatch(record["id"]):
        raise InputError("invalid parameter id")
    if not _plain_text(record["unit"]) or not _plain_text(record["locator"]):
        raise InputError("invalid parameter metadata")
    if not isinstance(record["status"], str) or record["status"] not in PARAMETER_STATUSES:
        raise InputError("invalid parameter status")
    value = record["value"]
    if value is not None:
        if isinstance(value, Decimal):
            _decimal(value, "parameter value")
        elif isinstance(value, str):
            if not _plain_text(value):
                raise InputError("invalid parameter value")
        elif isinstance(value, dict) and record["id"] == "frontend-policy-range":
            _keys(value, {"minimum", "maximum"}, set(), "frontend range")
        else:
            raise InputError("unsupported parameter value format")
    sources = record["source_ids"]
    if (not isinstance(sources, list) or not sources
            or any(not _plain_text(source) for source in sources)
            or len(set(sources)) != len(sources)):
        raise InputError("invalid parameter sources")
    limits = record["limits"]
    if not isinstance(limits, list) or any(not _plain_text(limit) for limit in limits):
        raise InputError("invalid parameter limits")
    if "history" in record:
        if not isinstance(record["history"], list):
            raise InputError("invalid parameter history")
        for historical in record["history"]:
            _keys(historical, {"value", "unit", "status", "observed_at",
                              "source_ids", "locator", "limits"}, set(), "parameter history")
            if historical["status"] != "superseded" or not _plain_text(historical["observed_at"]):
                raise InputError("invalid parameter history")
            # Validate historical metadata without treating it as an active rule.
            prior = {key: value for key, value in historical.items() if key != "observed_at"}
            prior.update(id=record["id"], status="documented-visible")
            _record_schema(prior)


def _read_parameter_file(directory, filename):
    """Read a fixed regular file without following links, including races."""
    before = os.stat(filename, dir_fd=directory, follow_symlinks=False)
    if not stat.S_ISREG(before.st_mode) or before.st_size > MAX_PARAMETER_BYTES:
        raise InputError("unsafe parameter file")
    descriptor = os.open(
        filename, os.O_RDONLY | os.O_NOFOLLOW | os.O_NONBLOCK, dir_fd=directory,
    )
    try:
        opened = os.fstat(descriptor)
        if (not stat.S_ISREG(opened.st_mode) or opened.st_size > MAX_PARAMETER_BYTES
                or (before.st_dev, before.st_ino) != (opened.st_dev, opened.st_ino)):
            raise InputError("unsafe parameter file")
        chunks = []
        size = 0
        while size <= MAX_PARAMETER_BYTES:
            chunk = os.read(descriptor, MAX_PARAMETER_BYTES + 1 - size)
            if not chunk:
                break
            chunks.append(chunk)
            size += len(chunk)
        if size > MAX_PARAMETER_BYTES:
            raise InputError("oversized parameter file")
        return b"".join(chunks)
    finally:
        os.close(descriptor)


def _load_parameters():
    """Load only the three fixed resources below the real installed root."""
    if (not all(hasattr(os, flag) for flag in ("O_DIRECTORY", "O_NOFOLLOW", "O_NONBLOCK"))
            or os.open not in os.supports_dir_fd or os.stat not in os.supports_dir_fd
            or os.stat not in os.supports_follow_symlinks):
        raise PackageDataError("host lacks required safe descriptor-relative parameter reads")
    descriptors = []
    try:
        root = Path(__file__).resolve(strict=True).parent.parent
        directory = os.open(root, os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW)
        descriptors.append(directory)
        for component in ("assets", "parameters"):
            before = os.stat(component, dir_fd=directory, follow_symlinks=False)
            if not stat.S_ISDIR(before.st_mode):
                raise InputError("unsafe parameter directory")
            directory = os.open(
                component, os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW, dir_fd=directory,
            )
            descriptors.append(directory)
            opened = os.fstat(directory)
            if (before.st_dev, before.st_ino) != (opened.st_dev, opened.st_ino):
                raise InputError("parameter directory changed")
        records = {}
        seen = set()
        files = []
        for filename, required in PARAMETER_IDS.items():
            raw = _read_parameter_file(directory, filename)
            text = raw.decode("utf-8")
            _check_depth(text)
            package = json.loads(
                text, parse_int=lambda value: _decimal(value, "parameter number"),
                parse_float=lambda value: _decimal(value, "parameter number"),
                parse_constant=_constant, object_pairs_hook=_pairs,
            )
            _keys(package, {"schema_version", "scope", "reviewed_at", "records"},
                  set(), "parameter package")
            if isinstance(package["schema_version"], bool) or package["schema_version"] != 1:
                raise InputError("unsupported parameter schema")
            if not _plain_text(package["scope"]) or not _plain_text(package["reviewed_at"]):
                raise InputError("invalid parameter package metadata")
            timestamp = datetime.fromisoformat(package["reviewed_at"].replace("Z", "+00:00"))
            if timestamp.tzinfo is None:
                raise InputError("parameter review timestamp requires timezone")
            if not isinstance(package["records"], list):
                raise InputError("invalid parameter records")
            found = set()
            for record in package["records"]:
                _record_schema(record)
                identifier = record["id"]
                if identifier in seen:
                    raise InputError("duplicate parameter id")
                seen.add(identifier)
                if identifier in required:
                    records[identifier] = record
                    found.add(identifier)
            if found != set(required):
                raise InputError("missing required parameter")
            files.append({
                "path": "assets/parameters/" + filename,
                "sha256": hashlib.sha256(raw).hexdigest(),
                "reviewed_at": package["reviewed_at"],
            })
        for identifier, unit in CAP_UNITS.items():
            record = records[identifier]
            if record["unit"] != unit or record["status"] != "documented-visible":
                raise InputError("unsupported cap metadata")
            value = _decimal(record["value"], "parameter cap")
            if value < ZERO or value != value.to_integral_value():
                raise InputError("parameter caps must be nonnegative integers")
            if identifier == "maximum-branches" and value <= ZERO:
                raise InputError("maximum branches must be positive")
            record["value"] = value
        frontend = records["frontend-policy-range"]
        if (frontend["unit"] != "multiplier range displayed by protocol page"
                or frontend["status"] != "observed frontend publication, not deployed configuration"):
            raise InputError("unsupported frontend range metadata")
        _keys(frontend["value"], {"minimum", "maximum"}, set(), "frontend range")
        bounds = {
            key: _decimal(value, "frontend range")
            for key, value in frontend["value"].items()
        }
        if not ZERO <= bounds["minimum"] <= bounds["maximum"]:
            raise InputError("invalid frontend range")
        frontend["value"] = bounds
        for identifier, unit in CONTEXT_UNITS.items():
            if records[identifier]["unit"] != unit:
                raise InputError("unsupported contextual parameter unit")
        return records, files
    except (OSError, ValueError, DecimalException, RecursionError, RuntimeError):
        # Do not disclose filesystem paths, file content, or decoder details.
        raise PackageDataError("fixed bundled parameter data is missing, unsafe, or invalid") from None
    finally:
        for descriptor in reversed(descriptors):
            os.close(descriptor)


def _evidence(record):
    sources = record["source_ids"]
    kind = ("frontend_publication" if record["id"] == "frontend-policy-range"
            else "official_announcement" if any(source.startswith("sr-post-") for source in sources)
            else "whitepaper")
    return {
        "parameter_id": record["id"], "documented_value": record["value"],
        "unit": record["unit"], "status": record["status"],
        "source_ids": list(sources), "locator": record["locator"],
        "source_kind": kind, "source_limits": list(record["limits"]),
    }


def _conformance(config, records, files):
    full = config["detail"] == "full"
    constraints = []
    by_path = {}
    evidence = {}

    def cite(identifier):
        if identifier not in evidence:
            item = _evidence(records[identifier])
            del item["parameter_id"]
            evidence[identifier] = item

    def check(path, value, identifier, relation):
        record = records[identifier]
        documented = record["value"]
        conforms = (value <= documented if relation == "<=" else
                    documented["minimum"] <= value <= documented["maximum"])
        constraint = {
            "input_path": path, "provided_value": value, "relation": relation,
            "parameter_id": identifier, "conforms": conforms,
        }
        if full:
            constraint.update(_evidence(record))
        else:
            cite(identifier)
        constraints.append(constraint)
        by_path[path] = constraint

    for field in ("initial_branches", "max_branches", "selective_target"):
        check(field, config[field], "maximum-branches", "<=")
    check("daily_license_limit", config["daily_license_limit"], "licenses-per-charter-per-day", "<=")
    check("remaining_issuance_budget", config["remaining_issuance_budget"], "issuance-budget", "<=")
    for index, scenario in enumerate(config["scenarios"]):
        check("scenarios." + str(index) + ".multiplier", scenario["multiplier"],
              "frontend-policy-range", "within_inclusive")

    unresolved_fields = {
        "base_daily_issuance": ("base-issuance", "User-supplied base issuance; source rate semantics remain unresolved."),
        "license_cost_tokens": ("license-floor-formula", "User-supplied fixed license cost is a proxy, not an established auction or floor quote."),
        "sale_fee_pct": ("trading-fee", "User-supplied sale fee; source rate and applied fee basis remain unresolved."),
        "entry_cost_eth": ("whitelist-liquidity-fee", "User-supplied acquisition cost; whitelist mint pricing is context only, not a universal entry cost or bound."),
        "resolution_fee_pct": ("resolution-fee-formula", "User-supplied resolution fee is a proxy for unresolved dynamic fee semantics."),
        "sale_tax_pct": ("launch-trading-tax-curve", "User-supplied sale tax is a proxy; timing, decay, basis, and applied tax rule remain unresolved."),
        "multiplier": ("multiplier-update-rule", "User-supplied constant multiplier is a proxy; frontend range checks do not resolve continuous policy or establish on-chain bounds."),
    }
    inputs = []
    unresolved = []

    def describe(path, field, value):
        classification = "user_selected"
        explanation = "User-selected scenario assumption; not verified against a live protocol or position."
        constraint = by_path.get(path)
        if constraint is not None:
            if constraint["conforms"]:
                explanation = "User-selected value within a checked publisher bound; not a verified live position or protocol parameter."
            if (field in ("max_branches", "daily_license_limit")
                    and value == records[constraint["parameter_id"]]["value"]):
                classification = "source_backed"
                explanation = "Matches the packaged publisher cap only; not contract-verified or a live configuration claim."
        unknown = unresolved_fields.get(field)
        if field == "funding" and value == "credits":
            unknown = ("license-floor-formula", "User-selected credits funding is an unchecked payment-feasibility assumption; the model does not establish that internal credits can pay for licenses.")
        source_evidence = None
        if unknown is not None:
            identifier, explanation = unknown
            classification = "unresolved"
            if full:
                source_evidence = [_evidence(records[identifier])]
                unresolved.append({
                    "path": path, "value": value, "explanation": explanation,
                    "evidence": source_evidence,
                })
            else:
                cite(identifier)
                unresolved.append({
                    "path": path, "explanation": explanation,
                    "parameter_ids": [identifier],
                })
        if constraint is not None and not constraint["conforms"]:
            classification = "inconsistent"
            explanation = "Conflicts with the checked packaged publisher statement; allowed only in stress mode. " + explanation
        entry = {"path": path, "classification": classification}
        if full:
            entry.update(value=value, origin="user_supplied", explanation=explanation)
            if constraint is not None:
                entry["constraints"] = [constraint]
            if source_evidence is not None:
                entry["evidence"] = source_evidence
        inputs.append(entry)

    for field in INTEGER_FIELDS:
        if field != "schema_version":
            describe(field, field, config[field])
    for field in DECIMAL_FIELDS:
        describe(field, field, config[field])
    for field in ("funding", "exit_mode"):
        describe(field, field, config[field])
    for index, scenario in enumerate(config["scenarios"]):
        for field in SCENARIO_DECIMALS:
            describe("scenarios." + str(index) + "." + field, field, scenario[field])
    conflicts = [constraint for constraint in constraints if not constraint["conforms"]]
    status = ("within_checked_rules" if not conflicts else
              "blocked" if config["mode"] == "documented" else "conflicts_allowed_in_stress")
    report = {
        "mode": config["mode"], "status": status,
        "scope": "partial checks against packaged publisher statements, not contract verification",
        "contract_verified": False, "constraints": constraints, "conflicts": conflicts,
        "inputs": inputs, "unresolved": unresolved,
        "parameter_files": files,
        "counts": {"checked": len(constraints), "conflicts": len(conflicts), "unresolved": len(unresolved)},
    }
    if full:
        report["assumptions"] = [dict(entry) for entry in inputs if entry["classification"] != "source_backed"]
        report["limitations"] = list(LIMITATIONS)
    else:
        report["evidence"] = evidence
    return report


def _path(config, scenario):
    """Compute one shared exogenous path, depleting gross issuance only once."""
    price = config["initial_token_price_eth"]
    others = Decimal(config["other_branches"])
    budget = config["remaining_issuance_budget"]
    issuance = config["base_daily_issuance"] * scenario["multiplier"]
    price_factor = ONE + scenario["price_growth_pct"] / HUNDRED
    branch_factor = ONE + scenario["other_branch_growth_pct"] / HUNDRED
    path = []
    for day in range(1, config["days"] + 1):
        daily_issuance = min(issuance, budget)
        budget -= daily_issuance
        end_price = price * price_factor
        end_others = others * branch_factor
        path.append((day, price, others, daily_issuance, end_price, end_others))
        price, others = end_price, end_others
    return path, price


def _initial_state(config):
    return {
        "branches": config["initial_branches"],
        "credits": config["initial_credits"],
        "credits_accrued": ZERO,
        "credits_spent": ZERO,
        "license_tokens_purchased": ZERO,
        "license_eth_spent": ZERO,
        "license_gas_eth_spent": ZERO,
        "expansion_eth_spent": ZERO,
        "licenses_bought": 0,
        "skipped_attempts": 0,
        "purchases": [],
    }


def _attempt_count(config, strategy, day, branches):
    if strategy == "keep":
        return 0
    if strategy == "selective":
        if day == 1 or (day - 1) % config["selective_interval_days"]:
            return 0
        return min(1, config["daily_license_limit"], config["selective_target"] - branches)
    return min(config["daily_license_limit"], config["max_branches"] - branches)


def _purchase(config, state, day, price, attempts):
    if not attempts:
        return
    external = config["funding"] == "external"
    tokens = config["license_cost_tokens"]
    license_cash = tokens * price * (ONE + config["buy_cost_markup_pct"] / HUNDRED) if external else ZERO
    gas = config["license_gas_eth"]
    cost = license_cash + gas
    bought = 0
    for _ in range(attempts):
        if cost > config["expansion_budget_eth"] - state["expansion_eth_spent"]:
            break
        if not external and tokens > state["credits"]:
            break
        bought += 1
        state["branches"] += 1
        state["licenses_bought"] += 1
        state["license_eth_spent"] += license_cash
        state["license_gas_eth_spent"] += gas
        state["expansion_eth_spent"] = state["license_eth_spent"] + state["license_gas_eth_spent"]
        if external:
            state["license_tokens_purchased"] += tokens
        else:
            state["credits_spent"] += tokens
            state["credits"] = config["initial_credits"] + state["credits_accrued"] - state["credits_spent"]
    state["skipped_attempts"] += attempts - bought
    if bought:
        state["purchases"].append({
            "day": day,
            "branches_added": bought,
            "license_tokens_spent": tokens * bought,
            "external_eth_spent": cost * bought,
        })


def _terminal(config, scenario, strategy, state, price):
    branches = state["branches"]
    mode = config["exit_mode"]
    retired = branches if mode == "all" else (1 if mode == "one" else 0)
    credits = state["credits"]
    released = credits if retired == branches else credits * retired / branches
    retained = credits - released
    resolution_fee = released * scenario["resolution_fee_pct"] / HUNDRED
    wallet = released - resolution_fee
    gross = wallet * price
    tax = gross * scenario["sale_tax_pct"] / HUNDRED
    fee = (gross - tax) * config["sale_fee_pct"] / HUNDRED
    slippage = (gross - tax - fee) * config["sale_slippage_pct"] / HUNDRED
    recovered = gross - tax - fee - slippage
    outlay = (config["entry_cost_eth"] + config["entry_gas_eth"]
              + state["expansion_eth_spent"] + (config["exit_gas_eth"] if retired else ZERO))
    denominator = (wallet * (ONE - scenario["sale_tax_pct"] / HUNDRED)
                   * (ONE - config["sale_fee_pct"] / HUNDRED)
                   * (ONE - config["sale_slippage_pct"] / HUNDRED))
    break_even = outlay / denominator if mode == "all" and denominator > ZERO else None
    return {
        "strategy": strategy,
        "branches_before_exit": branches,
        "branches_retired": retired,
        "branches_after_exit": branches - retired,
        "charter_retained": branches > retired,
        "credits_accrued": state["credits_accrued"],
        "credits_spent": state["credits_spent"],
        "credits_before_exit": credits,
        "credits_released": released,
        "credits_retained": retained,
        "resolution_fee_tokens": resolution_fee,
        "wallet_tokens_before_sale": wallet,
        "license_tokens_purchased": state["license_tokens_purchased"],
        "license_eth_spent": state["license_eth_spent"],
        "license_gas_eth_spent": state["license_gas_eth_spent"],
        "expansion_eth_spent": state["expansion_eth_spent"],
        "total_outlay_eth": outlay,
        "gross_sale_eth": gross,
        "sale_tax_eth": tax,
        "sale_fee_eth": fee,
        "sale_slippage_eth": slippage,
        "estimated_eth_recovered": recovered,
        "net_cash_eth": recovered - outlay,
        "delta_vs_keep_eth": ZERO,
        "break_even_price_eth": break_even,
        "licenses_bought": state["licenses_bought"],
        "skipped_attempts": state["skipped_attempts"],
        "purchases": state["purchases"],
    }


def _strategy(config, scenario, strategy, path, final_price):
    state = _initial_state(config)
    history = [] if config["include_history"] else None
    for day, price, others, issuance, end_price, end_others in path:
        attempts = _attempt_count(config, strategy, day, state["branches"])
        _purchase(config, state, day, price, attempts)
        accrued = issuance * state["branches"] / (others + state["branches"])
        state["credits_accrued"] += accrued
        state["credits"] = config["initial_credits"] + state["credits_accrued"] - state["credits_spent"]
        if history is not None:
            history.append({
                "day": day,
                "branches": state["branches"],
                "other_branches": end_others,
                "credits": state["credits"],
                "token_price_eth": end_price,
                "expansion_eth_spent": state["expansion_eth_spent"],
            })
    result = _terminal(config, scenario, strategy, state, final_price)
    if history is not None:
        result["history"] = history
    return result


def simulate(config):
    """Return hypothetical results or raise InputError/PackageDataError/ConformanceError."""
    with localcontext(Context(
        prec=PRECISION, rounding=ROUND_HALF_EVEN, Emin=-999999, Emax=999999,
        capitals=1, clamp=0, flags=[], traps=[InvalidOperation, DivisionByZero, Overflow],
    )):
        normalized = _validate(config)
        records, files = _load_parameters()
        conformance = _conformance(normalized, records, files)
        if conformance["status"] == "blocked":
            raise ConformanceError(conformance, normalized)
        scenarios = []
        for scenario in normalized["scenarios"]:
            path, final_price = _path(normalized, scenario)
            results = [
                _strategy(normalized, scenario, strategy, path, final_price)
                for strategy in ("keep", "selective", "aggressive")
            ]
            baseline = results[0]["net_cash_eth"]
            for result in results:
                result["warning"] = WARNING
                result["delta_vs_keep_eth"] = result["net_cash_eth"] - baseline
            if normalized["detail"] == "summary":
                results = [
                    {field: result[field] for field in SUMMARY_STRATEGY_FIELDS}
                    for result in results
                ]
            scenarios.append({
                "warning": WARNING,
                "id": scenario["id"],
                "name": scenario["name"],
                "final_token_price_eth": final_price,
                "results": results,
            })
        return _serialize({
            "warning": WARNING,
            "schema_version": 1,
            "model_version": "1",
            "detail": normalized["detail"],
            "mode": normalized["mode"],
            "conformance": conformance,
            "classification": "hypothetical",
            "assumptions": normalized,
            "limitations": list(LIMITATIONS if normalized["detail"] == "full" else SUMMARY_LIMITATIONS),
            "scenarios": scenarios,
        })


def _pairs(pairs):
    result = {}
    for key, value in pairs:
        if key in result:
            raise InputError("duplicate JSON object key")
        result[key] = value
    return result


def _constant(_value):
    raise InputError("NaN and Infinity are forbidden")


def _check_depth(text):
    depth = 0
    quoted = False
    escaped = False
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
            if depth > MAX_DEPTH:
                raise InputError("JSON nesting must not exceed 8 levels")
        elif character in "]}":
            depth -= 1


def _load_stdin():
    raw = sys.stdin.buffer.read(MAX_INPUT_BYTES + 1)
    if len(raw) > MAX_INPUT_BYTES:
        raise InputError("stdin JSON must not exceed 65536 bytes")
    try:
        text = raw.decode("utf-8")
    except UnicodeDecodeError:
        raise InputError("stdin must be UTF-8 JSON") from None
    _check_depth(text)
    try:
        return json.loads(
            text,
            parse_int=lambda value: _decimal(value, "JSON number"),
            parse_float=lambda value: _decimal(value, "JSON number"),
            parse_constant=_constant,
            object_pairs_hook=_pairs,
        )
    except json.JSONDecodeError as error:
        raise InputError("invalid JSON at line " + str(error.lineno) + ", column " + str(error.colno)) from None


def main():
    if sys.argv[1:] == ["--help"]:
        sys.stdout.write(WARNING + "\n\n" + __doc__ + "\n")
        return 0
    try:
        if len(sys.argv) != 1:
            raise InputError("no arguments are accepted except --help; supply JSON on stdin")
        result = simulate(_load_stdin())
        rendered = json.dumps(result, ensure_ascii=True, allow_nan=False, separators=(",", ":"))
    except ConformanceError as error:
        sys.stderr.write(json.dumps({
            "warning": WARNING,
            "error": {"type": "documented_rule_conflict", "message": str(error)},
            "detail": error.detail,
            "assumptions": error.assumptions,
            "conformance": error.report,
        }, ensure_ascii=True, allow_nan=False) + "\n")
        return 3
    except PackageDataError as error:
        sys.stderr.write(json.dumps({
            "warning": WARNING,
            "error": {"type": "package_data_error", "message": str(error)},
        }, ensure_ascii=True, allow_nan=False) + "\n")
        return 4
    except (InputError, DecimalException, RecursionError) as error:
        message = str(error) if isinstance(error, InputError) else "input cannot be represented within model arithmetic limits"
        sys.stderr.write(json.dumps({
            "warning": WARNING, "error": {"type": "invalid_input", "message": message},
        }, ensure_ascii=True, allow_nan=False) + "\n")
        return 2
    sys.stdout.write(rendered + "\n")
    return 0


if __name__ == "__main__":
    sys.exit(main())
