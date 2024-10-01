#!/bin/bash

set -e

source "./lib.sh"

abs_path=$1

cd "$abs_path/$AIRFLOW_PROJECT"

docker build . --no-cache -t airflow-sources:latest \
  --build-arg AIRFLOW_INSTALLATION_METHOD="." \
  --build-arg AIRFLOW_SOURCES_FROM="." \
  --build-arg AIRFLOW_SOURCES_TO="/opt/airflow"

cd "$abs_path/$CURRENT_PROJECT"

./utils/docker_restart.sh "true"


