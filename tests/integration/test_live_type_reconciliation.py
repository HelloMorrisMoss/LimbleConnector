"""Integration test for the live type reconciliation flow (T024, T032; FR-019, FR-022, FR-023).

The Limble API is mocked — what we're verifying here is that:
  * Observation, classification, and change-set application compose correctly through
    the checker class.
  * `override_type` is preserved across a flag-and-prompt write.
  * `flag-and-skip` mode writes nothing to disk even when discrepancies are found.
  * Discrepancy-kind metadata (drift/nullable/etc.) does NOT leak into the persisted
    registry — only `observed_type` and `empty_response_shape` are written.
"""

from __future__ import annotations

import io
import os
import tempfile
import unittest
from unittest.mock import patch

import yaml

from tests.semiautomated._reconciliation import EndpointChangeSet, classify_field_discrepancy


# A minimal registry seeded with one endpoint whose declared types disagree with what
# the (mocked) live API will return.
_SEED_REGISTRY = {
    "version": "1.0",
    "endpoints": {
        "routes.locations.locations": {
            "method": "GET",
            "url": "{api_base_url}/locations",
            "is_folder": False,
            "query_params": [
                {"key": "limit", "inferred_type": "int", "type": "int"},
            ],
            "response": {
                "fields": {
                    "locationID": {"inferred_type": "int", "type": "int", "origin_type": "int"},
                    "name": {"inferred_type": "str", "type": "str", "origin_type": "str"},
                    # Origin claims str; live data will show nullable.
                    "address": {"inferred_type": "str", "type": "str", "origin_type": "str"},
                    # Wrong origin: claims str, live data is int.
                    "regionID": {
                        "inferred_type": "str",
                        "type": "str",
                        "origin_type": "str",
                        # MUST be preserved across writes (FR-019).
                        "override_type": "Sequence[str]",
                    },
                },
            },
        },
    },
}


# Mocked live response: address is None for some records, regionID is int.
_LIVE_RESPONSE = [
    {"locationID": 78676, "name": "Hydranautics", "address": None, "regionID": 0},
    {"locationID": 78677, "name": "OtherCo", "address": "123 Main", "regionID": 1},
]


def _write_temp_registry(tmpdir):
    path = os.path.join(tmpdir, "registry.yaml")
    with open(path, "w", encoding="utf-8") as f:
        yaml.safe_dump(_SEED_REGISTRY, f, sort_keys=False)
    return path


class TestReconciliationFlow(unittest.TestCase):
    """End-to-end shape: observe → classify → apply → persist."""

    def _make_checker(self, registry_path, mode):
        # We import inside the method to avoid attempting a network connection during
        # module collection (LimbleConnection sets up auth eagerly in some paths).
        from tests.semiautomated.attended_preliminary_testing import LimbleEndpointChecker

        # Bypass the real LimbleConnection setup with a stub that only needs `.registry`.
        with patch("tests.semiautomated.attended_preliminary_testing.LimbleConnection") as MockLC, \
             patch("tests.semiautomated.attended_preliminary_testing.RegistryLoader") as MockLoader:
            MockLC.return_value = object()
            instance = MockLoader.return_value
            with open(registry_path, "r", encoding="utf-8") as f:
                instance.load.return_value = yaml.safe_load(f)

            checker = LimbleEndpointChecker(
                registry_path,
                lc=object(),  # bypass auth
                update_types=True,
                mode=mode,
                pickle_path=os.path.join(os.path.dirname(registry_path), "progress.pickle"),
            )
        return checker

    def test_flag_and_prompt_writes_observed_type_and_preserves_override(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            registry_path = _write_temp_registry(tmpdir)
            checker = self._make_checker(registry_path, mode="flag-and-prompt")

            # Simulate what run_get_tests would do: feed the mocked response in.
            checker._reconcile_response("routes.locations.locations", _LIVE_RESPONSE)

            # User confirms when prompted.
            with patch("builtins.input", return_value="y"):
                checker.finalize_reconciliation()

            with open(registry_path, "r", encoding="utf-8") as f:
                written = yaml.safe_load(f)

            fields = written["endpoints"]["routes.locations.locations"]["response"]["fields"]

            # observed_type written for nullable + drift cases
            self.assertEqual(fields["address"]["observed_type"], "Optional[str]")
            self.assertEqual(fields["regionID"]["observed_type"], "int")
            # No spurious update on agreeing field
            self.assertNotIn("observed_type", fields["name"])
            # FR-019: override_type preserved
            self.assertEqual(fields["regionID"]["override_type"], "Sequence[str]")

    def test_flag_and_skip_writes_nothing(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            registry_path = _write_temp_registry(tmpdir)
            checker = self._make_checker(registry_path, mode="flag-and-skip")
            checker._reconcile_response("routes.locations.locations", _LIVE_RESPONSE)

            # Capture stdout so we can confirm discrepancies are still reported.
            buf = io.StringIO()
            with patch("sys.stdout", buf):
                checker.finalize_reconciliation()

            with open(registry_path, "r", encoding="utf-8") as f:
                written = yaml.safe_load(f)

            # Registry unchanged.
            self.assertEqual(written, _SEED_REGISTRY)
            # But discrepancies were logged.
            out = buf.getvalue()
            self.assertIn("address", out)
            self.assertIn("regionID", out)
            self.assertIn("flag-and-skip", out)

    def test_disabled_update_types_means_no_reconciliation(self):
        """With --update-types off, behavior is byte-identical to the legacy flow (US4 scenario 7)."""
        with tempfile.TemporaryDirectory() as tmpdir:
            registry_path = _write_temp_registry(tmpdir)
            from tests.semiautomated.attended_preliminary_testing import LimbleEndpointChecker

            with patch("tests.semiautomated.attended_preliminary_testing.LimbleConnection"), \
                 patch("tests.semiautomated.attended_preliminary_testing.RegistryLoader") as MockLoader:
                instance = MockLoader.return_value
                with open(registry_path, "r", encoding="utf-8") as f:
                    instance.load.return_value = yaml.safe_load(f)
                checker = LimbleEndpointChecker(
                    registry_path,
                    lc=object(),
                    update_types=False,  # disabled
                    pickle_path=os.path.join(tmpdir, "progress.pickle"),
                )

            checker._reconcile_response("routes.locations.locations", _LIVE_RESPONSE)
            checker.finalize_reconciliation()

            with open(registry_path, "r", encoding="utf-8") as f:
                self.assertEqual(yaml.safe_load(f), _SEED_REGISTRY)

    def test_empty_envelope_records_shape_and_suppresses_field_writes(self):
        """FR-023 capture + FR-022 non-representative-sample suppression."""
        with tempfile.TemporaryDirectory() as tmpdir:
            registry_path = _write_temp_registry(tmpdir)
            checker = self._make_checker(registry_path, mode="flag-and-prompt")

            # Empty envelope from the live API.
            checker._reconcile_response("routes.locations.locations", [])

            with patch("builtins.input", return_value="y"):
                checker.finalize_reconciliation()

            with open(registry_path, "r", encoding="utf-8") as f:
                written = yaml.safe_load(f)

            response = written["endpoints"]["routes.locations.locations"]["response"]
            # FR-023: empty_response_shape captured
            self.assertEqual(response["empty_response_shape"], "[]")
            # Per FR-022: no field-level observed_type writes from a non-representative sample.
            for field_name, field_def in response["fields"].items():
                self.assertNotIn("observed_type", field_def,
                                 f"unexpected observed_type written for {field_name}")


class TestNoMetadataLeak(unittest.TestCase):
    """T032: discrepancy-kind metadata must not leak into the persisted registry."""

    def test_persisted_field_has_no_discrepancy_metadata(self):
        endpoint = {
            "response": {
                "fields": {
                    "address": {"inferred_type": "str", "origin_type": "str"},
                },
            },
        }
        existing = endpoint["response"]["fields"]["address"]
        discrepancy = classify_field_discrepancy(
            "routes.locations.locations", "address", "Optional[str]", existing,
        )
        self.assertIsNotNone(discrepancy)

        # Apply only what the checker would apply.
        from tests.semiautomated._reconciliation import apply_changeset_to_endpoint
        change = EndpointChangeSet(endpoint="routes.locations.locations",
                                   field_updates={"address": "Optional[str]"})
        apply_changeset_to_endpoint(endpoint, change)

        persisted = endpoint["response"]["fields"]["address"]
        # The maintainer-facing classification ("nullability", note, etc.) must NOT
        # appear anywhere in the persisted field — that's a Discrepancy object, kept
        # only in memory for the maintainer report.
        for forbidden_key in ("kind", "note", "discrepancy", "prior_observed_type"):
            self.assertNotIn(forbidden_key, persisted)
        # Only the type label is written.
        self.assertEqual(persisted["observed_type"], "Optional[str]")


if __name__ == "__main__":
    unittest.main()
