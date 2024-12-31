#!/bin/bash

set -e

source "./lib.sh"

abs_path=$1
github_user=${2:-"-"}
github_remote_user=${3:-"-"}  # 'origin' if current user is also the remote user.
arch=${4:-"arm64"}
initial_setup=${5:-"false"}
project=${6:-"core"}

# The 'tester' container is installing the otel sdk from the opentelemetry-python source code.
# It needs to be locally installed.
if [[ "$github_user" != "-" && "$github_remote_user" != "-" ]]; then
  cloneProjectIfNotExist "$abs_path" "$OTEL_PYTHON_SDK_PROJECT" "$github_user"
  checkoutToProjectCommit "$abs_path" "$OTEL_PYTHON_SDK_PROJECT" "$github_remote_user" "$OTEL_PYTHON_SDK_COMMIT_SHA"
fi

# Restore the working dir.
cd "$abs_path"/"$CURRENT_PROJECT"

# The scripts that refresh the binaries, check if each project is available locally and clone it if not.
./partial-spans/utils/refresh_otel_binary.sh "$abs_path" "$github_user" "$github_remote_user" "$arch" "$initial_setup" "$project"
./partial-spans/utils/refresh_jaeger_binary.sh "$abs_path" "$github_user" "$github_remote_user" "$arch" "$initial_setup"
