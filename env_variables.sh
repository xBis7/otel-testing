#!/bin/bash

# Commit SHAs
JAEGER_COMMIT_SHA="e95d120427f033ba336daca4465a84007cfa07af"
OTEL_CORE_COMMIT_SHA="e23802a27ef19cbc8e83e0795b84276272dde18f"
OTEL_CONTRIB_COMMIT_SHA="bc3d400ee110fa5ecef11502b2ba57f5975ba0cf"
OTEL_PYTHON_SDK_COMMIT_SHA="666e27e558fcf8019ef2090f6ef25e7a3f8b4815"
OTEL_DOTNET_SDK_COMMIT_SHA="c824ebdd5f43e954363e703079b24366c0aa324f"
OTEL_JAVA_SDK_COMMIT_SHA="645fc886a2e0bc2933c451cb45b9b26206afcc47"

# Projects
CURRENT_PROJECT="otel-testing"
JENKINS_PROJECT="jenkins"
AIRFLOW_PROJECT="airflow"
JAEGER_PROJECT="jaeger"
OTEL_PLUGIN_PROJECT="opentelemetry-plugin"
OTEL_CORE_PROJECT="opentelemetry-collector"
OTEL_CONTRIB_PROJECT="opentelemetry-collector-contrib"
OTEL_PYTHON_SDK_PROJECT="opentelemetry-python"
OTEL_DOTNET_SDK_PROJECT="opentelemetry-dotnet"
OTEL_JAVA_SDK_PROJECT="opentelemetry-java"

# Hostnames
JENKINS_HOSTNAME="jenkins"
AIRFLOW_WEBSERVER_HOSTNAME="airflow-webserver"
AIRFLOW_WORKER_HOSTNAME="airflow-worker"
AIRFLOW_SCHEDULER_HOSTNAME="airflow-scheduler"
PYTHON_TESTER_HOSTNAME="python-tester"
DOTNET_TESTER_HOSTNAME="dotnet-tester"
JAVA_TESTER_HOSTNAME="java-tester"
