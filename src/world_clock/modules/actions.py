import datetime

from world_clock.modules import functions
from world_clock.modules import types


def format_utc_offset(offset: datetime.timedelta) -> str:
    """Format timedelta offset as GMT±HH:MM"""
    total_seconds = int(offset.total_seconds())
    hours, remainder = divmod(abs(total_seconds), 3600)
    minutes = remainder // 60
    sign = '+' if total_seconds >= 0 else '-'
    return f"GMT{sign}{hours:02d}:{minutes:02d}"


def report_now_local_time() -> None:
    "Prints the current local time"

    t = functions.get_local_time()
    v = t.strftime("%Y-%m-%d %H:%M:%S %Z")
    zr_obj = functions.get_local_timezone()
    o = format_utc_offset(zr_obj.tzinfo.utcoffset(t))
    print(f"{'Local time:':>27} {v}, offset is {o}")


def report_now_utc_time() -> None:
    "Prints time at Zulu TimeZone or GMT-0"

    t = functions.get_utc_time().strftime("%Y-%m-%d %H:%M:%S %Z")
    print(f"{'UTC time:':>27} {t}")


def report_now_at_timezone_name(tz_name: str) -> None:
    "Prints the current time at the given timezone"

    zr_obj = types.from_tz_str_to_ZoneRepr(tz_name)
    t = datetime.datetime.now(zr_obj.tzinfo)
    v = t.strftime("%Y-%m-%d %H:%M:%S %Z")
    label = f"Time at {tz_name}:"
    o = format_utc_offset(zr_obj.tzinfo.utcoffset(t))
    print(f"{label:>27} {v}, offset is {o}")


def report_now() -> None:
    report_now_local_time()
    report_now_utc_time()


def report_translate_date_to_tz(x: str, tz_str: str) -> None:
    """
    1. dt_str is time expression, based in the local time zone
    2. tz_str is a timezone specification
    prints the corresponding date dt_str in timezone tz_str to d_str
    """
    dt_obj = functions.translate_date_to_tz(x, tz_str)
    v = dt_obj.strftime("%Y-%m-%d %H:%M:%S %Z")
    print(f"Local {x} would be at {tz_str}: {v}")


def report_translate_date_from_tz(dt_str: str, tz_str: str) -> None:
    """
    1. dt_str is time expression, based in the local time zone
    2. tz_str is a timezone specification
    prints the corresponding date dt_str in timezone tz_str
    """
    dt_obj = functions.translate_date_from_tz(dt_str, tz_str)
    v = dt_obj.strftime("%Y-%m-%d %H:%M:%S %Z")
    print(f"Remote {dt_str} {tz_str} would be {v} in local time.")


def report_translate_date_between_tz(
    dt_str: str, source_tz: str, target_tz: str
) -> None:
    """
    Converts time from one timezone to another via local time
    """
    dt_local = functions.translate_date_from_tz(dt_str, source_tz)
    dt_target = functions.translate_date_to_tz(
        dt_local.strftime("%Y-%m-%d %H:%M:%S"), target_tz
    )
    print(
        f"{source_tz} {dt_str} would be {dt_target.strftime('%Y-%m-%d %H:%M:%S %Z')} at {target_tz}"
    )


def report_timezones_diff(x: str, y: str) -> None:
    """
    Receives two timezone specifications
    Prints the difference in hours between the two timezones
    """
    zr_x = types.from_tz_str_to_ZoneRepr(x)
    zr_y = types.from_tz_str_to_ZoneRepr(y)
    diff = functions.get_timezones_diff(x, y)
    label = f"Difference in hours between {zr_x.name} and {zr_y.name}:"
    print(f"{label:>27} {diff}")


def demo() -> None:

    def title(x: str) -> None:
        print(f"\n{x}\n{'=' * len(x)}")

    title("Show current time:")

    report_now()
    report_now_at_timezone_name("GMT+1")
    report_now_at_timezone_name("America/Costa_Rica")

    title("Show corresponding time:")

    report_translate_date_to_tz("2027-12-31 23:30:00", "America/Costa_Rica")
    report_translate_date_from_tz("2028-01-01 00:30:00", "GMT+1")

    title("Timezone differences:")

    report_timezones_diff("GMT+1", "America/Costa_Rica")

    report_timezones_diff("America/Costa_Rica", "America/Costa_Rica")

    report_timezones_diff("GMT-0", "UTC")

    report_timezones_diff("GMT", "UTC")

    print("")


# eof
