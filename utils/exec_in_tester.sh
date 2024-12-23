#!/bin/bash

set -e

source "./lib.sh"

cmd=$1

docker exec -it tester bash -c "source /app/venv/bin/activate && $cmd"

