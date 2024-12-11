#!/bin/bash

# Initialize the Airflow database if it hasn't been done yet
airflow db init

# Check if the user already exists; if not, create the user
if ! airflow users list | grep -q "$_AIRFLOW_WWW_USER_USERNAME"; then
    echo "Creating Airflow admin user..."
    airflow users create \
        --username "$_AIRFLOW_WWW_USER_USERNAME" \
        --firstname "$_AIRFLOW_WWW_USER_FIRSTNAME" \
        --lastname "$_AIRFLOW_WWW_USER_LASTNAME" \
        --role "$_AIRFLOW_WWW_USER_ROLE" \
        --email "$_AIRFLOW_WWW_USER_EMAIL" \
        --password "$_AIRFLOW_WWW_USER_PASSWORD"
else
    echo "User $_AIRFLOW_WWW_USER_USERNAME already exists."
fi

# Start the webserver
exec "$@"
