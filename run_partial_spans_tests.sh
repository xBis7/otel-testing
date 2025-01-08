#!/bin/bash

set -e

source "./lib.sh"

abs_path=$1
setup=$2
github_user=$3
github_remote_user=$4   # 'origin' if current user is also the remote user.
arch=${5:-"arm64"} # If not on Apple Silicon, then this should be 'amd64'.
initial_setup=${6:-"false"}
project=${7:-"core"}

if [ "$setup" == "true" ]; then
  ./partial-spans/utils/setup_env.sh "$abs_path" "$github_user" "$github_remote_user" "$arch" "$initial_setup" "$project"
  ./partial-spans/utils/handle_docker.sh "$abs_path" "restart_new_imgs"

  # Wait for the venv setup to finish.
  # TODO: run the cmd with a repeat counter, instead of a sleep?
  sleep 25
fi

cmd="python test_partial_spans.py"
./partial-spans/utils/exec_in_python_tester.sh "$cmd"
