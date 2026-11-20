using System.Globalization;

namespace SugboHop.Client.Services;

public static class Fmt
{
    public static string Peso(decimal value) =>
        "₱" + value.ToString("N0", CultureInfo.InvariantCulture);

    public static string Time(TimeSpan time) =>
        DateTime.Today.Add(time).ToString("hh:mm tt", CultureInfo.InvariantCulture);

    public static string Duration(int minutes) => minutes >= 60
        ? $"{minutes / 60}h{(minutes % 60 == 0 ? string.Empty : $" {minutes % 60}m")}"
        : $"{minutes} min";

    public static string Date(DateOnly value) =>
        value.ToString("ddd, MMM d, yyyy", CultureInfo.InvariantCulture);

    public static string DateTimeLong(DateTime value) =>
        value.ToString("MMM d, yyyy • hh:mm tt", CultureInfo.InvariantCulture);
}
