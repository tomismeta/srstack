"""Offline inventory regressions; source-only, without network or execution clients."""
import importlib.util
import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location("srstack_inventory", Path(__file__).with_name("inventory.py"))
INVENTORY = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(INVENTORY)


class InventoryChecks(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.files = {path.relative_to(ROOT).as_posix(): path.read_bytes()
                     for directory in ("assets/interfaces", "assets/entities", "assets/sources")
                     for path in (ROOT / directory).glob("*.json")}

    def document(self, path):
        return json.loads(self.files[path])

    def entry(self, identity, signature):
        document = self.document(f"assets/interfaces/{identity}.json")
        return next(entry for entry in document["entries"] if entry["signature"] == signature)

    def changed(self, path, document):
        return {**self.files, path: json.dumps(document).encode()}

    def test_ethereum_hash_and_nested_tuple_array_signature(self):
        self.assertEqual("a9059cbb", INVENTORY.keccak256(b"transfer(address,uint256)")[:4].hex())
        self.assertEqual("ddf252ad1be2c89b69c2b068fc378daa952ba7f163c4a11628f55a4df523b3ef", INVENTORY.keccak256(b"Transfer(address,address,uint256)").hex())
        entry = {"type": "function", "name": "route", "inputs": [{"type": "tuple[][2]", "components": [
            {"type": "address"}, {"type": "tuple[]", "components": [{"type": "uint"}, {"type": "bytes32"}]}]}]}
        self.assertEqual("route((address,(uint256,bytes32)[])[][2])", INVENTORY.signature(entry))
        for invalid in ("uint7", "bytes33", "uint256[0]", "address garbage"):
            with self.subTest(invalid=invalid), self.assertRaises(ValueError):
                INVENTORY.canonical_type({"type": invalid})

    def test_keccak_rate_boundary_padding(self):
        # Independently obtained with PyCryptodome 3.23.0, not this implementation.
        vectors = {
            135: "cbdfd9dee5faad3818d6b06f95a219fd290b0e1706f6a82e5a595b9ce9faca62",
            136: "7ce759f1ab7f9ce437719970c26b0a66ff11fe3e38e17df89cf5d29c7d7f807e",
            137: "ac73d4fae68b8453f764007c1a20ce95994187861f0c3227a3a8e99a73a3b1db",
        }
        for length, expected in vectors.items():
            with self.subTest(length=length):
                self.assertEqual(INVENTORY.keccak256(bytes(range(length))).hex(), expected)

    def test_nft_transfer_overloads_have_distinct_selectors(self):
        plain = self.entry("charter-nft", "safeTransferFrom(address,address,uint256)")
        data = self.entry("charter-nft", "safeTransferFrom(address,address,uint256,bytes)")
        self.assertEqual("0x42842e0e", plain["selector"])
        self.assertEqual("0xb88d4fde", data["selector"])
        self.assertEqual("bytes", data["abi"]["inputs"][3]["type"])
        self.assertNotEqual(plain["selector"], data["selector"])

    def test_same_transfer_topic_does_not_share_nft_erc20_data_layout(self):
        nft = self.entry("charter-nft", "Transfer(address,address,uint256)")
        token = self.entry("standard", "Transfer(address,address,uint256)")
        self.assertEqual(nft["topic0"], token["topic0"])
        self.assertEqual(4, nft["event_layout"]["topic_count"])
        self.assertEqual(0, nft["event_layout"]["data_parameter_count"])
        self.assertEqual(3, nft["event_layout"]["fields"][2]["topic_index"])
        self.assertEqual(3, token["event_layout"]["topic_count"])
        self.assertEqual(1, token["event_layout"]["data_parameter_count"])
        self.assertEqual(0, token["event_layout"]["fields"][2]["data_parameter_index"])

    def test_purchase_and_checkin_empty_data_boundaries(self):
        license_sale = self.entry("license-auction-v1-2", "LicensesPurchased(uint256,uint256,uint256,uint256)")
        charter_sale = self.entry("charter-auction-v1-2", "CharterPurchased(uint256,address,uint256,uint256)")
        checkin = self.entry("central-bank", "CheckedIn(address)")
        self.assertEqual(["topic", "topic", "data", "data"], [field["location"] for field in license_sale["event_layout"]["fields"]])
        self.assertEqual(["topic", "topic", "topic", "data"], [field["location"] for field in charter_sale["event_layout"]["fields"]])
        self.assertEqual(0, checkin["event_layout"]["data_parameter_count"])
        self.assertEqual(1, checkin["event_layout"]["fields"][0]["topic_index"])

    def test_indexed_dynamic_values_are_hashes_not_decodable_words(self):
        event = {"type": "event", "name": "Record", "anonymous": True, "inputs": [
            {"name": "key", "type": "string", "indexed": True},
            {"name": "values", "type": "tuple[]", "indexed": True, "components": [{"name": "value", "type": "uint256"}]},
            {"name": "payload", "type": "bytes", "indexed": False}]}
        layout = INVENTORY.event_layout(event)
        self.assertEqual(0, layout["fields"][0]["topic_index"])
        self.assertEqual("keccak256_indexed_value", layout["fields"][0]["encoding"])
        self.assertEqual("keccak256_indexed_value", layout["fields"][1]["encoding"])
        self.assertEqual("abi_parameter", layout["fields"][2]["encoding"])
        self.assertEqual(0, layout["fields"][2]["data_parameter_index"])

    def test_incomplete_inventory_cannot_keep_complete_review(self):
        path = "assets/interfaces/charter-nft.json"
        document = self.document(path)
        document["entries"] = [entry for entry in document["entries"] if entry["signature"] != "safeTransferFrom(address,address,uint256,bytes)"]
        with self.assertRaises(ValueError):
            INVENTORY.validate_inventory(self.changed(path, document))
        abis = [entry["abi"] for entry in document["entries"]]
        document["coverage"]["abi_sha256"] = INVENTORY.abi_digest(abis)
        document["coverage"]["entry_counts"] = INVENTORY.entry_counts(abis)
        with self.assertRaises(ValueError):
            INVENTORY.validate_inventory(self.changed(path, document))

    def test_wrong_event_layout_is_rejected_even_with_matching_abi_digest(self):
        path = "assets/interfaces/central-bank.json"
        document = self.document(path)
        event = next(entry for entry in document["entries"] if entry["signature"] == "CheckedIn(address)")
        event["event_layout"]["fields"][0]["location"] = "data"
        with self.assertRaises(ValueError):
            INVENTORY.validate_inventory(self.changed(path, document))

    def test_review_and_contract_reference_closure(self):
        path = "assets/interfaces/standard.json"
        document = self.document(path)
        document["entries"][0]["review_id"] = "missing-review"
        with self.assertRaises(ValueError):
            INVENTORY.validate_inventory(self.changed(path, document))
        path = "assets/entities/contracts.json"
        document = self.document(path)
        fragment = next(binding for binding in document["bindings"] if binding["role"] == "registry")
        fragment["interface_status"] = "complete_publisher_definition"
        with self.assertRaises(ValueError):
            INVENTORY.validate_inventory(self.changed(path, document))

    def test_negative_capability_cannot_use_incomplete_scope_or_existing_function(self):
        path = "assets/interfaces/capabilities.json"
        document = self.document(path)
        negative = next(row for row in document["capabilities"] if row["status"] == "not_exposed")
        negative["interface_ids"] = ["publisher-control-fragment"]
        with self.assertRaises(ValueError):
            INVENTORY.validate_inventory(self.changed(path, document))
        document = self.document(path)
        negative = next(row for row in document["capabilities"] if row["status"] == "not_exposed")
        negative["interface_ids"] = ["license-auction-original"]
        negative["functions"] = []
        negative["absent_signatures"] = ["purchasedOnDay(uint256,uint256)"]
        with self.assertRaises(ValueError):
            INVENTORY.validate_inventory(self.changed(path, document))

    def test_available_capability_requires_observed_function_and_alternative(self):
        path = "assets/interfaces/capabilities.json"
        document = self.document(path)
        available = next(row for row in document["capabilities"] if row["status"] == "available")
        available["functions"] = []
        with self.assertRaises(ValueError):
            INVENTORY.validate_inventory(self.changed(path, document))
        document = self.document(path)
        document["capabilities"][0].pop("alternative_evidence")
        with self.assertRaises(ValueError):
            INVENTORY.validate_inventory(self.changed(path, document))

    def test_adapter_cannot_silently_inherit_removed_original_methods(self):
        path = "assets/interfaces/license-auction-v1-1.json"
        document = self.document(path)
        document["coverage"]["adaptation"]["removed_names"].remove("AUCTION_DAY")
        reviews_path = "assets/interfaces/reviews.json"
        reviews = self.document(reviews_path)
        reviews["reviews"][0]["interfaces"][document["id"]] = document["coverage"]
        changed = self.changed(path, document)
        changed[reviews_path] = json.dumps(reviews).encode()
        with self.assertRaises(ValueError):
            INVENTORY.validate_inventory(changed)

    def test_source_provenance_can_be_direct_artifact_without_html_shell(self):
        path = "assets/interfaces/reviews.json"
        document = self.document(path)
        review = document["reviews"][0]
        review["source_chain"] = [artifact for artifact in review["source_chain"] if artifact["url"].endswith(".js")]
        report = INVENTORY.validate_inventory(self.changed(path, document))
        self.assertEqual(len(review["interfaces"]), report["interfaces"])
        review["source_chain"][0]["sha256"] = "0" * 64
        with self.assertRaises(ValueError):
            INVENTORY.validate_inventory(self.changed(path, document))

    def test_unknown_or_impossible_review_date_cannot_claim_freshness(self):
        reviews_path = "assets/interfaces/reviews.json"
        bindings_path = "assets/entities/contracts.json"
        for invalid in ("unknown", "2026-02-30"):
            with self.subTest(reviewed_at=invalid):
                reviews = self.document(reviews_path)
                review = reviews["reviews"][0]
                review["reviewed_at"] = invalid
                bindings = self.document(bindings_path)
                for binding in bindings["bindings"]:
                    if binding["review_id"] == review["id"]:
                        binding["as_of"] = invalid
                changed = self.changed(reviews_path, reviews)
                changed[bindings_path] = json.dumps(bindings).encode()
                with self.assertRaises(ValueError):
                    INVENTORY.validate_inventory(changed)


if __name__ == "__main__":
    unittest.main()
