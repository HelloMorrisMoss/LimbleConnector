import json
import os
import pickle
from pprint import pprint, pformat
from typing import Optional, Dict, Any, List, Union
from LimbleConnection import LimbleConnection
from LimbleConnection.util import encode_credentials, logger, logging
from LimbleConnection.endpoint import RegistryLoader, LimbleEndpoint


# any references to `playground` are leftover from the original manual build that was written in a scratch
#  file called playground
class LimbleEndpointChecker:
    """
    Utility for manual/attended testing of Limble API endpoints.
    Aligns with best practices for development testing and supports full lifecycle tests.

    Will go through the registry and test GET endpoints with live requests against the Limble API. Retains results
    from requests that are required for subsequent tests. Ex: `assetID` from assets for querying asset logs.

    Successful tests are saved to a pickle file so that not all endpoints need to be tested if a single endpoint fails.
    """

    def __init__(self, registry_path: str, client_id: str = "client_id", client_secret: str = "client_secret", proxies: Optional[Dict[str, str]] = None):
        """Initializes the playground with Limble connection and registry."""
        self.registry_path = registry_path
        self.encred = encode_credentials(client_id, client_secret)
        self.lc = LimbleConnection(b64_credentials=self.encred, proxies=proxies)

        # Load Registry
        print(f"Loading endpoints from {registry_path}")
        loader = RegistryLoader(registry_path, "")
        self.registry = loader.load()
        self.reg_endpoints = self.registry.get('endpoints', {})
        print(f"Loaded {len(self.reg_endpoints)} registry endpoints")

        # Load Progress
        self.pickle_path = '../../successfully_manually_tested.pickle'
        self.successfully_tested = self._load_progress()
        print(f'Successfully tested {len(self.successfully_tested)}/{len(self.reg_endpoints)} endpoints.')

        # Dependent values tracking (to provide path parameters for subsequent requests)
        self.dependent_values = {
            'routes.locations': {'required_value_name': 'locationID', 'returned_values': []},
            'routes.assets': {'required_value_name': 'assetID', 'returned_values': []},
            'routes.parts': {'required_value_name': 'partID', 'returned_values': []},
            'routes.tasks': {'required_value_name': 'taskID', 'returned_values': []},
            'routes.tasks.instructions': {'required_value_name': 'instructionID', 'returned_values': [],},
            'routes.users': {'required_value_name': 'userID', 'returned_values': []},
            'routes.vendors': {'required_value_name': 'vendorID', 'returned_values': []},
            'routes.purchase_orders': {'required_value_name': 'poID', 'returned_values': []},
            'routes.bills': {'required_value_name': 'billID', 'returned_values': []},
        }

    def _load_progress(self):
        """Loads successfully tested endpoints from pickle file."""
        if os.path.exists(self.pickle_path):
            try:
                with open(self.pickle_path, 'rb') as f:
                    return pickle.load(f)
            except (EOFError, pickle.UnpicklingError):
                return []
        return []

    def save_progress(self):
        """Saves successfully tested endpoints to pickle file."""
        with open(self.pickle_path, 'wb') as f:
            pickle.dump(self.successfully_tested, f)

    def get_endpoint(self, name: str) -> Optional[LimbleEndpoint]:
        """Recursively get the endpoint object from LimbleConnection."""
        name_clean = name.replace('routes.', '')
        endpoint = self.lc
        for name_part in name_clean.split('.'):
            # LimbleConnection dynamically attaches endpoints.
            # Names might be merged if they repeat (e.g. assets.assets -> assets).
            if hasattr(endpoint, name_part):
                endpoint = getattr(endpoint, name_part)
            else:
                # Fallback: check if the connection's internal endpoint dictionary has it
                if hasattr(self.lc, '__endpoints__'):
                    return self.lc.__endpoints__.get(name)
                return None
        return endpoint

    def run_get_tests(self, run_this_many_endpoints_now: int = None):
        """Iterates through registry and tests GET endpoints."""
        count = 0
        # Priority for dependent endpoints to ensure values are available
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
            
            # Skip if already tested and not needed for values
            if is_tested and not is_dependent:
                logger.debug(f"Skipping {name} because it's already been tested and values are not needed.")
                continue

            print(f"\n[GET] Testing: {name}")
            path_params = {}
            query_params = {}

            # Handle path parameters from dependent values
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

            # Special case for batch_task_instructions
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
        """
        Performs a full lifecycle test: Create -> (Confirm) -> Update -> (Confirm) -> Delete -> (Confirm).
        """
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

        # 1. CREATE
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

        # 2. UPDATE
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

        # 3. DELETE
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


def main():
    # Use paths relative to the project root
    registry_path = os.path.join('../../LimbleConnection', 'registry.yaml')
    
    # Initialize playground
    # Change client_id and client_secret if needed
    cid, csecret, proxies = json.loads(input("Enter client_id and client_secret: "))
    playground = LimbleEndpointChecker(registry_path, client_id=cid, client_secret=csecret, proxies=proxies)

    # 1. Run GET tests (Batch)
    print("\n--- Running GET Tests ---")
    test_limit = input("Enter number of GET endpoints to test (default 4): ")
    playground.run_get_tests(run_this_many_endpoints_now=int(test_limit) if test_limit.isdigit() else 4)

    # 2. Prepared Lifecycle Tests
    # These are not run automatically. Uncomment to enable.
    
    # Example Asset Lifecycle Test
    # playground.run_lifecycle_test(
    #     resource_type='asset',
    #     create_payload={'name': 'Playground Test Asset', 'locationID': 1},
    #     update_payload={'name': 'Playground Test Asset UPDATED'}
    # )

    # Example Part Lifecycle Test
    # playground.run_lifecycle_test(
    #     resource_type='part',
    #     create_payload={'name': 'Playground Test Part', 'locationID': 1},
    #     update_payload={'name': 'Playground Test Part UPDATED'}
    # )
    pass

if __name__ == "__main__":
    main()
    pass
