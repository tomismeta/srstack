#!/usr/bin/env python3
"""Offline behavioral checks for canonical prices; never contact a live provider."""

import copy
import importlib.util
import io
import json
import os
from pathlib import Path
import tempfile
import threading
import time
import unittest
from unittest.mock import Mock, patch

ROOT = Path(__file__).resolve().parent.parent
SPEC = importlib.util.spec_from_file_location("sr_price", ROOT / "scripts/price.py")
price = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(price)
NOW = 1_789_500_000


class ProviderFixture:
    def __init__(self):
        target, _ = price._load_package()
        self.pair = {"chainId": "robinhood", "dexId": "uniswap", "labels": ["v4"],
                     "pairAddress": target["pool_id"],
                     "baseToken": {"address": target["token_address"]},
                     "quoteToken": {"address": price.ZERO_ADDRESS},
                     "priceUsd": "2.5000", "priceNative": "0.0012500"}
        self.body = {"pairs": [self.pair]}
        self.pool = {"type": "pool", "id": "robinhood_" + target["pool_id"],
                     "attributes": {"address": target["pool_id"], "name": "STANDARD / WETH",
                                    "base_token_price_usd": "3", "base_token_price_native_currency": "0.002"},
                     "relationships": {
                         "base_token": {"data": {"id": "robinhood_" + target["token_address"]}},
                         "quote_token": {"data": {"id": "robinhood_" + price.ZERO_ADDRESS}},
                         "dex": {"data": {"id": "uniswap-v4-robinhood"}}}}
        self.gt_body = {"data": self.pool}
        self.failures = {}
        self.requests = []

    def __call__(self, source, path, timeout, deadline, monotonic):
        self.requests.append((source, path, timeout, deadline))
        if source in self.failures:
            raise self.failures[source]
        return json.dumps(self.body if source == "dexscreener" else self.gt_body).encode()

    def run(self, **config):
        return price.price(dict({"schema_version": 1}, **config), transport=self, now=lambda: NOW)


def connection_fixture(body=b"{}", status=200, length=None):
    connection = Mock()
    response = connection.getresponse.return_value
    response.status = status
    response.getheader.return_value = length
    response.read1.side_effect = [body, b""]
    return connection


class PriceChecks(unittest.TestCase):
    def setUp(self):
        self.provider = ProviderFixture()

    def test_typed_quotes_and_one_fetch_gross_mark(self):
        result = self.provider.run(standard_amount="0012.500")
        self.assertEqual(result["status"], "ok")
        self.assertEqual(result["values"], {
            "standard_usd": {"value": "2.5", "unit": "USD/STANDARD"},
            "standard_eth": {"value": "0.00125", "unit": "ETH/STANDARD"}})
        self.assertEqual(result["valuation"]["standard_amount"], "12.5")
        self.assertEqual(result["valuation"]["gross_usd"], {"value": "31.25", "unit": "USD"})
        self.assertEqual(result["valuation"]["gross_eth"], {"value": "0.015625", "unit": "ETH"})
        self.assertEqual(len(self.provider.requests), 1)

    def test_no_amount_has_no_valuation_and_zero_is_not_missing(self):
        self.assertNotIn("valuation", self.provider.run())
        result = self.provider.run(standard_amount="000.000")
        self.assertEqual(result["valuation"]["standard_amount"], "0")
        self.assertEqual(result["valuation"]["gross_usd"]["value"], "0")
        self.assertEqual(result["valuation"]["gross_eth"]["value"], "0")

    def test_maximum_digits_multiply_exactly_beyond_decimal_default(self):
        from decimal import localcontext
        amount = "9" * 60 + "." + "9" * 18
        quote = "9" * 42 + "." + "9" * 36
        self.provider.pair["priceUsd"] = quote
        # Independent integer arithmetic oracle: both coefficients are 10**78-1.
        coefficient = str((10 ** 78 - 1) ** 2)
        expected = coefficient[:-54] + "." + coefficient[-54:]
        with localcontext() as context:
            context.prec = 6
            result = self.provider.run(standard_amount=amount)
        self.assertEqual(result["valuation"]["gross_usd"]["value"], expected)
        self.assertEqual(result["values"]["standard_usd"]["value"], quote)

    def test_input_denials_precede_any_fetch(self):
        bad = [None, [], {}, {"schema_version": True}, {"schema_version": 2}]
        for value in (-1, True, 2.5, None, "-1", "+1", "1e2", "NaN", "Infinity", ".1", "1.", " 1", "1\n",
                      "9" * 79, "0." + "1" * 19):
            bad.append({"schema_version": 1, "standard_amount": value})
        for field in ("view", "detail", "url", "address", "pool_id", "path", "wallet", "charter_id", "headers"):
            bad.append({"schema_version": 1, field: "untrusted"})
        for source in (None, True, 1, [], {}, "", "DEX Screener", "auto\n"):
            bad.append({"schema_version": 1, "source": source})
        for cross_check in (None, 0, 1, [], {}, "true"):
            bad.append({"schema_version": 1, "cross_check": cross_check})
        for config in bad:
            with self.subTest(config=config), self.assertRaises(price.InputError):
                price.price(config, transport=self.provider)
        self.assertEqual(self.provider.requests, [])

    def test_invalid_price_only_removes_its_denomination(self):
        for invalid in (None, 1, 1.5, True, "0", "-1", "+1", "NaN", "Infinity", "1e2", ".2", "1.", "1\n",
                        "9" * 79, "0." + "1" * 37):
            with self.subTest(invalid=invalid):
                self.provider.pair["priceUsd"] = invalid
                result = self.provider.run(standard_amount="4")
                self.assertEqual(result["status"], "partial")
                self.assertEqual(result["values"], {"standard_eth": {"value": "0.00125", "unit": "ETH/STANDARD"}})
                self.assertIn("standard_usd", result["errors"])
                self.assertNotIn("gross_usd", result["valuation"])
                self.assertEqual(result["valuation"]["gross_eth"]["value"], "0.005")

    def test_missing_native_quote_preserves_usd_and_both_missing_fail(self):
        del self.provider.pair["priceNative"]
        result = self.provider.run(standard_amount="2")
        self.assertEqual(result["status"], "partial")
        self.assertEqual(result["valuation"]["gross_usd"]["value"], "5")
        self.assertNotIn("gross_eth", result["valuation"])
        del self.provider.pair["priceUsd"]
        with self.assertRaises(price.PriceError):
            self.provider.run(source="dexscreener")

    def test_identity_spoofs_fail_even_with_valid_prices(self):
        original = copy.deepcopy(self.provider.pair)
        for field, value in (("chainId", "ethereum"), ("dexId", "other"), ("labels", ["v3"]),
                             ("labels", "v4"), ("pairAddress", "0x" + "ab" * 32),
                             ("baseToken", {"address": price.ZERO_ADDRESS}),
                             ("quoteToken", {"address": "0x" + "ab" * 20}),
                             ("baseToken", None), ("quoteToken", [])):
            with self.subTest(field=field, value=value):
                self.provider.body = {"pairs": [dict(original, **{field: value})]}
                with self.assertRaises(price.PriceError):
                    self.provider.run()

    def test_duplicate_matching_pairs_are_ambiguous(self):
        self.provider.body["pairs"].append(copy.deepcopy(self.provider.pair))
        with self.assertRaises(price.PriceError):
            self.provider.run()

    def test_empty_missing_or_legacy_pair_cannot_substitute(self):
        for body in ({}, {"pairs": None}, {"pairs": []}, {"pair": self.provider.pair},
                     {"pairs": [], "pair": self.provider.pair}):
            with self.subTest(body=body), self.assertRaises(price.PriceError):
                self.provider.body = body
                self.provider.run(source="dexscreener")

    def test_irrelevant_pairs_and_provider_timestamps_are_not_evidence(self):
        other = dict(self.provider.pair, pairAddress="0x" + "ab" * 32, irrelevant_secret="unrelated-token")
        self.provider.body["pairs"].append(other)
        self.provider.body["pair"] = other
        self.provider.pair.update(pairCreatedAt=NOW - 100, info={"imageUrl": "https://untrusted.invalid/?timestamp=1"},
                                  url="https://untrusted.invalid/market")
        result = self.provider.run()
        self.assertEqual(result["evidence"]["price_observed_at"], None)
        self.assertEqual(result["evidence"]["price_observation_time_status"], "not_supplied_by_provider")
        self.assertEqual(price.datetime.fromisoformat(result["evidence"]["retrieved_at"].replace("Z", "+00:00")).timestamp(), NOW)
        self.assertNotIn("untrusted", json.dumps(result))
        self.assertNotIn("unrelated-token", json.dumps(result))
        self.assertNotIn("block_number", result["evidence"])

    def test_bad_provider_json_is_fatal_not_partial(self):
        for raw in (b"\xff", b'{"pairs":[],"pairs":[]}', b'{"x":NaN}', b'{"x":1e400}',
                    b'{"x":' + b"9" * 100 + b"}", b"[" * 13 + b"]" * 13,
                    b" " * 65537, b'{"pairs":', "not bytes"):
            transport = Mock(return_value=raw)
            with self.subTest(raw=str(raw)[:40]), self.assertRaises(price.PriceError):
                price.price({"schema_version": 1}, transport=transport)
            transport.assert_called_once()

    def test_transport_exception_does_not_expose_provider_body(self):
        def fail(*args):
            raise OSError("SECRET_RESPONSE_BODY")
        with self.assertRaises(price.PriceError) as raised:
            price.price({"schema_version": 1}, transport=fail)
        self.assertNotIn("SECRET", str(raised.exception))

    def test_late_injected_response_is_not_usable(self):
        clock = iter((0, 0, 0, 11))
        with self.assertRaises(price.PriceError):
            price.price({"schema_version": 1, "source": "dexscreener"}, transport=self.provider, monotonic=lambda: next(clock))

    def test_direct_get_ignores_environment_proxy_and_never_follows_redirect(self):
        for status in (302, 403, 500):
            connection = connection_fixture(status=status)
            with self.subTest(status=status), patch.dict(os.environ, {"HTTPS_PROXY": "http://bad.invalid:1", "HTTP_PROXY": "http://bad.invalid:1"}), \
                    patch.object(price.http.client, "HTTPSConnection", return_value=connection) as factory:
                with self.assertRaises(price.PriceError):
                    price.price({"schema_version": 1, "source": "dexscreener"})
            self.assertEqual(factory.call_args.args, ("api.dexscreener.com",))
            self.assertEqual(connection.request.call_count, 1)
            self.assertEqual(connection.request.call_args.args,
                             ("GET", "/latest/dex/pairs/robinhood/" + self.provider.pair["pairAddress"]))
            connection.getresponse.return_value.read1.assert_not_called()

    def test_http_length_and_body_bounds(self):
        for body, length in ((b"{}", "3"), (b"{}", "1"), (b"{}", "65537"),
                             (b"{}", "-1"), (b"{}", "1e3"), (b"{}", "9" * 100),
                             (b" " * 65537, None)):
            connection = connection_fixture(body, length=length)
            with self.subTest(length=length), self.assertRaises(price.PriceError):
                price._https_request(connection, "dexscreener", "/fixed", 10, lambda: 0)
            connection.close.assert_called_once()

    def test_truncated_chunked_response_is_transport_failure(self):
        connection = connection_fixture()
        connection.getresponse.return_value.read1.side_effect = price.http.client.IncompleteRead(b"SECRET_BODY")
        with self.assertRaises(price.PriceError) as raised:
            price._https_request(connection, "dexscreener", "/fixed", 10, lambda: 0)
        self.assertNotIn("SECRET", str(raised.exception))

    def test_expired_connection_cannot_send(self):
        connection = connection_fixture()
        with self.assertRaises(price.PriceError):
            price._https_request(connection, "dexscreener", "/fixed", 10, lambda: 10)
        connection.request.assert_not_called()

    def test_worker_bounds_stalled_connect_and_denies_late_send(self):
        release, completed = threading.Event(), threading.Event()
        connection = connection_fixture()
        connection.connect.side_effect = lambda: release.wait(2)
        parent = threading.current_thread()
        connection.close.side_effect = lambda: completed.set() if threading.current_thread() is not parent else None
        try:
            with patch.object(price.http.client, "HTTPSConnection", return_value=connection), self.assertRaises(price.PriceError):
                price._https("dexscreener", "/fixed", 0.02, time.monotonic() + 1, time.monotonic)
        finally:
            release.set()
        self.assertTrue(completed.wait(2), "worker did not terminate after resolver released")
        connection.request.assert_not_called()

    def test_worker_bounds_stalled_response_body(self):
        release, completed = threading.Event(), threading.Event()
        connection = connection_fixture()
        connection.getresponse.return_value.read1.side_effect = lambda size: (release.wait(2), b"")[1]
        parent = threading.current_thread()
        connection.close.side_effect = lambda: completed.set() if threading.current_thread() is not parent else None
        try:
            with patch.object(price.http.client, "HTTPSConnection", return_value=connection), self.assertRaises(price.PriceError):
                price._https("dexscreener", "/fixed", 0.02, time.monotonic() + 1, time.monotonic)
        finally:
            release.set()
        self.assertTrue(completed.wait(2), "worker did not terminate after body released")

    def test_auto_success_never_contacts_fallback(self):
        result = self.provider.run()
        self.assertEqual([call[0] for call in self.provider.requests], ["dexscreener"])
        self.assertEqual(result["evidence"]["provider"], "DEX Screener")
        self.assertNotIn("fallback", result)
        self.assertNotIn("cross_check", result)

    def test_availability_fallback_is_labelled_and_marks_only_fallback_quotes(self):
        self.provider.failures["dexscreener"] = TimeoutError("SECRET timeout")
        result = self.provider.run(standard_amount="4")
        self.assertEqual([call[0] for call in self.provider.requests], ["dexscreener", "geckoterminal"])
        self.assertEqual(result["status"], "partial")
        self.assertEqual(result["fallback"]["from"], "DEX Screener")
        self.assertEqual(result["fallback"]["to"], "GeckoTerminal")
        self.assertIn("primary_source", result["errors"])
        self.assertIn("GeckoTerminal fallback", result["note"])
        self.assertEqual(result["evidence"]["source_ids"], ["geckoterminal-api"])
        self.assertEqual(result["valuation"]["gross_usd"]["value"], "12")
        self.assertEqual(result["valuation"]["gross_eth"]["value"], "0.008")
        self.assertNotIn("SECRET", json.dumps(result))

    def test_empty_data_and_absent_quotes_are_available_for_fallback(self):
        missing_quotes = copy.deepcopy(self.provider.pair)
        missing_quotes.pop("priceUsd")
        missing_quotes.pop("priceNative")
        for body in (None, {"pairs": None}, {"pairs": []}, {"pairs": [missing_quotes]}):
            self.provider.body = body
            self.provider.requests.clear()
            result = self.provider.run()
            self.assertEqual(result["evidence"]["provider"], "GeckoTerminal")
            self.assertEqual(len(self.provider.requests), 2)

    def test_identity_schema_invalid_quotes_and_access_never_fall_back(self):
        self.provider.body = {"pairs": [dict(self.provider.pair, chainId="ethereum")]}
        for body in (self.provider.body, {"pairs": "invalid"}, {"pairs": [dict(self.provider.pair, priceUsd="0", priceNative="NaN")]}):
            self.provider.body = body
            self.provider.requests.clear()
            with self.assertRaises(price.PriceError):
                self.provider.run(cross_check=True)
            self.assertEqual([call[0] for call in self.provider.requests], ["dexscreener"])
        self.provider.failures["dexscreener"] = PermissionError("SECRET host restriction")
        self.provider.requests.clear()
        with self.assertRaises(price.PriceError) as raised:
            self.provider.run(cross_check=True)
        self.assertEqual(raised.exception.category, "access")
        self.assertNotIn("SECRET", str(raised.exception))
        self.assertEqual([call[0] for call in self.provider.requests], ["dexscreener"])

    def test_http_status_classification_controls_fallback(self):
        for status in (401, 403, 302, 404, 429, 500, 503):
            first = connection_fixture(status=status)
            second = connection_fixture(json.dumps(self.provider.gt_body).encode())
            eligible = status in (404, 429, 500, 503)
            with self.subTest(status=status), patch.object(price.http.client, "HTTPSConnection", side_effect=[first, second]) as factory:
                if eligible:
                    result = price.price({"schema_version": 1})
                    self.assertEqual(result["evidence"]["provider"], "GeckoTerminal")
                else:
                    with self.assertRaises(price.PriceError):
                        price.price({"schema_version": 1})
                self.assertEqual(factory.call_count, 2 if eligible else 1)
            if eligible:
                self.assertEqual(factory.call_args.args, ("api.geckoterminal.com",))
                self.assertEqual(second.request.call_args.args,
                                 ("GET", "/api/v2/networks/robinhood/pools/" + self.provider.pair["pairAddress"]))
                self.assertEqual(second.request.call_args.kwargs["headers"]["Accept"], "application/json;version=20230203")

    def test_partial_selected_response_never_borrows_other_denomination(self):
        del self.provider.pair["priceNative"]
        result = self.provider.run(standard_amount="2", cross_check=True)
        self.assertEqual(result["evidence"]["provider"], "DEX Screener")
        self.assertNotIn("standard_eth", result["values"])
        self.assertNotIn("gross_eth", result["valuation"])
        self.assertEqual(result["valuation"]["gross_usd"]["value"], "5")
        self.assertIn("standard_eth", result["cross_check"]["values"])
        self.assertNotIn("standard_eth", result["cross_check"]["disagreement_percent"])
        self.assertNotIn("fallback", result)
        self.provider.requests.clear()
        self.provider.run()
        self.assertEqual([call[0] for call in self.provider.requests], ["dexscreener"])

    def test_explicit_geckoterminal_accepts_native_identity_not_display_name(self):
        result = self.provider.run(source="geckoterminal", standard_amount="2")
        self.assertEqual([call[0] for call in self.provider.requests], ["geckoterminal"])
        self.assertEqual(result["values"]["standard_eth"]["value"], "0.002")
        self.assertEqual(result["evidence"]["quote_token_address"], price.ZERO_ADDRESS)
        self.assertEqual(result["valuation"]["gross_eth"]["value"], "0.004")
        self.provider.failures["geckoterminal"] = TimeoutError()
        self.provider.requests.clear()
        with self.assertRaises(price.PriceError):
            self.provider.run(source="geckoterminal")
        self.assertEqual([call[0] for call in self.provider.requests], ["geckoterminal"])

    def test_geckoterminal_rejects_spoofed_pool_and_relationships(self):
        original = copy.deepcopy(self.provider.pool)
        variants = [dict(original, type="token"), dict(original, id="ethereum_" + self.provider.pair["pairAddress"])]
        attributes = copy.deepcopy(original)
        attributes["attributes"]["address"] = "0x" + "ab" * 32
        variants.append(attributes)
        for name, value in (("base_token", "robinhood_" + price.ZERO_ADDRESS),
                            ("quote_token", "robinhood_0x" + "ab" * 20), ("dex", "uniswap-v3-robinhood")):
            pool = copy.deepcopy(original)
            pool["relationships"][name]["data"]["id"] = value
            variants.append(pool)
        for pool in variants:
            self.provider.gt_body = {"data": pool}
            self.provider.requests.clear()
            with self.assertRaises(price.PriceError):
                self.provider.run(source="geckoterminal", cross_check=True)
            self.assertEqual([call[0] for call in self.provider.requests], ["geckoterminal"])

    def test_cross_check_conflicts_never_change_selected_valuation(self):
        result = self.provider.run(standard_amount="4", cross_check=True)
        self.assertEqual(result["valuation"]["gross_usd"]["value"], "10")
        self.assertEqual(result["cross_check"]["provider"], "GeckoTerminal")
        self.assertEqual(result["cross_check"]["disagreement_percent"], {"standard_usd": "20.0000", "standard_eth": "60.0000"})
        self.assertEqual(result["status"], "ok")
        result = self.provider.run(source="geckoterminal", standard_amount="4", cross_check=True)
        self.assertEqual(result["valuation"]["gross_usd"]["value"], "12")
        self.assertEqual(result["cross_check"]["provider"], "DEX Screener")
        self.assertEqual(result["cross_check"]["disagreement_percent"]["standard_usd"], "16.6667")

    def test_failed_cross_check_keeps_primary_quotes_usable(self):
        for failure in (PermissionError("SECRET"), TimeoutError("SECRET"), price.PriceError("SECRET", "identity")):
            self.provider.failures["geckoterminal"] = failure
            result = self.provider.run(standard_amount="4", cross_check=True)
            self.assertEqual(result["status"], "partial")
            self.assertEqual(result["valuation"]["gross_usd"]["value"], "10")
            self.assertEqual(result["cross_check"]["status"], "unavailable")
            self.assertEqual(result["cross_check"]["values"], {})
            self.assertIn("cross_check", result["errors"])
            self.assertNotIn("SECRET", json.dumps(result))

    def test_fallback_cross_check_reuses_failure_with_two_request_limit(self):
        self.provider.failures["dexscreener"] = OSError("SECRET")
        result = self.provider.run(cross_check=True)
        self.assertEqual([call[0] for call in self.provider.requests], ["dexscreener", "geckoterminal"])
        self.assertEqual(result["cross_check"]["provider"], "DEX Screener")
        self.assertEqual(result["cross_check"]["status"], "unavailable")
        self.assertNotIn("SECRET", json.dumps(result))

    def test_each_provider_has_own_retrieval_time_but_no_observation_timestamp(self):
        self.provider.pool["attributes"].update(pool_created_at="2020-01-01T00:00:00Z", last_trade_at=NOW)
        self.provider.pair["pairCreatedAt"] = NOW - 500
        timestamps = iter((NOW, NOW + 2))
        result = price.price({"schema_version": 1, "cross_check": True}, transport=self.provider, now=lambda: next(timestamps))
        for evidence, timestamp in ((result["evidence"], NOW), (result["cross_check"]["evidence"], NOW + 2)):
            self.assertEqual(evidence["price_observed_at"], None)
            self.assertEqual(price.datetime.fromisoformat(evidence["retrieved_at"].replace("Z", "+00:00")).timestamp(), timestamp)

    def test_disagreement_preserves_large_coefficients_and_tiny_denominator(self):
        self.provider.pair["priceUsd"] = "1" + "0" * 40
        self.provider.pool["attributes"]["base_token_price_usd"] = "1" + "0" * 35 + "12345"
        self.provider.pair["priceNative"] = "0." + "0" * 35 + "1"
        self.provider.pool["attributes"]["base_token_price_native_currency"] = "9" * 78
        with price.localcontext() as context:
            context.prec = 6
            result = self.provider.run(cross_check=True)
        self.assertEqual(result["cross_check"]["disagreement_percent"]["standard_usd"], "0.0000")
        expected = str((10 ** 78 - 1) * 10 ** 38 - 100) + ".0000"
        self.assertEqual(result["cross_check"]["disagreement_percent"]["standard_eth"], expected)

    def test_per_request_deadlines_and_total_budget(self):
        ticks = [0]
        def transport(source, path, timeout, deadline, monotonic):
            raw = self.provider(source, path, timeout, deadline, monotonic)
            if source == "dexscreener":
                ticks[0] = 9
            return raw
        price.price({"schema_version": 1, "cross_check": True}, transport=transport, monotonic=lambda: ticks[0])
        self.assertEqual([(call[2], call[3]) for call in self.provider.requests], [(10, 10), (10, 19)])
        self.provider.requests.clear()
        ticks[0] = 0
        def late(source, path, timeout, deadline, monotonic):
            raw = self.provider(source, path, timeout, deadline, monotonic)
            ticks[0] = 15 if source == "dexscreener" else 20
            return raw
        with self.assertRaises(price.PriceError):
            price.price({"schema_version": 1, "cross_check": True}, transport=late, monotonic=lambda: ticks[0])
        self.assertEqual([(call[2], call[3]) for call in self.provider.requests], [(10, 10), (5, 20)])

    def test_cli_explicit_and_cross_check_selections(self):
        code, stdout, stderr = self.cli(b'{"schema_version":1,"source":"geckoterminal","cross_check":true,"standard_amount":"2"}')
        self.assertEqual((code, stderr), (0, ""))
        result = json.loads(stdout)
        self.assertEqual(result["evidence"]["provider"], "GeckoTerminal")
        self.assertEqual(result["cross_check"]["provider"], "DEX Screener")
        self.assertEqual(result["valuation"]["gross_usd"]["value"], "6")
        self.assertEqual([call[0] for call in self.provider.requests], ["geckoterminal", "dexscreener"])

    def test_unsafe_or_invalid_catalog_denied_before_fetch(self):
        catalog = json.loads((ROOT / "assets/entities/robinhood.json").read_text())
        variants = []
        for key, value in (("schema_version", True), ("chain", {"id": 1}), ("records", []),
                           ("market", {"chain_id": 4663, "pool_id": "../other"}),
                           ("market", {"chain_id": True, "pool_id": catalog["market"]["pool_id"]})):
            variants.append(dict(catalog, **{key: value}))
        duplicate = copy.deepcopy(catalog)
        duplicate["records"].append(copy.deepcopy(duplicate["records"][0]))
        variants.append(duplicate)
        duplicate_address = copy.deepcopy(catalog)
        duplicate_address["records"][1]["address"] = duplicate_address["records"][0]["address"]
        variants.append(duplicate_address)
        missing = copy.deepcopy(catalog)
        missing["records"] = [r for r in missing["records"] if r["id"] != "sr-robinhood-standard"]
        variants.append(missing)
        for field, value in (("chain_id", True), ("address", price.ZERO_ADDRESS), ("address", "not-an-address")):
            invalid = copy.deepcopy(catalog)
            invalid["records"][0][field] = value
            variants.append(invalid)
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            (root / "scripts").mkdir()
            helper = root / "scripts/price.py"
            helper.touch()
            (root / "assets/entities").mkdir(parents=True)
            asset = root / "assets/entities/robinhood.json"
            for data in variants:
                asset.write_text(json.dumps(data))
                with self.subTest(data=str(data)[:80]), patch.object(price, "__file__", str(helper)), self.assertRaises(price.PackageDataError):
                    price.price({"schema_version": 1}, transport=self.provider)
        self.assertEqual(self.provider.requests, [])

    def test_catalog_missing_symlink_directory_and_oversize_fail_closed(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            (root / "scripts").mkdir()
            helper = root / "scripts/price.py"
            helper.touch()
            (root / "assets/entities").mkdir(parents=True)
            asset = root / "assets/entities/robinhood.json"
            with patch.object(price, "__file__", str(helper)):
                with self.assertRaises(price.PackageDataError):
                    price.price({"schema_version": 1}, transport=self.provider)
                asset.symlink_to(ROOT / "assets/entities/robinhood.json")
                with self.assertRaises(price.PackageDataError):
                    price.price({"schema_version": 1}, transport=self.provider)
                asset.unlink()
                for raw in (b" " * 65537, b"\xff", b'{"schema_version":1,"schema_version":1}',
                            b'{"schema_version":NaN}', b"[" * 13 + b"]" * 13):
                    asset.write_bytes(raw)
                    with self.subTest(raw=raw[:40]), self.assertRaises(price.PackageDataError):
                        price.price({"schema_version": 1}, transport=self.provider)
                asset.unlink()
                os.mkfifo(asset)
                with self.assertRaises(price.PackageDataError):
                    price.price({"schema_version": 1}, transport=self.provider)
                asset.unlink()
                asset.parent.rmdir()
                asset.parent.symlink_to(ROOT / "assets/entities", target_is_directory=True)
                with self.assertRaises(price.PackageDataError):
                    price.price({"schema_version": 1}, transport=self.provider)
        self.assertEqual(self.provider.requests, [])

    def cli(self, raw, args=(), transport=None):
        incoming = Mock()
        if args:
            incoming.buffer.read.side_effect = AssertionError("explicit CLI read stdin")
        else:
            incoming.buffer = io.BytesIO(raw)
        stdout, stderr = io.StringIO(), io.StringIO()
        with patch.object(price.sys, "argv", ["price.py", *args]), patch.object(price.sys, "stdin", incoming), \
                patch.object(price.sys, "stdout", stdout), patch.object(price.sys, "stderr", stderr), \
                patch.object(price, "_https", transport or self.provider), \
                patch.object(price.time, "time", return_value=NOW), \
                patch.object(price.time, "monotonic", return_value=0):
            code = price.main()
        return code, stdout.getvalue(), stderr.getvalue()

    def test_explicit_cli_matches_json_without_reading_stdin(self):
        cases = [
            (("--quote",), {}),
            (("--source", "geckoterminal"), {"source": "geckoterminal"}),
            (("--cross-check",), {"cross_check": True}),
            (("--amount-standard", "0012.500", "--source", "dexscreener", "--cross-check"),
             {"standard_amount": "0012.500", "source": "dexscreener", "cross_check": True}),
            (("--amount-standard", "0"), {"standard_amount": "0"}),
            (("--amount-standard", "9" * 60 + "." + "9" * 18),
             {"standard_amount": "9" * 60 + "." + "9" * 18}),
        ]
        for args, config in cases:
            with self.subTest(args=args):
                expected = self.cli(json.dumps(dict(schema_version=1, **config)).encode())
                actual = self.cli(b"invalid stdin must be ignored", args=args)
                self.assertEqual(actual[0], 0, actual[2])
                self.assertEqual(actual, expected)

    def test_cli_denials_precede_package_reads_and_transport(self):
        cases = [
            ("--quote", "--amount-standard", "1"), ("--quote", "--quote"),
            ("--cross-check", "--cross-check"), ("--source", "auto", "--source", "auto"),
            ("--amount-standard", "1", "--amount-standard", "2"),
            ("--amount-standard",), ("--source",), ("--source", "other"),
            ("--amount-standard", "-1"), ("--amount-standard", "1e2"),
            ("--amount-standard", "NaN"), ("--amount-standard", "１"),
            ("--amount-standard", "9" * 79), ("--amount-standard", "0." + "1" * 19),
            ("--amount-standard", "1" * 81), ("--amount", "1"), ("--quote=true",),
            ("--cross-check", "false"), ("--help", "--quote"), ("--", "--quote"),
            ("--quote",) * 7,
        ]
        with patch.object(price, "_load_package", side_effect=AssertionError("invalid CLI read package")):
            for args in cases:
                with self.subTest(args=args):
                    code, stdout, stderr = self.cli(b'{"schema_version":1}', args=args)
                    self.assertEqual((code, stdout), (2, ""))
                    self.assertEqual(json.loads(stderr)["error"]["type"], "invalid_input")
        self.assertEqual(self.provider.requests, [])

    def test_cli_structured_errors_and_partial_exit_success(self):
        for raw in (b"\xff", b'{"schema_version":1,"schema_version":1}', b'{"schema_version":NaN}',
                    b" " * 4097, b"[" * 13 + b"]" * 13):
            code, stdout, stderr = self.cli(raw)
            self.assertEqual(code, 2)
            self.assertEqual(stdout, "")
            self.assertEqual(json.loads(stderr)["error"]["type"], "invalid_input")
        self.provider.body = {"pairs": []}
        code, stdout, stderr = self.cli(b'{"schema_version":1,"source":"dexscreener"}')
        self.assertEqual((code, stdout), (5, ""))
        self.assertEqual(json.loads(stderr)["error"]["type"], "price_error")
        self.provider.body = {"pairs": [self.provider.pair]}
        del self.provider.pair["priceNative"]
        code, stdout, stderr = self.cli(b'{"schema_version":1}')
        self.assertEqual((code, stderr), (0, ""))
        self.assertEqual(json.loads(stdout)["status"], "partial")
        with patch.object(price, "_load_package", side_effect=price.PackageDataError("unsafe package")):
            code, stdout, stderr = self.cli(b'{"schema_version":1}')
        self.assertEqual((code, stdout), (4, ""))
        self.assertEqual(json.loads(stderr)["error"]["type"], "package_data_error")

    def test_cli_help_and_extra_arguments_do_not_fetch(self):
        code, stdout, stderr = self.cli(b"", args=("--help",))
        self.assertEqual((code, stderr), (0, ""))
        code, stdout, stderr = self.cli(b'{"schema_version":1}', args=("--url", "https://bad.invalid"))
        self.assertEqual((code, stdout), (2, ""))
        self.assertEqual(json.loads(stderr)["error"]["type"], "invalid_input")
        self.assertEqual(self.provider.requests, [])


if __name__ == "__main__":
    unittest.main()
