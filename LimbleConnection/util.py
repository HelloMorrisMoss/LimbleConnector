"""Utilities used by or useful for the LimbleConnections.

encode_credentials: a function that accepts the client id and client secret from your Limble API and returns the
    base64 encoded credentials needed to authenticate your connection with the Limble API. Check the bottom of the
    settings page as a superuser to get/find your id and secret.
task_type_dict: a dictionary of Limble task type integer keys and human-readable string values.
task_status_dict: a dictionary of Limble task status integer keys and human-readable string values.

"""
from __future__ import annotations

import base64
import datetime
import math
import re
import time
from pprint import pprint, pformat

import pandas as pd


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
div_pattern = re.compile(r'(\<(\/)?div\>)')  # regex pattern for cleaning errant <div> tags from user strings


def convert_timestamp_to_datetime(timestamp: int, timezone) -> datetime.datetime:
    """Convert a Unix/Epoch timestamp to a datetime object *specifically* in the same way as the DataFrame columns."""
    return pd.to_datetime(timestamp, unit='s', origin='unix', utc=True).tz_convert(timezone)


class RateLimit:
    __slots__ = ('_limit', '_remaining', '_first_call', '_ttl', 'limit', 'remaining', 'first_call', 'ttl', 'ttls')
    def __init__(self, limit, remaining, first_call, ttl, timezone):
        self._limit = limit
        self._remaining = remaining
        self._first_call = first_call
        self._ttl = ttl
        # todo: at least for more expensive conversions, only do if they are requested and cache them
        self.limit = int(limit) if limit is not None else None
        self.remaining = int(remaining) if remaining is not None else None
        self.first_call =  convert_timestamp_to_datetime(int(first_call), timezone) if first_call is not None else None
        self.ttl = int(ttl) if ttl is not None else 0 # ms
        self.ttls = math.ceil(self.ttl/1000)

    @property
    def next_live_time(self):
        return datetime.timedelta(seconds=self.ttls) + self.first_call



class RateLimitHandler:
    def __init__(self, response, timezone):
        self.response = response

        # Limble's endpoint rate limit headers
        self._rate_limit_headers = ('X-RateLimit-Limit', 'X-RateLimit-Remaining', 'X-RateLimit-First-Call',
                                    'X-RateLimit-TTL', 'X-RateLimit-Minute-Limit', 'X-RateLimit-Minute-Remaining',
                                    'X-RateLimit-Minute-First-Call', 'X-RateLimit-Minute-TTL')
        self._hour_limit_headers = ('X-RateLimit-Limit', 'X-RateLimit-Remaining', 'X-RateLimit-First-Call',
                                    'X-RateLimit-TTL')
        self._mint_limit_headers = ('X-RateLimit-Minute-Limit', 'X-RateLimit-Minute-Remaining',
                                    'X-RateLimit-Minute-First-Call', 'X-RateLimit-Minute-TTL')
        self._ratelimit_ts_headers = 'X-RateLimit-First-Call', 'X-RateLimit-Minute-First-Call'

        self.hour = RateLimit(*(self.response.headers.get(hdr) for hdr in self._hour_limit_headers), timezone)
        self.minute = RateLimit(*(self.response.headers.get(hdr) for hdr in self._mint_limit_headers), timezone)

    @property
    def ttls(self):
        """The time till live in seconds that the next request is ready, minute or hour. """
        return max(self.hour.ttls, self.minute.ttls)

    @property
    def ttl(self):
        """The time till live in milliseconds that the next request is ready, minute or hour. """
        return max(self.hour.ttl, self.minute.ttl)

    @property
    def next_live_time(self):
        return max(self.hour.next_live_time, self.minute.next_live_time)

    def sleep_till_ready(self, verbose=False):
        """Sleep this thread until the time that the next of this type of request is ready."""
        if verbose:
            print(f'Sleeping for {self.ttl} seconds until next request is ready at {self.next_live_time}.')
        time.sleep(self.ttls)



