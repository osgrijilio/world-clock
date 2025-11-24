# World Clock Usage Examples

## Demo

```bash
python cli.py
python cli.py demo
```

## Current Time

```bash
python cli.py now
python cli.py now --at "America/Costa_Rica"
```

## Time Conversion

```bash
python cli.py from local "2025-01-01 12:00:00" "GMT+1"
python cli.py from "GMT+1" "2025-01-01 12:00:00" local
python cli.py from "GMT+1" "2025-01-01 12:00:00" "America/Costa_Rica"
```

## Timezone Difference

```bash
python cli.py diff "GMT+1" "America/Costa_Rica"
```

## For testing

```bash
PYTHONPATH=src pytest
```

or if you want the pipeline to deal with a test error:

```bash
INJECT_TEST_ERROR=1 PYTHONPATH=src pytest
```

## Strange behavior

If you pass timezone name "GMT", it will be generate timezone "UTC", with name "UTC".
They are comparable, but not the same.

## Stuff for the pipeline

Things run manually that should be part of the pipeline:

```bash
PYTHONPATH=src pytest
mypy --strict --ignore-missing-imports src/world_clock/modules/*.py
mypy --strict --ignore-missing-imports src/world_clock/cli.py
```

Calling the program:

```bash
export PYTHONPATH=src
python src/world_clock/cli.py now --at "GMT+1"
python src/world_clock/cli.py now --at "Pacific/Rarotonga"
python src/world_clock/cli.py from "GMT+2" "2025-11-18 14:34:33" local
python src/world_clock/cli.py from local "2025-11-18 05:34:33" "GMT+2"
python src/world_clock/cli.py from "GMT+1" "2025-01-01 05:00:00" "America/Costa_Rica"
python src/world_clock/cli.py diff 'America/Costa_Rica' 'Asia/Kolkata'
python src/world_clock/cli.py diff 'GMT-5' 'Asia/Kolkata'
python src/world_clock/cli.py diff 'GMT-05:00' 'Asia/Kolkata'
python src/world_clock/cli.py diff "Pacific/Rarotonga" "Pacific/Niue"
python src/world_clock/cli.py diff "Pacific/Niue" "Pacific/Rarotonga"
python src/world_clock/cli.py diff "Pacific/Auckland" "Pacific/Rarotonga"
```

An error looks like this:

```bash
$ python src/world_clock/cli.py now --at "GMT+"
Traceback (most recent call last):
  File "src/py/python-basics/code/world_clock/src/world_clock/cli.py", line 11, in <module>
    actions.report_now_at_timezone_name(args.timezone)
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^
  File "src/py/python-basics/code/world_clock/src/world_clock/modules/actions.py", line 36, in report_now_at_timezone_name
    zr_obj = types.from_tz_str_to_ZoneRepr(tz_name)
  File "src/py/python-basics/code/world_clock/src/world_clock/modules/types.py", line 146, in from_tz_str_to_ZoneRepr
    raise ValueError(f"Invalid timezone: {x}")
ValueError: Invalid timezone: GMT+
```

## Author

Leonel Fonseca.
c(2025).
