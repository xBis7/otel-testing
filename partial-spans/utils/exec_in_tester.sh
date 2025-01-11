#!/bin/bash

set -e

source "./lib.sh"

tester=$1
cmd=$2

if [ "$tester" == "python" ]; then
  # TODO: another parameter to check whether to activate the venv or not?
  # We need to activate the venv only for python commands.
  docker exec -it "$PYTHON_TESTER_HOSTNAME" bash -c "source /app/venv/bin/activate && $cmd"
elif [ "$tester" == "dotnet" ]; then
  docker exec -it "$DOTNET_TESTER_HOSTNAME" bash -c "$cmd"
elif [ "$tester" == "java" ]; then
  docker exec -it "$JAVA_TESTER_HOSTNAME" bash -c "$cmd"
else
  echo "The provided tester '$tester' is invalid. Try one of the following: 'python', 'dotnet' or 'java'."
fi


