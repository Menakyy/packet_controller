#!/bin/sh
set -e
PROJECT_ROOT="$(dirname "$0")/.."

cd "$PROJECT_ROOT"
python3 -m pylint \
    main.py \
    argument_parser.py \
    logger.py \
    modbus_client.py \
    $@