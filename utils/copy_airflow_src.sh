#!/bin/bash

set -e

source "./lib.sh"

abs_path=$1

docker image rm compose-airflow-init
docker image rm compose-airflow-worker
docker image rm compose-airflow-webserver
docker image rm compose-airflow-scheduler

cp -f -R "$abs_path/$AIRFLOW_PROJECT/." "$abs_path/$CURRENT_PROJECT/compose/airflow_files/airflow_src"
