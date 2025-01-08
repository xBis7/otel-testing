#!/bin/bash

set -e

source "./lib.sh"

cmd=$1

docker exec -it "$DOTNET_TESTER_HOSTNAME" bash -c "$cmd"

