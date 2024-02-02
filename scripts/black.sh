#!/bin/sh
set -e
PROJECT_ROOT="$(dirname "$0")/.."

cd "$PROJECT_ROOT"
if [ $# -ge 1 ] ; then
    if [ "$1" != "--check" ] ; then
        echo "Invalid arguments"
        exit 1
    fi
    FLAGS="--check"
else
    FLAGS=""
fi
python3 -m black $FLAGS main.py argument_parser.py logger.py modbus_client.py
