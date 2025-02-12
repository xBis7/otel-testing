#!/bin/bash

set -e

source "./lib.sh"

abs_path=$1
action=$2
file=${3:-"docker-compose.yml"}

cd "$abs_path"/"$CURRENT_PROJECT"/partial-spans/compose

if [ "$action" == "up" ]; then
  docker compose -f "$file" up -d
elif [ "$action" == "down" ]; then
  docker compose -f "$file" down
elif [ "$action" == "restart_new_imgs" ]; then
  docker compose -f "$file" down
  docker compose build --no-cache
  docker compose -f "$file" up -d
else
  docker compose -f "$file" down
  docker compose -f "$file" up -d
fi

