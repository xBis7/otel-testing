#!/usr/bin/env bash
set -e

dotnet new sln -n OtelSetupSolution

dotnet sln OtelSetupSolution.sln add ./OtelDotnetTest/OtelDotnetTest.csproj
dotnet sln OtelSetupSolution.sln add ./opentelemetry-dotnet/src/OpenTelemetry/OpenTelemetry.csproj
dotnet sln OtelSetupSolution.sln add ./opentelemetry-dotnet/src/OpenTelemetry.Exporter.Console/OpenTelemetry.Exporter.Console.csproj
dotnet sln OtelSetupSolution.sln add ./opentelemetry-dotnet/src/OpenTelemetry.Exporter.OpenTelemetryProtocol/OpenTelemetry.Exporter.OpenTelemetryProtocol.csproj

dotnet build OtelSetupSolution.sln

exec "$@"
