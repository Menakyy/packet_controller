#!/bin/sh
set -e
PROJECT_ROOT="$(dirname "$0")/.."
cd "$PROJECT_ROOT"
python main.py $@
