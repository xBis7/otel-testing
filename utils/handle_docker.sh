#!/bin/bash

set -e

source "./lib.sh"

abs_path=$1
action=$2

cd "$abs_path"/"$CURRENT_PROJECT"/partial-spans/compose

if [ "$action" == "up" ]; then
  docker compose up -d
elif [ "$action" == "down" ]; then
  docker compose down
elif [ "$action" == "restart_new_imgs" ]; then
  docker compose down
  docker compose build --no-cache
  docker compose up -d
else
  docker compose down
  docker compose up -d
fi

