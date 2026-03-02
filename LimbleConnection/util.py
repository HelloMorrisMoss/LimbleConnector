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
import logging
import time
from typing import Callable, Any

# Configure standard logger (NFR-001)
logger = logging.getLogger("LimbleConnector")
from pprint import pprint, pformat

import pandas as pd
from pandas import DatetimeTZDtype

# from LimbleConnection.untracked_config.timezones import local_tz
local_tz = None


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
remove_html_pattern = re.compile(r'(\<(\/)?div\>)|(\<(\/)?a\>)|()')  # regex pattern for cleaning errant html tags
new_line_pattern = re.compile(r'(\<(\/)?\s?br\s?(\/)?\>)')

def escape_xlsx_char(ch):
    # thanks to https://www.havnemark.dk/?p=185 for a solution to the openpyxl.utils.exceptions.IllegalCharacterError
    illegal_xlsx_chars = {
        '\x00': '\\x00',  # NULL
        '\x01': '\\x01',  # SOH
        '\x02': '\\x02',  # STX
        '\x03': '\\x03',  # ETX
        '\x04': '\\x04',  # EOT
        '\x05': '\\x05',  # ENQ
        '\x06': '\\x06',  # ACK
        '\x07': '\\x07',  # BELL
        '\x08': '\\x08',  # BS
        '\x0b': '\\x0b',  # VT
        '\x0c': '\\x0c',  # FF
        '\x0e': '\\x0e',  # SO
        '\x0f': '\\x0f',  # SI
        '\x10': '\\x10',  # DLE
        '\x11': '\\x11',  # DC1
        '\x12': '\\x12',  # DC2
        '\x13': '\\x13',  # DC3
        '\x14': '\\x14',  # DC4
        '\x15': '\\x15',  # NAK
        '\x16': '\\x16',  # SYN
        '\x17': '\\x17',  # ETB
        '\x18': '\\x18',  # CAN
        '\x19': '\\x19',  # EM
        '\x1a': '\\x1a',  # SUB
        '\x1b': '\\x1b',  # ESC
        '\x1c': '\\x1c',  # FS
        '\x1d': '\\x1d',  # GS
        '\x1e': '\\x1e',  # RS
        '\x1f': '\\x1f'}  # US

    if ch in illegal_xlsx_chars:
        return illegal_xlsx_chars[ch]

    return ch

# Wraps the function escape_xlsx_char(ch).
def escape_xlsx_string(st):
    escaped_text = ''.join([escape_xlsx_char(ch) for ch in st])
    if escaped_text != st:
        logger.debug(f"Original text: {st}\nescaped text: {escaped_text}")
    return escaped_text

def clean_text(text: str) -> str:
    """Clean lingering html tags from the text."""
    if text is None:
        return ''
    cleaned_txt = escape_xlsx_string(clean_html_from_text(fix_br_newlines(text)).strip(' \t\n'))
    # if cleaned_txt != text:
    #     print(f"Cleaned text: {cleaned_txt}")
    return cleaned_txt


def clean_html_from_text(text: str) -> str:
    """Clean lingering html tags from the text."""
    try:
        fixed_text = remove_html_pattern.sub("", text)
        if fixed_text != text:
            logger.debug(f"Original text: {text}\nCleaned text: {fixed_text}")
        return fixed_text
    except TypeError as te:
        logger.error(f"Error cleaning text: {te}")
        return ""

def fix_br_newlines(text: str) -> str:
    """Replace <br> tags with newlines."""
    return new_line_pattern.sub("\n", text)


def is_string_series(s : pd.Series):
    """Check if a Pandas Series is a string series."""
    # Thanks to https://stackoverflow.com/a/67001213
    if isinstance(s.dtype, pd.StringDtype):
        # The series was explicitly created as a string series (Pandas>=1.0.0)
        return True
    elif s.dtype == 'object':
        # Object series, check each value
        return all((v is None) or isinstance(v, str) for v in s)
    else:
        return False


def clean_column_text(df: pd.DataFrame, columns: list[str] = None, in_place: bool = False) -> pd.DataFrame:
    """Clean lingering html tags from the text from a DataFrame column.

    The Limble web interface will insert html tags like <div>, </ br> in the text of some fields, and that carries over
    to the data returned by the API."""

    if not columns:
        columns = [col for col in df.columns if is_string_series(df[col])]
    logger.info(f'Cleaning these columns: {columns}')
    for col in columns:
        logger.debug(f'Cleaning column {col}')
        if in_place:
            df.loc[:, col] = df.loc[:, col].apply(clean_text)
        else:
            df.loc[:, f'{col}_clean'] = df.loc[:, col].copy().apply(clean_text)
    if not in_place:
        # print([(col, 'is changed?', any(df.loc[:, f'{col}_clean'] != df.loc[:, col])) for col in columns])
        logger.info(f"Changed: {[(col, sum(df.loc[:, f'{col}_clean'] != df.loc[:, col])) for col in columns if any(df.loc[:, f'{col}_clean'] != df.loc[:, col])]}")
    return df


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




class ResilienceHandler:
    """Handles automatic retries for transient errors (NFR-002)."""

    def __init__(self, max_retries: int = 3, backoff_factor: float = 0.5):
        self.max_retries = max_retries
        self.backoff_factor = backoff_factor

    def execute(self, func: Callable[..., Any], *args, **kwargs) -> Any:
        """Executes a function with exponential backoff for 429, 502, 503 errors."""
        retries = 0
        while retries <= self.max_retries:
            try:
                response = func(*args, **kwargs)
                if response.status_code in [429, 502, 503]:
                    if retries == self.max_retries:
                        response.raise_for_status()
                    
                    wait_time = self.backoff_factor * (2 ** retries)
                    if response.status_code == 429:
                        # Try to use X-RateLimit-TTL if available
                        ttl_ms = response.headers.get("X-RateLimit-TTL") or response.headers.get("X-RateLimit-Minute-TTL")
                        if ttl_ms:
                            wait_time = int(ttl_ms) / 1000.0 + 0.1 # Add a small buffer

                    logger.warning(f"Transient error {response.status_code}. Retrying in {wait_time:.2f}s... ({retries+1}/{self.max_retries})")
                    time.sleep(wait_time)
                    retries += 1
                    continue
                return response
            except Exception as e:
                if retries == self.max_retries:
                    raise e
                wait_time = self.backoff_factor * (2 ** retries)
                logger.warning(f"Exception {type(e).__name__} occurred. Retrying in {wait_time:.2f}s... ({retries+1}/{self.max_retries})")
                time.sleep(wait_time)
                retries += 1


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


def localize_dt_columns(df: pd.DataFrame, dt_cols: list[str] = None) -> pd.DataFrame:
    """Convert the specified columns in a DataFrame to local time."""

    if dt_cols is None:
        dt_cols = [col for col in df.columns if isinstance(df[col].dtype, DatetimeTZDtype)]

    # if not dt_cols:
    #     print(f'No datetime columns to be converted.')

    for dt_col in dt_cols:
        holder = df.loc[:, dt_col]
        df.loc[:, dt_col] = None
        df.loc[:, dt_col] = holder.dt.tz_convert(local_tz)
        # df.loc[:, dt_col].apply(lambda t: t.tz is None).all()  # this is a mask
        # df.loc[:, dt_col] = df.loc[:, dt_col].dt.tz_localize(None)
    return df
