import pytest
from world_clock.modules import functions

def test_get_timezones_diff():
    assert functions.get_timezones_diff("America/Costa_Rica", "Asia/Kolkata") == -11.5
    assert functions.get_timezones_diff("Pacific/Rarotonga", "Pacific/Niue") == 1.0
    assert functions.get_timezones_diff("Pacific/Niue", "Pacific/Rarotonga") == -1.0
    assert functions.get_timezones_diff("Pacific/Auckland", "Pacific/Rarotonga") == 23.0