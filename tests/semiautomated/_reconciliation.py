"""Registry type reconciliation helpers for `attended_preliminary_testing.py` (FR-022, FR-023).

Pure functions kept out of the script so they can be unit-tested without a live API.

Three concerns live here:
  * Observation — turn a live response into observed types per field.
  * Classification — compare observed types against existing registry values and label
    each discrepancy by kind.
  * Change-set apply — write an approved set of observed_type / empty_response_shape
    updates back into the registry YAML, preserving override_type per FR-019.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional


# ---------------------------------------------------------------------------
# Discrepancy classification
# ---------------------------------------------------------------------------

DOCUMENTATION_DRIFT = "documentation_drift"
NULLABILITY = "nullability"
NON_REPRESENTATIVE_SAMPLE = "non_representative_sample"
PRIOR_OBSERVATION_CONFLICT = "prior_observation_conflict"
OTHER = "other"


@dataclass
class Discrepancy:
    """A single discrepancy between observed and registry-recorded types."""
    endpoint: str
    location: str          # e.g. "response.fields.address" or "query_params.limit"
    field_name: str
    kind: str              # one of the constants above
    observed_type: Optional[str]
    inferred_type: Optional[str] = None
    origin_type: Optional[str] = None
    prior_observed_type: Optional[str] = None
    note: str = ""         # explanation, especially for non_representative_sample


@dataclass
class EndpointChangeSet:
    """The set of proposed changes for one endpoint after observing a live response."""
    endpoint: str
    field_updates: Dict[str, str] = field(default_factory=dict)         # response field -> new observed_type
    param_updates: Dict[str, str] = field(default_factory=dict)         # query param key -> new observed_type
    empty_response_shape: Optional[str] = None                          # FR-023
    discrepancies: List[Discrepancy] = field(default_factory=list)

    @property
    def has_changes(self) -> bool:
        return bool(self.field_updates or self.param_updates or self.empty_response_shape)


# ---------------------------------------------------------------------------
# Type observation
# ---------------------------------------------------------------------------

_SCALAR_TYPE_NAMES = {bool: "bool", int: "int", float: "float", str: "str"}


def python_type_name(value: Any) -> str:
    """Return the conservative Python type label for a non-None value."""
    # bool is a subclass of int — check it first
    if isinstance(value, bool):
        return "bool"
    for ty, name in _SCALAR_TYPE_NAMES.items():
        if type(value) is ty:
            return name
    if isinstance(value, list):
        return "list"
    if isinstance(value, dict):
        return "dict"
    return "Any"


def observe_field_type(samples: List[Any], fallback: Optional[str] = None) -> str:
    """Derive an observed type label from a list of sampled field values (FR-018, FR-022).

    `Optional[X]` is used when any sample is None and at least one non-None sample exists.
    If all samples are None, returns `Optional[fallback or 'Any']`. Mixed non-None types
    yield `Any` (or `Optional[Any]`).
    """
    has_none = any(v is None for v in samples)
    non_none = [v for v in samples if v is not None]

    if not non_none:
        base = fallback or "Any"
        return f"Optional[{base}]" if has_none else base

    base = python_type_name(non_none[0])
    if any(python_type_name(v) != base for v in non_none):
        base = "Any"
    return f"Optional[{base}]" if has_none else base


def observe_response_field_types(records: List[Dict[str, Any]]) -> Dict[str, str]:
    """Walk a list of records and return observed_type per field (FR-022)."""
    if not records:
        return {}
    samples_by_field: Dict[str, List[Any]] = {}
    for record in records:
        if not isinstance(record, dict):
            continue
        for k, v in record.items():
            samples_by_field.setdefault(k, []).append(v)
    return {k: observe_field_type(v) for k, v in samples_by_field.items()}


def detect_empty_response_shape(response: Any) -> Optional[str]:
    """Return a label for the empty-response envelope shape, or None if the response is non-empty (FR-023).

    Only flags genuinely empty envelopes — top-level None, [], {}, or {"data": [], ...}.
    A populated list whose elements happen to contain null fields is NOT an empty response.
    """
    if response is None:
        return "null"
    if isinstance(response, list) and len(response) == 0:
        return "[]"
    if isinstance(response, dict):
        if not response:
            return "{}"
        # Envelope-with-empty-data: e.g. {"data": [], "meta": {...}}
        if "data" in response and isinstance(response["data"], list) and len(response["data"]) == 0:
            keys = sorted(response.keys())
            return "{" + ", ".join(f'"{k}": ...' for k in keys) + '}  # data is []'
    return None


# ---------------------------------------------------------------------------
# Classification
# ---------------------------------------------------------------------------

def classify_field_discrepancy(
    endpoint: str,
    field_name: str,
    observed_type: str,
    existing_field: Dict[str, Any],
    *,
    envelope_is_empty: bool = False,
    location: str = "response.fields",
) -> Optional[Discrepancy]:
    """Compare observed_type against an existing registry field, return Discrepancy or None.

    Precedence of classification (first match wins):
      1. non-representative sample — whole response envelope is empty
      2. prior-observation conflict — existing observed_type disagrees with new one
      3. documentation drift — observed_type disagrees with origin_type
      4. nullability — observed_type is Optional[...] but inferred/origin are not
      5. other — any other mismatch
    """
    inferred = existing_field.get("inferred_type")
    origin = existing_field.get("origin_type")
    prior_observed = existing_field.get("observed_type")

    base = {
        "endpoint": endpoint,
        "location": f"{location}.{field_name}",
        "field_name": field_name,
        "observed_type": observed_type,
        "inferred_type": inferred,
        "origin_type": origin,
        "prior_observed_type": prior_observed,
    }

    if envelope_is_empty:
        return Discrepancy(
            **base,
            kind=NON_REPRESENTATIVE_SAMPLE,
            note="response envelope was empty/sentinel — observed_type may not reflect the true field type",
        )

    if prior_observed and prior_observed != observed_type:
        return Discrepancy(**base, kind=PRIOR_OBSERVATION_CONFLICT,
                           note=f"prior observed_type was {prior_observed}")

    if origin and observed_type != origin:
        # If the only difference is Optional wrapping, classify as nullability.
        if observed_type == f"Optional[{origin}]" or origin == f"Optional[{observed_type}]":
            return Discrepancy(**base, kind=NULLABILITY,
                               note="observed sample includes None; origin_type does not document nullability")
        return Discrepancy(**base, kind=DOCUMENTATION_DRIFT,
                           note="observed_type disagrees with upstream-declared origin_type")

    # No origin: compare against inferred for nullability/other.
    if inferred and observed_type != inferred:
        if observed_type == f"Optional[{inferred}]":
            return Discrepancy(**base, kind=NULLABILITY,
                               note="observed sample includes None; inferred_type does not capture nullability")
        return Discrepancy(**base, kind=OTHER,
                           note="observed_type differs from inferred_type")

    return None


# ---------------------------------------------------------------------------
# Registry change-set apply
# ---------------------------------------------------------------------------

def apply_changeset_to_endpoint(endpoint_entry: Dict[str, Any], change: EndpointChangeSet) -> None:
    """Write a confirmed change-set into an endpoint dict in-place (FR-019, FR-022, FR-023).

    `override_type` MUST NOT be touched. Only `observed_type` (per field/param) and
    `empty_response_shape` (per endpoint) are updated.
    """
    # Response field updates
    if change.field_updates:
        response = endpoint_entry.setdefault("response", {})
        fields = response.setdefault("fields", {})
        for field_name, new_observed in change.field_updates.items():
            existing = fields.setdefault(field_name, {})
            existing["observed_type"] = new_observed

    # Query param updates
    if change.param_updates:
        params = endpoint_entry.setdefault("query_params", [])
        params_by_key = {p.get("key"): p for p in params if isinstance(p, dict)}
        for key, new_observed in change.param_updates.items():
            if key in params_by_key:
                params_by_key[key]["observed_type"] = new_observed
            else:
                params.append({"key": key, "observed_type": new_observed})

    # Empty-response-shape (FR-023)
    if change.empty_response_shape is not None:
        response = endpoint_entry.setdefault("response", {})
        response["empty_response_shape"] = change.empty_response_shape
