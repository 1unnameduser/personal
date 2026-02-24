using System.Diagnostics;

class Program
{
    static void Main()
    {
        // Путь к исполняемому файлу без расширения
        var assemblyLocation = AppDomain.CurrentDomain.BaseDirectory;
        var executableFileName = Path.GetFileNameWithoutExtension(AppDomain.CurrentDomain.FriendlyName);

        // Полный путь к батнику
        var batFilePath = Path.Combine(assemblyLocation, $"{executableFileName}.bat");

        // Быстро запускаем батник без окна и ожидания
        Process.Start(new ProcessStartInfo($"{batFilePath}")
        {
            UseShellExecute = false,
            CreateNoWindow = true
        });
    }
}
