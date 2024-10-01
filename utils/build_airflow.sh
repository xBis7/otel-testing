#!/bin/bash

set -e

source "./lib.sh"

abs_path=$1

cd "$abs_path/airflow"

docker build . --no-cache -t airflow-sources:latest \
  --build-arg AIRFLOW_INSTALLATION_METHOD="." \
  --build-arg AIRFLOW_SOURCES_FROM="." \
  --build-arg AIRFLOW_SOURCES_TO="/opt/airflow" \
  --build-arg AIRFLOW_CONSTRAINTS_REFERENCE="constraints-2-10"

cd "$abs_path/jenkins-otel-testing"

./utils/docker_restart.sh "true"


