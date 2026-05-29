"""Attended preliminary testing of the LimbleConnection registry against the live Limble API.

Two purposes:
  1. Exercise GET endpoints (and prepared lifecycle tests) end-to-end against the live API
     to confirm that registry parameters are accepted and that responses are well-formed.
     This is the original purpose; the y/n prompts remain a deliberate part of the workflow.
  2. (Opt-in, US4/FR-022/FR-023) Observe types from live responses and reconcile them
     against the registry's recorded type fields, writing `observed_type` (per-field) and
     `empty_response_shape` (per-endpoint) when discrepancies are confirmed.

Credentials are read from environment variables; never pass them on the command line
(they would leak into shell history and `ps`). If unset, the script prompts for them
interactively via `getpass`, which does not echo.

  LIMBLE_CLIENT_ID
  LIMBLE_CLIENT_SECRET
  HTTPS_PROXY / HTTP_PROXY  (standard; optional)
"""

from __future__ import annotations

import argparse
import copy
import getpass
import os
import pickle
from pprint import pformat, pprint
from typing import Any, Dict, List, Optional

import yaml

from LimbleConnection import LimbleConnection
from LimbleConnection.endpoint import LimbleEndpoint, RegistryLoader
from LimbleConnection.util import encode_credentials, logger, logging

from tests.semiautomated._reconciliation import (
    DOCUMENTATION_DRIFT,
    EndpointChangeSet,
    NON_REPRESENTATIVE_SAMPLE,
    NULLABILITY,
    OTHER,
    PRIOR_OBSERVATION_CONFLICT,
    apply_changeset_to_endpoint,
    classify_field_discrepancy,
    detect_empty_response_shape,
    observe_response_field_types,
)


MODE_FLAG_AND_PROMPT = "flag-and-prompt"
MODE_FLAG_AND_SKIP = "flag-and-skip"

_KIND_TAG = {
    DOCUMENTATION_DRIFT: "drift",
    NULLABILITY: "nullable",
    NON_REPRESENTATIVE_SAMPLE: "empty-sample",
    PRIOR_OBSERVATION_CONFLICT: "prior-conflict",
    OTHER: "other",
}


def _load_credentials(args_proxy_http: Optional[str], args_proxy_https: Optional[str]) -> Dict[str, Any]:
    """Pull credentials and proxies from env vars, falling back to non-echoing prompts."""
    client_id = os.environ.get("LIMBLE_CLIENT_ID") or input("LIMBLE_CLIENT_ID (not echoed if pasted): ").strip()
    client_secret = (
        os.environ.get("LIMBLE_CLIENT_SECRET")
        or getpass.getpass("LIMBLE_CLIENT_SECRET (input hidden): ")
    )
    proxies = {}
    http_proxy = args_proxy_http or os.environ.get("HTTP_PROXY") or os.environ.get("http_proxy")
    https_proxy = args_proxy_https or os.environ.get("HTTPS_PROXY") or os.environ.get("https_proxy")
    if http_proxy:
        proxies["http"] = http_proxy
    if https_proxy:
        proxies["https"] = https_proxy
    return {"client_id": client_id, "client_secret": client_secret, "proxies": proxies or None}


# any references to `playground` are leftover from the original manual build that was
# written in a scratch file called playground
class LimbleEndpointChecker:
    """Utility for manual/attended testing of Limble API endpoints (US1 testing aid; US4 reconciliation)."""

    def __init__(
        self,
        registry_path: str,
        client_id: str = "client_id",
        client_secret: str = "client_secret",
        proxies: Optional[Dict[str, str]] = None,
        lc: LimbleConnection = None,
        *,
        update_types: bool = False,
        mode: str = MODE_FLAG_AND_PROMPT,
        pickle_path: str = "../../successfully_manually_tested.pickle",
    ):
        logger.level = logging.DEBUG
        self.registry_path = registry_path
        if lc is not None:
            self.lc = lc
        else:
            self.encred = encode_credentials(client_id, client_secret)
            self.lc = LimbleConnection(b64_credentials=self.encred, proxies=proxies)

        print(f"Loading endpoints from {registry_path}")
        loader = RegistryLoader(registry_path, "")
        self.registry = loader.load()
        self.reg_endpoints = self.registry.get('endpoints', {})
        print(f"Loaded {len(self.reg_endpoints)} registry endpoints")

        self.pickle_path = pickle_path
        self.successfully_tested = self._load_progress()
        print(f'Successfully tested {len(self.successfully_tested)}/{len(self.reg_endpoints)} endpoints.')

        # Reconciliation state (US4)
        self.update_types = update_types
        self.mode = mode
        self._changesets: Dict[str, EndpointChangeSet] = {}

        self.dependent_values = {
            'routes.locations': {'required_value_name': 'locationID', 'returned_values': []},
            'routes.assets': {'required_value_name': 'assetID', 'returned_values': []},
            'routes.parts': {'required_value_name': 'partID', 'returned_values': []},
            'routes.tasks': {'required_value_name': 'taskID', 'returned_values': []},
            'routes.tasks.instructions': {'required_value_name': 'instructionID', 'returned_values': []},
            'routes.users': {'required_value_name': 'userID', 'returned_values': []},
            'routes.vendors': {'required_value_name': 'vendorID', 'returned_values': []},
            'routes.purchase_orders': {'required_value_name': 'poID', 'returned_values': []},
            'routes.bills': {'required_value_name': 'billID', 'returned_values': []},
        }

    def _load_progress(self):
        if os.path.exists(self.pickle_path):
            try:
                with open(self.pickle_path, 'rb') as f:
                    return pickle.load(f)
            except (EOFError, pickle.UnpicklingError):
                return []
        return []

    def save_progress(self):
        with open(self.pickle_path, 'wb') as f:
            pickle.dump(self.successfully_tested, f)

    def get_endpoint(self, name: str) -> Optional[LimbleEndpoint]:
        name_clean = name.replace('routes.', '')
        endpoint = self.lc
        for name_part in name_clean.split('.'):
            if hasattr(endpoint, name_part):
                endpoint = getattr(endpoint, name_part)
            else:
                if hasattr(self.lc, '__endpoints__'):
                    return self.lc.__endpoints__.get(name)
                return None
        return endpoint

    # ------------------------------------------------------------------
    # Reconciliation (US4)
    # ------------------------------------------------------------------

    def _reconcile_response(self, endpoint_name: str, response: Any) -> None:
        """Observe types from a live response and accumulate a per-endpoint change-set."""
        if not self.update_types:
            return

        endpoint_config = self.reg_endpoints.get(endpoint_name, {})
        existing_fields = endpoint_config.get("response", {}).get("fields", {})

        envelope_shape = detect_empty_response_shape(response)

        # Normalize the response into a list of records to observe per-field types.
        records: List[Dict[str, Any]]
        if isinstance(response, list):
            records = [r for r in response if isinstance(r, dict)]
        elif isinstance(response, dict):
            records = [response]
        else:
            records = []

        observed_types = observe_response_field_types(records)
        change = self._changesets.setdefault(
            endpoint_name, EndpointChangeSet(endpoint=endpoint_name)
        )

        # Record empty-response shape (FR-023) if observed
        if envelope_shape is not None and not change.empty_response_shape:
            change.empty_response_shape = envelope_shape

        for field_name, observed in observed_types.items():
            existing = existing_fields.get(field_name, {})
            discrepancy = classify_field_discrepancy(
                endpoint_name,
                field_name,
                observed,
                existing,
                envelope_is_empty=(envelope_shape is not None),
            )
            if discrepancy is None:
                continue
            change.discrepancies.append(discrepancy)
            # Only stage a write when the observation is trustworthy (i.e. envelope not empty).
            if discrepancy.kind != NON_REPRESENTATIVE_SAMPLE:
                change.field_updates[field_name] = observed

    def _emit_endpoint_summary(self, change: EndpointChangeSet) -> None:
        """Scannable per-endpoint summary (FR-022, T030)."""
        if not change.discrepancies and change.empty_response_shape is None:
            return

        header = f"\n[{change.endpoint}]"
        if change.empty_response_shape is not None:
            header += f"  empty_response_shape={change.empty_response_shape!r}"
        print(header)

        if not change.discrepancies:
            return

        # Column widths kept compact for scannability — no wall-of-text.
        max_kind = max(len(_KIND_TAG[d.kind]) for d in change.discrepancies)
        max_field = max(len(d.field_name) for d in change.discrepancies)
        for d in change.discrepancies:
            tag = _KIND_TAG[d.kind].ljust(max_kind)
            name = d.field_name.ljust(max_field)
            ref = d.origin_type or d.inferred_type or "(none)"
            print(f"  [{tag}] {name}  ref={ref}  observed={d.observed_type}")
            if d.note:
                print(f"    note: {d.note}")

    def _prompt_endpoint_write(self, change: EndpointChangeSet) -> bool:
        """flag-and-prompt: ask whether to stage this endpoint's writes."""
        if not change.has_changes:
            return False
        ans = input(f"  Stage these {len(change.field_updates)} field update(s) for {change.endpoint}? (y/n): ").strip().lower()
        return ans == 'y'

    def finalize_reconciliation(self) -> None:
        """After all endpoints have been tested, emit summaries and (in flag-and-prompt) write changes."""
        if not self.update_types:
            return

        approved: Dict[str, EndpointChangeSet] = {}
        print("\n=== Type Reconciliation Summary ===")
        for name, change in self._changesets.items():
            self._emit_endpoint_summary(change)
            if self.mode == MODE_FLAG_AND_PROMPT:
                if self._prompt_endpoint_write(change):
                    approved[name] = change

        if self.mode == MODE_FLAG_AND_SKIP:
            print("\n(mode=flag-and-skip — no registry writes)")
            return

        if not approved:
            print("\nNo changes confirmed; registry untouched.")
            return

        self._write_registry(approved)

    def _write_registry(self, approved: Dict[str, EndpointChangeSet]) -> None:
        """Apply confirmed change-sets and persist the registry (FR-019, FR-022, FR-023)."""
        registry_disk = copy.deepcopy(self.registry)
        endpoints = registry_disk.setdefault("endpoints", {})
        for name, change in approved.items():
            entry = endpoints.setdefault(name, {})
            apply_changeset_to_endpoint(entry, change)

        # Single write at the end — avoids partial-write states.
        with open(self.registry_path, "w", encoding="utf-8") as f:
            yaml.safe_dump(registry_disk, f, sort_keys=False)
        print(f"\nWrote {len(approved)} endpoint update(s) to {self.registry_path}.")

    # ------------------------------------------------------------------
    # Live test loop (existing behavior; reconciliation hooks added at the response point)
    # ------------------------------------------------------------------

    def run_get_tests(self, run_this_many_endpoints_now: int = None):
        count = 0
        ordered_names = list(self.dependent_values.keys()) + [k for k in self.reg_endpoints if k not in self.dependent_values]
        run_this_many_endpoints_now = min((run_this_many_endpoints_now or len(ordered_names)), len(ordered_names))
        logger.debug(f'Ordered names to test now {run_this_many_endpoints_now}/{len(ordered_names)}: {pformat(ordered_names[:run_this_many_endpoints_now])}')

        for name in ordered_names:
            if count >= run_this_many_endpoints_now:
                break

            config = self.reg_endpoints.get(name)
            if not config or config.get('is_folder') or config.get('method') != 'GET':
                continue

            is_dependent = name in self.dependent_values
            is_tested = name in self.successfully_tested

            if is_tested and not is_dependent:
                logger.debug(f"Skipping {name} because it's already been tested and values are not needed.")
                continue

            print(f"\n[GET] Testing: {name}")
            path_params = {}
            query_params = {}

            skip_endpoint = False
            for dep_name, dep_info in self.dependent_values.items():
                marker = f":{dep_info['required_value_name']}"
                if marker in config['url']:
                    if dep_info['returned_values']:
                        path_params[dep_info['required_value_name']] = dep_info['returned_values'][0]
                    else:
                        print(f"  Missing required value {marker} from {dep_name}. Skipping.")
                        skip_endpoint = True
                        break

            if skip_endpoint:
                continue

            if name == 'routes.tasks.instructions.batch_task_instructions':
                tasks_dep = self.dependent_values.get('routes.tasks.tasks')
                if tasks_dep and tasks_dep['returned_values']:
                    query_params['tasks'] = str(tasks_dep['returned_values'][0])

            endpoint = self.get_endpoint(name)
            if not endpoint:
                print(f"  Could not find endpoint object for {name}")
                continue

            try:
                # TODO: this *should* ultimately be coming from the Postman Collection - but in any event there needs
                #  to be tracking of where this can be used. right now it's going through 3 retries on a deeper level
                #  also, maybe the retry shouldn't retry on this kind of error
                if endpoint.supports_query_param('limit'):
                    query_params['limit'] = 3
                try:
                    response = endpoint.get(path_params=path_params, query_params=query_params)
                except ConnectionError as e:
                    if ''''message': '`limit` is not allowed''''' in str(e):
                        _ = query_params.pop('limit', None)
                        response = endpoint.get(path_params=path_params, query_params=query_params)

                # Reconciliation hook (US4) — observe types from the live response.
                self._reconcile_response(name, response)

                if is_dependent:
                    val_name = self.dependent_values[name]['required_value_name']
                    self.dependent_values[name]['returned_values'] = [
                        item.get(val_name) for item in response
                        if isinstance(item, dict) and item.get(val_name)
                    ]
                    if name == 'routes.locations.locations':
                        self.lc.location_id = response['locationID']

                if not is_tested:
                    pprint(response)
                    if input(f'  Did this work? (y/n) {name}: ').lower() == 'y':
                        self.successfully_tested.append(name)
                        self.save_progress()
                        print(f'  Progress: {len(self.successfully_tested)} endpoints tested.')
                else:
                    print(f'  Already passed: {name} (values updated)')

                count += 1
            except Exception as e:
                print(f"  Error testing {name}: {e}")

    def run_lifecycle_test(self, resource_type: str, create_payload: dict, update_payload: dict):
        LIFECYCLE_GROUPS = {
            'asset': {
                'create': 'routes.assets.new_asset',
                'update': 'routes.assets.patch_asset',
                'delete': 'routes.assets.delete_asset',
                'id_field': 'assetID',
                'id_param': 'assetID'
            },
            'part': {
                'create': 'routes.parts.create_part',
                'update': 'routes.parts.update_part',
                'delete': 'routes.parts.delete_part',
                'id_field': 'partID',
                'id_param': 'partID'
            }
        }

        if resource_type not in LIFECYCLE_GROUPS:
            print(f"No lifecycle group configured for {resource_type}")
            return

        group = LIFECYCLE_GROUPS[resource_type]
        print(f"\n=== Starting Lifecycle Test: {resource_type.upper()} ===")

        create_ep = self.get_endpoint(group['create'])
        print(f"[STEP 1] CREATE {resource_type} at {group['create']}")
        print(f"  Payload: {create_payload}")
        if input("  Execute Create? (y/n): ").lower() != 'y':
            print("  Lifecycle test aborted.")
            return

        try:
            response = create_ep.create(data=create_payload)
            pprint(response)
            resource_id = response.get(group['id_field']) or response.get('id')
            if not resource_id:
                print("  Error: Creation failed (no ID in response).")
                return
            print(f"  Success! Created resource ID: {resource_id}")
        except Exception as e:
            print(f"  Error during creation: {e}")
            return

        update_ep = self.get_endpoint(group['update'])
        print(f"\n[STEP 2] UPDATE {resource_type} (ID: {resource_id}) at {group['update']}")
        print(f"  Payload: {update_payload}")
        if input("  Execute Update? (y/n): ").lower() == 'y':
            try:
                response = update_ep.update(data=update_payload, path_params={group['id_param']: resource_id})
                pprint(response)
                print(f"  Success! Resource {resource_id} updated.")
            except Exception as e:
                print(f"  Error during update: {e}")
        else:
            print("  Skipped update.")

        delete_ep = self.get_endpoint(group['delete'])
        print(f"\n[STEP 3] DELETE {resource_type} (ID: {resource_id}) at {group['delete']}")
        if input("  Execute Delete? (y/n): ").lower() == 'y':
            try:
                success = delete_ep.delete(path_params={group['id_param']: resource_id})
                if success:
                    print(f"  Success! Resource {resource_id} deleted.")
                else:
                    print(f"  Deletion reported failure.")
            except Exception as e:
                print(f"  Error during deletion: {e}")
        else:
            print(f"  Skipped deletion. Manual cleanup required for ID: {resource_id}")


def _build_argparser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(
        description="Attended live-API testing for the LimbleConnector registry. "
                    "Credentials are read from env (LIMBLE_CLIENT_ID, LIMBLE_CLIENT_SECRET) "
                    "or prompted via getpass — never accepted as CLI args.",
    )
    p.add_argument(
        "--registry-path",
        default=os.path.join("../../LimbleConnection", "registry.yaml"),
        help="Path to registry.yaml (default: ../../LimbleConnection/registry.yaml)",
    )
    p.add_argument(
        "--pickle-path",
        default="../../successfully_manually_tested.pickle",
        help="Path to the progress pickle file (default: ../../successfully_manually_tested.pickle)",
    )
    p.add_argument(
        "--limit",
        type=int,
        default=4,
        help="Number of GET endpoints to test in this run (default: 4)",
    )
    p.add_argument(
        "--update-types",
        action="store_true",
        help="Opt-in: observe types from live responses and reconcile against the registry (FR-022, US4). "
             "Off by default; when off, behavior is identical to the legacy flow.",
    )
    p.add_argument(
        "--mode",
        choices=[MODE_FLAG_AND_PROMPT, MODE_FLAG_AND_SKIP],
        default=MODE_FLAG_AND_PROMPT,
        help="Reconciliation mode (only meaningful with --update-types). "
             "'flag-and-prompt' prompts before each endpoint write; "
             "'flag-and-skip' logs without writing.",
    )
    p.add_argument("--http-proxy", default=None, help="Override HTTP_PROXY env var")
    p.add_argument("--https-proxy", default=None, help="Override HTTPS_PROXY env var")
    p.add_argument(
        "--skip-lifecycle",
        action="store_true",
        help="Skip the prepared lifecycle (CREATE/UPDATE/DELETE) test prompts",
    )
    return p


def main(argv: Optional[List[str]] = None) -> int:
    args = _build_argparser().parse_args(argv)

    creds = _load_credentials(args.http_proxy, args.https_proxy)
    encred = encode_credentials(creds["client_id"], creds["client_secret"])
    lc = LimbleConnection(b64_credentials=encred, proxies=creds["proxies"])

    playground = LimbleEndpointChecker(
        args.registry_path,
        client_id=creds["client_id"],
        client_secret=creds["client_secret"],
        proxies=creds["proxies"],
        lc=lc,
        update_types=args.update_types,
        mode=args.mode,
        pickle_path=args.pickle_path,
    )

    print("\n--- Running GET Tests ---")
    playground.run_get_tests(run_this_many_endpoints_now=args.limit)

    if not args.skip_lifecycle:
        try:
            playground_location_id = playground.dependent_values.get('routes.locations')['returned_values'][0]
        except (IndexError, KeyError, TypeError):
            playground_location_id = None

        if playground_location_id is not None:
            if input("Run prepared lifecycle tests on ASSETS? (y/n): ").lower() == 'y':
                playground.run_lifecycle_test(
                    resource_type='asset',
                    create_payload={'name': 'Playground Test Asset', 'locationID': playground_location_id},
                    update_payload={'name': 'Playground Test Asset UPDATED'}
                )
            if input("Run prepared lifecycle tests on PARTS? (y/n): ").lower() == 'y':
                playground.run_lifecycle_test(
                    resource_type='part',
                    create_payload={'name': 'Playground Test Part', 'locationID': playground_location_id},
                    update_payload={'name': 'Playground Test Part UPDATED', 'locationID': playground_location_id}
                )

    # Emit summary and (if flag-and-prompt) write confirmed changes.
    playground.finalize_reconciliation()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
