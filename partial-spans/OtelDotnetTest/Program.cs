// See https://aka.ms/new-console-template for more information
namespace OtelDotnetTest;

public class Program
{
    static void Main(string[] args)
    {
        Console.WriteLine("Hello, World!");
        var sdkProvider = new OtelSdkProvider();
        sdkProvider.Run();
    }
}
