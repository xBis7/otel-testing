#!/bin/bash

set -e

source "./lib.sh"

abs_path=$1
github_user=$2
github_remote_user=$3   # 'origin' if current user is also the remote user.
arch=${4:-"arm64"}
initial_setup=${5:-"false"}
project=${6:-"core"}

if [ "$project" == "core" ]; then
  # Check if the project exists, clone and checkout to the correct branch if needed.
  cloneProjectIfNotExist "$abs_path" "$OTEL_CORE_PROJECT" "$github_user"
  checkoutToProjectCommit "$abs_path" "$OTEL_CORE_PROJECT" "$github_remote_user" "$OTEL_CORE_COMMIT_SHA"

  cd "$abs_path"/"$OTEL_CORE_PROJECT"
else
  # Check if the project exists, clone and checkout to the correct branch if needed.
  cloneProjectIfNotExist "$abs_path" "$OTEL_CONTRIB_PROJECT" "$github_user"
  checkoutToProjectCommit "$abs_path" "$OTEL_CONTRIB_PROJECT" "$github_remote_user" "$OTEL_CONTRIB_COMMIT_SHA"

  cd "$abs_path"/"$OTEL_CONTRIB_PROJECT"
fi

unset GOROOT

if [ "$initial_setup" == "true" ]; then
  go env -w GOSUMDB=sum.golang.org
  go env -w GOPROXY="https://proxy.golang.org,direct"

  make install-tools
fi

go mod tidy
if [ "$project" == "core" ]; then
  GOOS=linux GOARCH="$arch" make otelcorecol
else
  GOOS=linux GOARCH="$arch" make otelcontribcol
fi

# After the build has finished, the binary is under the project root under the bin dir
# e.g. bin/otelcontribcol_<OS>_<ARCH>

source_bin_name=""
source_bin_path=""

if [ "$project" == "core" ]; then
  source_bin_name="otelcorecol_linux_$arch"
  source_bin_path="$abs_path/$OTEL_CORE_PROJECT/bin/$source_bin_name"
else
  source_bin_name="otelcontribcol_linux_$arch"
  source_bin_path="$abs_path/$OTEL_CONTRIB_PROJECT/bin/$source_bin_name"
fi

# Check if the file exists.
if find "$source_bin_path" -type f | grep -E "/$source_bin_name$"; then
  echo "Otel binary '$source_bin_name' exists. Copying over..."
  # go-binaries might be missing.
  mkdir -p "$abs_path"/"$CURRENT_PROJECT"/partial-spans/compose/go-binaries

  cp "$source_bin_path" "$abs_path"/"$CURRENT_PROJECT"/partial-spans/compose/go-binaries/otel_col_bin
else
  echo "Can't copy the otel binary because it doesn't exist."
fi

