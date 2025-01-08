using System.Diagnostics;
using Microsoft.Extensions.Logging;
using OpenTelemetry;
using OpenTelemetry.Logs;
using OpenTelemetry.Metrics;
using OpenTelemetry.Resources;
using OpenTelemetry.Trace;

namespace OtelDotnetTest;

public class OtelSdkProvider
{

    // Create an ActivitySource to use for starting spans
    private static readonly ActivitySource MyActivitySource =
        new ActivitySource("Dotnet.Tester");


    public void Run()
    {
        var tracerProvider = Sdk.CreateTracerProviderBuilder()
            // .SetResourceBuilder(ResourceBuilder.CreateDefault()
            //     .AddService("MyServiceName"))
            .AddConsoleExporter()
            .Build();

        var meterProvider = Sdk.CreateMeterProviderBuilder()
            .AddConsoleExporter()
            .Build();

        var loggerFactory = LoggerFactory.Create(builder =>
        {
            builder.AddOpenTelemetry(logging =>
            {
                logging.AddConsoleExporter();
            });
        });

        // Now you can create spans from your ActivitySource
        CreateSomeSpans(tracerProvider.GetTracer("dotnet-tester"));

        Console.WriteLine("Press any key to exit...");
        Console.ReadKey();
    }

    private static void CreateSomeSpans(Tracer tracer)
    {

        tracer.StartRootSpan("root-span");
    }
    
}