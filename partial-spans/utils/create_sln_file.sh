#!/bin/bash

set -e

source "./lib.sh"

abs_path=$1
sln_name=$2

cd "$abs_path"/"$CURRENT_PROJECT"/partial-spans

dotnet new sln -n "$sln_name"

dotnet sln "$sln_name".sln add ./OtelDotnetTest/OtelDotnetTest.csproj
dotnet sln "$sln_name".sln add ../../opentelemetry-dotnet/src/OpenTelemetry/OpenTelemetry.csproj
dotnet sln "$sln_name".sln add ../../opentelemetry-dotnet/src/OpenTelemetry.Exporter.Console/OpenTelemetry.Exporter.Console.csproj
dotnet sln "$sln_name".sln add ../../opentelemetry-dotnet/src/OpenTelemetry.Exporter.OpenTelemetryProtocol/OpenTelemetry.Exporter.OpenTelemetryProtocol.csproj



