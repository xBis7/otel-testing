using Microsoft.Extensions.Logging;
using System.Diagnostics;
using OpenTelemetry;
using OpenTelemetry.Exporter;
using OpenTelemetry.Resources;
using OpenTelemetry.Trace;
using OtelPartialSpanLib;

using OpenTelemetry.Logs;
using OpenTelemetry.Exporter.OpenTelemetryProtocol;
//using OpenTelemetry.Exporter.PartialActivity;
//using OpenTelemetry.Exporter.PartialActivity.Processor;

namespace OtelDotnetTest;

public class TestLogsToPartialSpans
{

    internal static readonly ActivitySource SActivitySource = new(Program.ServiceName);

    public void ExecuteWithConsoleExporter()
    {
        using var tracerProvider = Sdk.CreateTracerProviderBuilder()
            .AddSource(Program.ServiceName)
            .SetResourceBuilder(
                ResourceBuilder.CreateDefault()
                    .AddService(serviceName: Program.ServiceName, serviceVersion: Program.ServiceVersion))
            .AddConsoleExporter()
            .Build();

        Console.WriteLine("===============> Hello, World!");

        const string rootName = "activity-root-span";
        using var activity = SActivitySource.StartActivity(rootName);
        Console.WriteLine("===============> Activity root-span");

        /* for loop execution */
        for (var a = 0; a < 3; a += 1) {
            var n = $"activity-sub-span-{a}";
            using var subActivity = SActivitySource.StartActivity(n);
            Console.WriteLine($"===============> iteration: {a}");
        }

    }

    public void ExecuteWithOtlpExporter(bool useStandalone)
    {
        if (useStandalone) {
            useStandaloneProcessor();
        } else {
            usePartialProcessorModule();
        }
    }

    private void useStandaloneProcessor() {
        var otlpTraceOptions = new OtlpExporterOptions
        {
            Endpoint = new Uri("http://otel-collector:4317"),
            Protocol = OtlpExportProtocol.Grpc,
        };
        var traceExporter = new OtlpTraceExporter(otlpTraceOptions);

        var otlpLogOptions = new OtlpExporterOptions
        {
            Endpoint = new Uri("http://otel-collector:4318/v1/logs"),
            Protocol = OtlpExportProtocol.HttpProtobuf,
        };
        var logExporter = new OtlpLogExporter(otlpLogOptions);

        var loggerFactory = LoggerFactory.Create(builder =>
            builder.AddOpenTelemetry(options =>
            {
                options.IncludeScopes = true;
                options.ParseStateValues = true;
                options.AddOtlpExporter(o =>
                {
                    o.Endpoint = new Uri("http://otel-collector:4318/v1/logs");
                    o.Protocol = OtlpExportProtocol.HttpProtobuf;
                });
            }));

        var logger = loggerFactory.CreateLogger<Activity>();

        using var tracerProvider = Sdk.CreateTracerProviderBuilder()
            .AddSource(Program.ServiceName)
            .SetResourceBuilder(
                ResourceBuilder.CreateDefault()
                    .AddService(serviceName: Program.ServiceName, serviceVersion: Program.ServiceVersion))
            .AddProcessor(new PartialSpanProcessor<Activity>(logger))
            .AddProcessor(new BatchActivityExportProcessor(traceExporter))
            .Build();

        Console.WriteLine("===============> Hello, World!");

        const string rootName = "activity-root-span";
        using var activity = SActivitySource.StartActivity(rootName);
        Console.WriteLine("===============> Activity root-span");

        /* for loop execution */
        for (var a = 0; a < 3; a += 1) {
            var n = $"activity-sub-span-{a}";
            using (var subActivity = SActivitySource.StartActivity(n))
            {
                Console.WriteLine($"===============> iteration: {a}");
            }
            Thread.Sleep(10000);
        }
    }

    private void usePartialProcessorModule() {
        Console.WriteLine(
            "To use this, 1. uncomment the code\n" +
            "2. uncomment the imports\n" +
            "3. uncomment the ProjectReference on the .csproj file"
        );

//        var otlpTraceOptions = new OtlpExporterOptions
//        {
//            Endpoint = new Uri("http://otel-collector:4317"),
//            Protocol = OtlpExportProtocol.Grpc,
//        };
//        var traceExporter = new OtlpTraceExporter(otlpTraceOptions);
//
//        var otlpLogOptions = new OtlpExporterOptions
//        {
//            Endpoint = new Uri("http://otel-collector:4318/v1/logs"),
//            Protocol = OtlpExportProtocol.HttpProtobuf,
//        };
//        var logExporter = new OtlpLogExporter(otlpLogOptions);
//
//        using var tracerProvider = Sdk.CreateTracerProviderBuilder()
//            .AddSource(Program.ServiceName)
//            .SetResourceBuilder(
//                ResourceBuilder.CreateDefault()
//                    .AddService(serviceName: Program.ServiceName, serviceVersion: Program.ServiceVersion))
//            .AddProcessor(new BatchPartialActivityExportProcessor(traceExporter, logExporter))
//            .Build();
//
//        Console.WriteLine("===============> Hello, World!");
//
//        const string rootName = "activity-root-span";
//        using var activity = TestLogsToPartialSpans.SActivitySource.StartActivity(rootName);
//        Console.WriteLine("===============> Activity root-span");
//
//        /* for loop execution */
//        for (var a = 0; a < 3; a += 1) {
//            var n = $"activity-sub-span-{a}";
//            using (var subActivity = TestLogsToPartialSpans.SActivitySource.StartActivity(n))
//            {
//                Console.WriteLine($"===============> iteration: {a}");
//            }
//            Thread.Sleep(10000);
//        }
    }
}
