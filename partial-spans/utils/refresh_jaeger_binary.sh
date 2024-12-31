#!/bin/bash

set -e

source "./lib.sh"

abs_path=$1
github_user=${2:-"-"}
github_remote_user=${3:-"-"}   # 'origin' if current user is also the remote user.
arch=${4:-"arm64"}
initial_setup=${5:-"false"}

if [[ "$github_user" != "-" && "$github_remote_user" != "-" ]]; then
  # Check if the project exists, clone and checkout to the correct commit SHA if needed.
  cloneProjectIfNotExist "$abs_path" "$JAEGER_PROJECT" "$github_user"
  checkoutToProjectCommit "$abs_path" "$JAEGER_PROJECT" "$github_remote_user" "$JAEGER_COMMIT_SHA"
fi

cd "$abs_path"/"$JAEGER_PROJECT"

if ! git remote -v | grep upstream; then
  echo "Upstream doesn't exist as a remote. Adding it..."
  # make install-tools fetches all tags from upstream.
  # It needs the upstream repo to be available as a remote.
  git remote add upstream https://github.com/jaegertracing/jaeger.git
else
  echo "Upstream exists as a remote."
fi

git submodule update --init --recursive

unset GOROOT

if [ "$initial_setup" == "true" ]; then
  go env -w GOSUMDB=sum.golang.org
  go env -w GOPROXY="https://proxy.golang.org,direct"

  make install-tools
fi

GOOS=linux GOARCH="$arch" make build-all-in-one

source_bin_name="all-in-one-linux-$arch"
source_bin_path="$abs_path/$JAEGER_PROJECT/cmd/all-in-one/$source_bin_name"

# Check if the file exists.
if find "$source_bin_path" -type f | grep -E "/$source_bin_name$"; then
  echo "Jaeger binary '$source_bin_name' exists. Copying over..."
  # go-binaries might be missing.
  mkdir -p "$abs_path"/"$CURRENT_PROJECT"/partial-spans/compose/go-binaries

  cp "$source_bin_path" "$abs_path"/"$CURRENT_PROJECT"/partial-spans/compose/go-binaries/jaeger_bin
else
  echo "Can't copy the jaeger binary because it doesn't exist."
fi

