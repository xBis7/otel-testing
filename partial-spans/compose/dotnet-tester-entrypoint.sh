#!/usr/bin/env bash
set -e

# The local dir structure is
# parent-dir/opentelemetry-dotnet
# parent-dir/otel-testing/partial-spans/OtelDotnetTest

# The container dir structure is
# /app/opentelemetry-dotnet
# /app/testing/partial-spans/OtelDotnetTest

# Working dir is
# /app/testing/partial-spans/

dotnet build OtelTestSolution.sln

exec "$@"
