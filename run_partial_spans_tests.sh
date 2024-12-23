#!/bin/bash

set -e

source "./lib.sh"

abs_path=$1
setup=$2

if [ "$setup" == "true" ]; then
  ./utils/refresh_otel_binary.sh "$abs_path"
  ./utils/refresh_jaeger_binary.sh "$abs_path"

  ./utils/handle_docker.sh "$abs_path" "restart_new_imgs"

  # Wait for the venv setup to finish.
  sleep 25
fi

cmd="python test_partial_spans.py"
./utils/exec_in_tester.sh "$cmd"
