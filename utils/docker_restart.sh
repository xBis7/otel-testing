#!/bin/bash

set -e

source "./lib.sh"

new_images=$1

cd compose

docker compose down

if [ "$new_images" == "true" ]; then
  docker compose build --no-cache
fi

docker compose up -d


