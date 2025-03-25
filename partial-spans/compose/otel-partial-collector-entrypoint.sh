#!/bin/bash
set -e

migrate -source file:///$(pwd)/internal/postgres/migrations -database "postgres://postgres:test@otel-partial-collector-db:5432/otelpartialcollector?sslmode=disable" up

go run go.opentelemetry.io/collector/cmd/builder@v0.122.1 --config ./example/builder-config.yaml

./bin/otel-partial-collector --config example/config.yaml