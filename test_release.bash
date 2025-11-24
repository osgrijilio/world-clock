#!/usr/bin/env bash

# Stuff you'd put on a pipeline test

set -e

./dist/world-clock now --at "GMT+1"
./dist/world-clock now --at "Pacific/Rarotonga"
./dist/world-clock from "GMT+2" "2025-11-18 14:34:33" local
./dist/world-clock from local "2025-11-18 05:34:33" "GMT+2"
./dist/world-clock from "GMT+1" "2025-01-01 05:00:00" "America/Costa_Rica"
./dist/world-clock diff 'America/Costa_Rica' 'Asia/Kolkata'
./dist/world-clock diff 'GMT-5' 'Asia/Kolkata'
./dist/world-clock diff 'GMT-05:00' 'Asia/Kolkata'
./dist/world-clock diff "Pacific/Rarotonga" "Pacific/Niue"
./dist/world-clock diff "Pacific/Niue" "Pacific/Rarotonga"
./dist/world-clock diff "Pacific/Auckland" "Pacific/Rarotonga"
