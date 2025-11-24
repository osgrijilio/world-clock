import datetime
from world_clock.modules import types
from typing import Any


def get_local_timezone() -> types.ZoneRepr:
    "Returns the current local timezone"
    tz = datetime.datetime.now().astimezone().tzinfo
    if tz:
        return types.ZoneRepr(tz)
    else:
        raise ValueError("No local timezone found")


def get_local_time() -> datetime.datetime:
    "Returns the current local time"
    return datetime.datetime.now(get_local_timezone().tzinfo)


def get_utc_time() -> datetime.datetime:
    "Returns time at Zulu TimeZone or GMT-0"
    return datetime.datetime.now(datetime.timezone.utc)


def get_utc_to_localzone_diff() -> datetime.timedelta:
    "Returns the difference between UTC and local timezone"
    x = datetime.datetime.now().astimezone().utcoffset()
    if x:
        return x
    raise ValueError("No local timezone found")


def translate_date_to_tz(dt_str: str, tz_name: str) -> datetime.datetime:
    """
    Receives
      1. dt_str is time expression, based in the local time zone
      2. tz_str is a timezone specification
    Returns the computed datetime object for the given timezone
    Example:
      translate_date_to_tz("2023-01-01 12:00:00", "America/Costa_Rica")
      returns a datetime object for tz
    """
    dt_obj = datetime.datetime.fromisoformat(dt_str)
    if dt_obj.tzinfo is not None:
        dt_obj = dt_obj.replace(tzinfo=None)
    zr_obj = types.from_tz_str_to_ZoneRepr(tz_name)
    return dt_obj.astimezone(zr_obj.tzinfo)


def translate_date_from_tz(dt_str: str, tz_name: str) -> datetime.datetime:
    """
    Receives
      1. dt_str is time expression in tz_str
      2. tz_str is a timezone specification
    Process:
        1. Create a datetime x with timezone tz_str
        2. Return a representation of x in local time zone.
    Example:
      translate_date_from_tz("2023-01-01 12:00:00", "GMT+5")
      returns a datetime object for local time zone.
    """
    dt_obj = datetime.datetime.fromisoformat(dt_str)
    source_zr = types.from_tz_str_to_ZoneRepr(tz_name)
    dt_with_tz = dt_obj.replace(tzinfo=source_zr.tzinfo)
    return dt_with_tz.astimezone(get_local_timezone().tzinfo)


def get_timezones_diff(x: str, y: str) -> float:
    """
    Receives two timezone specifications
    Returns the difference in hours between the two timezones
    """
    zr_x = types.from_tz_str_to_ZoneRepr(x)
    zr_y = types.from_tz_str_to_ZoneRepr(y)
    return float(zr_x.diff(zr_y))

# eof
