"""Utilities used by or useful for the LimbleConnections.

encode_credentials: a function that accepts the client id and client secret from your Limble API and returns the
    base64 encoded credentials needed to authenticate your connection with the Limble API. Check the bottom of the
    settings page as a superuser to get/find your id and secret.
task_type_dict: a dictionary of Limble task type integer keys and human-readable string values.
task_status_dict: a dictionary of Limble task status integer keys and human-readable string values.

"""
from __future__ import annotations

import base64
import re


def encode_credentials(client_id: str, client_secret: str) -> str:
    """Turn client_id and client_secret into a base64 encoded string."""
    return base64.b64encode(f'{client_id}:{client_secret}'.encode('utf-8')).decode('utf-8')

task_type_dict = {
    1: "Preventative Maintenance (PM)",
    2: "Unplanned Work Order (WO)",
    # there does not seem to be a type 3
    4: "Planned Work Order (WO)",
    5: "Cycle Count",
    6: "Work Request (WR)",
    7: "Min Part Threshold",
    8: "Materials Request",
}

task_status_dict = {
    0: 'Open',
    1: 'Complete'
}
div_pattern = re.compile(r'(\<(\/)?div\>)')
