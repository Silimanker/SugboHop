using System.Globalization;

namespace SugboHop.Client.Services;

public static class Fmt
{
    public static string Peso(decimal value) =>
        "₱" + value.ToString("N0", CultureInfo.InvariantCulture);

    public static string Time(TimeSpan time) =>
        DateTime.Today.Add(time).ToString("hh:mm tt", CultureInfo.InvariantCulture);

    public static string DateTimeLong(DateTime value) =>
        value.ToString("MMM d, yyyy • hh:mm tt", CultureInfo.InvariantCulture);
}
