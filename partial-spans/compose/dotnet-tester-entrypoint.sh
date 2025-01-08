#!/usr/bin/env bash
set -e

dotnet build
dotnet restore

exec "$@"
