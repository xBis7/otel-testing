using OpenTelemetry;
using OpenTelemetry.Resources;
using OpenTelemetry.Trace;

namespace OtelDotnetTest;

public class OtelSdkShimProvider
{
    private readonly Tracer _tracer;

    public OtelSdkShimProvider()
    {
        var tracerProvider = Sdk.CreateTracerProviderBuilder()
            .AddSource(Program.ServiceName)
            .SetResourceBuilder(
                ResourceBuilder.CreateDefault()
                    .AddService(serviceName: Program.ServiceName, serviceVersion: Program.ServiceVersion))
            .AddConsoleExporter()
            .Build();

        _tracer = tracerProvider.GetTracer(Program.ServiceName);
    }

    public void Execute()
    {
        using var parentSpan = _tracer.StartActiveSpan("parent-span");

        Console.WriteLine("===============> Under parent span");

        using (var childSpan = _tracer.StartActiveSpan("child-span"))
        {
            Console.WriteLine("===============> Under child span");
        }

        Console.WriteLine("===============> Back under parent span");
    }
}