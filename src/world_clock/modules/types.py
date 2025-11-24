"""
We use ZoneRepr to abstract common features of
tzinfo and ZoneInfo, who have similar interfaces, but they aren't the same.
"""

import datetime
import re
from typing import Any
from dataclasses import dataclass, field
from zoneinfo import ZoneInfo, ZoneInfoNotFoundError
from enum import Enum

__all__ = ["ZoneRepr", "from_tz_str_to_ZoneRepr", "valid_timezone_str"]


# Regex to match GMT/UTC offset formats like:
#   GMT
#   GMT+5
#   GMT-11
#   GMT+05
#   GMT+05:30
#   UTC+2, UTC-03:00, etc. (we reuse the same pattern for UTC)
GMT_UTC_OFFSET_RE = re.compile(
    r"^(?P<prefix>GMT|UTC|Z)"  # GMT or UTC
    r"(?P<offset>"  # optional offset part
    r"(?P<sign>[+-])"  # + or -
    r"(?P<hour>(?:[01]?\d|2[0-3]))"  # hour 0-23 (e.g. 5, 05, 23)
    r"(?:\:(?P<minute>[0-5]\d))?"  # optional minutes :00-59
    r")?$"
)


class TimezoneType(Enum):
    ZULU = "zulu"
    GMT_STYLE = "gmt-style"
    ZONEINFO = "zoneinfo"
    NUMERIC = "numeric"
    FAILURE = ""


def valid_timezone_str(tz_str: str) -> tuple[bool, TimezoneType]:
    "Validates if the given timezone is valid"

    if not tz_str:
        return (False, TimezoneType.FAILURE)

    if tz_str.upper() in ["Z", "UTC"]:
        return (True, TimezoneType.ZULU)

    if GMT_UTC_OFFSET_RE.match(tz_str.upper()):
        return (True, TimezoneType.GMT_STYLE)

    try:
        ZoneInfo(tz_str)
        return (True, TimezoneType.ZONEINFO)
    except Exception:
        pass

    try:
        int(tz_str)
        return (True, TimezoneType.NUMERIC)
    except ValueError:
        return (False, TimezoneType.FAILURE)


def extract_tz_from_gmt_style(s: str) -> datetime.tzinfo:
    """
    Supported:
      - GMT, UTC, Z
      - GMT+5, UTC-11, GMT+05
      - GMT+05:30, UTC-03:45
    """
    raw = s
    s = s.strip().upper()

    # 1) GMT/UTC/Z with optional offset
    m = GMT_UTC_OFFSET_RE.match(s)
    if not m:
        raise ValueError(f"Invalid timezone: {raw}")

    offset = m.group("offset")

    # Plain "GMT", "UTC", "Z"
    if offset is None:
        return datetime.timezone.utc

    sign = m.group("sign")
    hour = int(m.group("hour"))
    minute = int(m.group("minute") or 0)

    delta = datetime.timedelta(hours=hour, minutes=minute)
    if sign == "-":
        delta = -delta

    return datetime.timezone(delta, name=raw)


def get_timezone_name(tz: datetime.tzinfo) -> Any:
    if hasattr(tz, "key"):
        return tz.key  # ZoneInfo
    else:
        return tz.tzname(None)  # datetime.timezone


def get_utcoffset_as_float(now: datetime.datetime, tz: datetime.tzinfo) -> float:
    o = tz.utcoffset(now)
    if o is None:
        raise ValueError(f"Unable to determine UTC offset for timezone: {tz.tzname}")
    return o.total_seconds() / 3600


@dataclass(frozen=True, init=False)
class ZoneRepr:
    name: str = field(init=False)
    tzinfo: datetime.tzinfo = field(init=False)

    def __init__(self, tzinfo: datetime.tzinfo):
        object.__setattr__(self, "tzinfo", tzinfo)
        object.__setattr__(self, "name", get_timezone_name(tzinfo))

    def __str__(self) -> str:
        return self.name

    def diff(self, x: ZoneRepr) -> float:
        """Returns difference in hours between two timezones using UTC offsets"""
        now = datetime.datetime.now()
        a = get_utcoffset_as_float(now, self.tzinfo)
        b = get_utcoffset_as_float(now, x.tzinfo)
        return a - b


def from_tz_str_to_ZoneRepr(x: str) -> ZoneRepr:
    "Converts the given timezone string into a ZoneRepr object"

    expr_is_valid, type_value = valid_timezone_str(x)

    if not expr_is_valid:
        raise ValueError(f"Invalid timezone: {x}")

    tz: datetime.tzinfo

    if type_value == TimezoneType.ZULU:
        # In a better implementation we would preserve the original string
        # so we could compare against it. Here, we might change it from
        # 'Z' to 'UTC'.
        tz = datetime.timezone.utc
    elif type_value == TimezoneType.GMT_STYLE:
        tz = extract_tz_from_gmt_style(x)
    elif type_value == TimezoneType.NUMERIC:
        try:
            offset_hours = int(x)
            tz = datetime.timezone(datetime.timedelta(hours=offset_hours))
        except ValueError:
            raise ValueError(f"Invalid timezone: {x}")
    else:
        try:
            tz = ZoneInfo(x)
        except (ZoneInfoNotFoundError, ValueError):
            raise ValueError(f"Invalid timezone: {x}")

    return ZoneRepr(tz)
