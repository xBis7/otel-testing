#!/bin/bash

set -e


cd demo

mvn clean install -DskipTests

env \
OTEL_SERVICE_NAME=dice-server \
OTEL_TRACES_EXPORTER=logging \
OTEL_METRICS_EXPORTER=logging \
OTEL_LOGS_EXPORTER=logging \
OTEL_METRIC_EXPORT_INTERVAL=15000

export OTEL_METRICS_EXPORTER=none


java -jar ./target/demo-0.0.1-SNAPSHOT.jar

curl "http://localhost:8081/rolldice?rolls=12"
