using System.Diagnostics;
using OpenTelemetry;
using OpenTelemetry.Resources;
using OpenTelemetry.Trace;

namespace OtelDotnetTest;

public class OtelSystemDiagnosticsProvider
{

    private static readonly ActivitySource SActivitySource = new(Program.ServiceName);

    public void Execute()
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
}