#!/usr/bin/env python3
"""Offline, literal ABI known answers; no RPC, crypto dependency or source proof.

Run: python3 maintenance/check-interface.py
Only packaged scripts/catalogs are needed at execution time. Catalogs are decoder
inputs, never encoders for the expected bytes/values, and are loaded without the
production fingerprint gate so a matching fingerprint update cannot hide drift.
These synthetic vectors check selected interfaces, not deployment equivalence,
economic semantics, complete selector recomputation or all malformed boundaries.
"""

import importlib.util
import json
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parent.parent
SPEC = importlib.util.spec_from_file_location("sr_history", ROOT / "scripts/history.py")
history = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(history)
snapshot = history._load_snapshot()

# Provenance below names repository-root maintenance/source-snapshots artifacts;
# they are review citations only, NOT runtime dependencies or generated fixtures.
# v0.2.0-extended-reads/source-provenance.json records the complete publisher
# mountApp-DmwNsaDC.js asset (SHA256 5e7399b7...9cc29bc). Its extracted
# centralBank-abi.json supplies branchCountOf(uint256), queuedEpochDays();
# expansionVault-abi.json supplies holdingsOf(address), reservePool(address).
# signature-hashes.json independently records Ethereum web3_sha3 results:
# branchCountOf(uint256) -> e1b8a032; holdingsOf(address) -> 03995b2d.
# Do not replace these literals with catalog selectors or a production encoder.
BRANCH_CALLDATA = (
    "0xe1b8a032"
    "0000000000000000000000000000000000000000000000010203040506070809"
)
HOLDINGS_CALLDATA = (
    "0x03995b2d"
    "0000000000000000000000001234567890abcdef1234567890abcdef12345678"
)

# Source ABI output order: value:uint256, pending:bool. Distinct values avoid
# the all-one tuple fixture's inability to distinguish reordered fields.
QUEUED_RESULT = (
    "0x000000000000000000000000000000000000000000000000000000000000002a"
    "0000000000000000000000000000000000000000000000000000000000000001"
)
# Source ABI output order: currency0:address, currency1:address, fee:uint24,
# tickSpacing:int24, hooks:address. -60 has full 256-bit sign extension.
POOL_RESULT = (
    "0x0000000000000000000000001234567890abcdef1234567890abcdef12345678"
    "0000000000000000000000002234567890abcdef1234567890abcdef12345678"
    "0000000000000000000000000000000000000000000000000000000000000bb8"
    "ffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffc4"
    "0000000000000000000000003234567890abcdef1234567890abcdef12345678"
)
POOL_EXPECTED = {
    "currency0": "0x1234567890abcdef1234567890abcdef12345678",
    "currency1": "0x2234567890abcdef1234567890abcdef12345678",
    "fee": 3000,
    "tickSpacing": -60,
    "hooks": "0x3234567890abcdef1234567890abcdef12345678",
}

# Auction layouts: v0.2.0-extended-reads/{licenseAuction,charterAuction}-abi.json.
# Topics: v0.2.0-auction-event-review/rpc-evidence.json web3_sha3 request IDs
# 59 (LicensesPurchased(uint256,uint256,uint256,uint256)) and
# 51 (CharterPurchased(uint256,address,uint256,uint256)).
LICENSE_TOPICS = [
    "0x01862d9110233f6709760be3b1cc45660f4b8b0698777de996e5a7d262638fb5",
    "0x0000000000000000000000000000000000000000000000000000000000000011",
    "0x0000000000000000000000000000000000000000000000000000000000000017",
]
LICENSE_DATA = (
    "0x0000000000000000000000000000000000000000000000000000000000000003"
    "00000000000000000000000000000000000000000000000000000000075bcd15"
)
LICENSE_EXPECTED = {"charterId": 17, "day": 23, "count": 3, "unitPrice": 123456789}
CHARTER_TOPICS = [
    "0x1c54748c22f6bf384e0cf9a6a4dfbc630c9ac343ba8a88a5769508bd2da18e50",
    "0x0000000000000000000000000000000000000000000000000000000000000011",
    "0x0000000000000000000000001234567890abcdef1234567890abcdef12345678",
    "0x0000000000000000000000000000000000000000000000000000000000000017",
]
CHARTER_DATA = "0x000000000000000000000000000000000000000000000000000000003ade68b1"

# Contraction layout: v0.2.0-extended-reads/contractionVault-abi.json,
# BuybackExecuted(uint256 ethSpent,uint256 tokensBurned), neither indexed;
# topic independently recorded in that directory's signature-hashes.json.
CONTRACTION_TOPICS = [
    "0x8e8412cac6b961b95ef832e2bac486977bbd29eb9725f9eddd97f3380c31f649",
]
CONTRACTION_DATA = (
    "0x0000000000000000000000000000000000000000000000000de0b6b3a7640000"
    "00000000000000000000000000000000000000000000000000000000075bcd15"
)
# POL layout/topic: protocol-v1.1-review-2026-09-22.json vault_report and
# retained receipt for tx d38d8cad716e65f66babb64f6406d81dab3158cc481401be6dd1f0a8ff7eadae.
# Explorer-decoded BuybackExecuted(uint256 ethIn,uint256 tokensOut,address
# indexed destination), corroborated by raw receipt; not a full authenticated ABI.
# Values below are invented, not a replay or claim about the observed transaction.
POL_TOPICS = [
    "0xb226e46e9ea13f5bbac224e6b365c82beb22fbd42694f7721db493241b3337db",
    "0x0000000000000000000000003234567890abcdef1234567890abcdef12345678",
]
POL_DATA = (
    "0x0000000000000000000000000000000000000000000000001bc16d674ec80000"
    "0000000000000000000000000000000000000000000000000000000100000001"
)


class InterfaceKnownAnswers(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.calls = json.loads((ROOT / "assets/interfaces/robinhood-reads.json").read_text())["calls"]
        cls.events = []
        for filename in ("auction-events.json", "treasury-events.json"):
            cls.events.extend(json.loads((ROOT / "assets/interfaces" / filename).read_text())["events"])

    def call(self, contract, signature):
        return next(c for c in self.calls if c["contract"] == contract and c["signature"] == signature)

    def event(self, role, name):
        return next(e for e in self.events if role in e["contracts"] and e["abi"]["name"] == name)

    def decode_event(self, definition, topics, data):
        # Envelope fields are arbitrary valid scaffolding, not deployment inputs.
        address = "0x4234567890abcdef1234567890abcdef12345678"
        log = {
            "address": address, "blockNumber": "0x64", "transactionIndex": "0x2",
            "logIndex": "0x3", "removed": False,
            "blockHash": "0x1111111111111111111111111111111111111111111111111111111111111111",
            "transactionHash": "0x2222222222222222222222222222222222222222222222222222222222222222",
            "topics": topics, "data": data,
        }
        emitters = {address: {
            "role": "fixture", "entity_id": "fixture",
            "definitions": {definition["topic0"]: definition},
        }}
        return history._decode_log(snapshot, log, emitters, 100, 100)

    def test_calldata_uint256_and_address_known_answers(self):
        self.assertEqual(snapshot._calldata(self.call("centralBank", "branchCountOf(uint256)"),
                                           {"charter_id": 0x010203040506070809}), BRANCH_CALLDATA)
        self.assertEqual(snapshot._calldata(self.call("expansionVault", "holdingsOf(address)"),
                                           {"reserve_asset": "0x1234567890AbCdEf1234567890aBcDeF12345678"}),
                         HOLDINGS_CALLDATA)

    def test_true_boolean_calldata_complements_existing_false_vector(self):
        # check-snapshot.py already pins the false tax word. Reuse that selector,
        # also retained in publisher-read-interface-2026-09-15.json for
        # currentTaxBps(bool); this is not a newly recomputed selector claim.
        buy = next(c for c in self.calls if c["id"] == "buy_tax_percent")
        self.assertEqual(snapshot._calldata(buy, {}),
                         "0xa578d5780000000000000000000000000000000000000000000000000000000000000001")

    def test_scalar_return_preserves_more_than_uint64(self):
        self.assertEqual(snapshot._decode_result(
            "0x0000000000000000000000000000000000000000000000010000000000000001",
            self.call("expansionVault", "holdingsOf(address)")), 18446744073709551617)

    def test_queued_and_pool_return_known_answers(self):
        queued = snapshot._decode_result(QUEUED_RESULT, self.call("centralBank", "queuedEpochDays()"))
        self.assertEqual(queued, {"value": 42, "pending": True})
        self.assertIs(queued["pending"], True)
        self.assertEqual(snapshot._decode_result(POOL_RESULT, self.call("expansionVault", "reservePool(address)")),
                         POOL_EXPECTED)

    def test_auction_indexed_and_nonindexed_known_answers(self):
        license_event = self.decode_event(self.event("licenseAuction", "LicensesPurchased"),
                                          LICENSE_TOPICS, LICENSE_DATA)
        self.assertEqual(license_event["event"], "LicensesPurchased")
        self.assertEqual(license_event["fields"], LICENSE_EXPECTED)
        charter_event = self.decode_event(self.event("charterAuction", "CharterPurchased"),
                                          CHARTER_TOPICS, CHARTER_DATA)
        self.assertEqual(charter_event["event"], "CharterPurchased")
        self.assertEqual(charter_event["fields"], {
            "charterId": 17, "buyer": "0x1234567890abcdef1234567890abcdef12345678",
            "day": 23, "price": 987654321,
        })

    def test_contraction_and_pol_buybacks_have_distinct_known_answers(self):
        contraction = self.decode_event(self.event("contractionVault", "BuybackExecuted"),
                                        CONTRACTION_TOPICS, CONTRACTION_DATA)
        self.assertEqual(contraction["fields"], {"ethSpent": 1000000000000000000, "tokensBurned": 123456789})
        pol = self.decode_event(self.event("polBuyback", "BuybackExecuted"), POL_TOPICS, POL_DATA)
        self.assertEqual(pol["fields"], {
            "ethIn": 2000000000000000000, "tokensOut": 4294967297,
            "destination": "0x3234567890abcdef1234567890abcdef12345678",
        })


if __name__ == "__main__":
    unittest.main()
