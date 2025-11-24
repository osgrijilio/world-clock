#!/usr/bin/env bash

# Stuff you'd have for pipeline builds

pip install pyinstaller

pyinstaller --onefile --name world-clock src/world_clock/cli.py