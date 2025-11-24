import pytest
import os
from world_clock.modules import types

existing_zones = [
    "UTC",
    "Z",
    "GMT-0",
    "GMT-5",
    "GMT+4",
    "GMT",
    "America/Costa_Rica",
    "Indian/Antananarivo",
    "GMT+05:30",
]

invalid_zones = ["", "XYZ", "GMT-", "CST", "IST"]


@pytest.mark.parametrize("tz_str", existing_zones)
def test_valid_timezone_str(tz_str: str):
    x, _ = types.valid_timezone_str(tz_str)
    assert x == True


@pytest.mark.parametrize("tz_str", invalid_zones)
def test_invalid_timezone_str(tz_str: str):
    x, _ = types.valid_timezone_str(tz_str)
    assert x == False


normalized_zone_names = [
    "UTC",
    "GMT-0",
    "GMT-05:00",
    "GMT+04:00",
    "America/Costa_Rica",
    "Indian/Antananarivo",
    "Asia/Kolkata",
]


# test get_timezone_name by:
# - calling types.from_tz_str_to_ZoneRepr for an x value
# - calling types.ZoneRepr.name and comparing for equality against the x value
# Repeat the test for every value in existing_zones
@pytest.mark.parametrize("tz_str", normalized_zone_names)
def test_get_timezone_name(tz_str: str):
    tz = types.from_tz_str_to_ZoneRepr(tz_str)
    assert types.get_timezone_name(tz.tzinfo) == tz_str


second_round = ["+6", "-3"]


@pytest.mark.parametrize("tz_str", second_round)
def test_get_timezone_name_extra(tz_str: str):
    if os.getenv("INJECT_TEST_ERROR"):
        # pytest.fail("Injected test failure")
        tz = types.from_tz_str_to_ZoneRepr(tz_str)
        assert types.get_timezone_name(tz.tzinfo) == tz_str


def test_gmt_against_utc():
    # Note this test passes, although it goes against common sense.
    tz = types.from_tz_str_to_ZoneRepr("GMT")
    assert types.get_timezone_name(tz.tzinfo) == "UTC"
