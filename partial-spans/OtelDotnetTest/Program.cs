// See https://aka.ms/new-console-template for more information
namespace OtelDotnetTest;

public class Program
{
    public static readonly string ServiceName = "Dotnet.Tester";
    public static readonly string ServiceVersion = "1.0.0";

    static void Main(string[] args)
    {
        // var sdkShimProvider = new OtelSdkShimProvider();
        // sdkShimProvider.Execute();

        var otelSdProvider = new OtelSystemDiagnosticsProvider();
        otelSdProvider.Execute();
    }
}
