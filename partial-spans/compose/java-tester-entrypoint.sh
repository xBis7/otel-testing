#!/usr/bin/env bash
set -e

#cd opentelemetry-java

# The working dir is /app
cd otel-java-test

./gradlew clean build

exec "$@"
