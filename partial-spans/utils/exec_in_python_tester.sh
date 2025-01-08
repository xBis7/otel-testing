#!/bin/bash

set -e

source "./lib.sh"

cmd=$1

# TODO: 2nd parameter to check whether to activate the venv or not?
# We need to activate the venv only for python commands.
docker exec -it python-tester bash -c "source /app/venv/bin/activate && $cmd"

