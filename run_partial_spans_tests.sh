#!/bin/bash

set -e

source "./lib.sh"

abs_path=$1
run_tests_for_sdk_impl=${2:-"all"}
setup=$3
github_user=$4
github_remote_user=$5   # 'origin' if current user is also the remote user.
arch=${6:-"arm64"} # If not on Apple Silicon, then this should be 'amd64'.
initial_setup=${7:-"false"}
collector_project=${8:-"core"}

if [ "$setup" == "true" ]; then
  ./partial-spans/utils/setup_env.sh "$abs_path" "$github_user" "$github_remote_user" "$arch" "$initial_setup" "$collector_project"
  ./partial-spans/utils/handle_docker.sh "$abs_path" "restart_new_imgs"

  # Wait for the venv setup to finish.
  # TODO: run the cmd with a repeat counter, instead of a sleep?
  sleep 35
fi

run_python_tests=0
run_dotnet_tests=0

if [ "$run_tests_for_sdk_impl" == "python" ]; then
  run_python_tests=1
elif [ "$run_tests_for_sdk_impl" == "dotnet" ]; then
  run_dotnet_tests=1
elif [ "$run_tests_for_sdk_impl" == "all" ]; then
  run_python_tests=1
  run_dotnet_tests=1
else
  echo "Value '$run_tests_for_sdk_impl' is invalid. Try one of the following: 'python', 'dotnet', 'all'."
fi

if [ "$run_python_tests" != 0 ]; then
  python_cmd="python test_partial_spans.py"
  ./partial-spans/utils/exec_in_python_tester.sh "$python_cmd"
fi

if [ "$run_dotnet_tests" != 0 ]; then
  dotnet_cmd="dotnet run --project ./OtelDotnetTest"
  ./partial-spans/utils/exec_in_dotnet_tester.sh "$dotnet_cmd"
fi
