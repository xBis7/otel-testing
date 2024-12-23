#!/bin/bash

set -e

source "./lib.sh"

abs_path=$1

# Remove the airflow dir.
docker exec -it -u root "$AIRFLOW_WEBSERVER_HOSTNAME" rm -rf /opt/airflow/airflow
docker exec -it -u root "$AIRFLOW_WORKER_HOSTNAME" rm -rf /opt/airflow/airflow
docker exec -it -u root "$AIRFLOW_SCHEDULER_HOSTNAME" rm -rf /opt/airflow/airflow

# Copy the local dir.
docker cp $abs_path/$AIRFLOW_PROJECT/airflow "$AIRFLOW_WEBSERVER_HOSTNAME":/opt/airflow
docker cp $abs_path/$AIRFLOW_PROJECT/airflow "$AIRFLOW_WORKER_HOSTNAME":/opt/airflow
docker cp $abs_path/$AIRFLOW_PROJECT/airflow "$AIRFLOW_SCHEDULER_HOSTNAME":/opt/airflow

# Commit the new image.
docker commit "$AIRFLOW_WEBSERVER_HOSTNAME" airflow-sources:latest
docker commit "$AIRFLOW_WORKER_HOSTNAME" airflow-sources:latest
docker commit "$AIRFLOW_SCHEDULER_HOSTNAME" airflow-sources:latest

docker commit "$AIRFLOW_WEBSERVER_HOSTNAME" compose-airflow-webserver
docker commit "$AIRFLOW_WORKER_HOSTNAME" compose-airflow-worker
docker commit "$AIRFLOW_SCHEDULER_HOSTNAME" compose-airflow-scheduler

# cd "$abs_path/$CURRENT_PROJECT"

# ./utils/docker_restart.sh
