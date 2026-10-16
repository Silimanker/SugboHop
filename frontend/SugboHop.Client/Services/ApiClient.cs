using System.Net;
using System.Net.Http.Headers;
using System.Net.Http.Json;
using System.Text.Json;

namespace SugboHop.Client.Services;

/// <summary>Thin wrapper over HttpClient: snake_case JSON, token header, friendly errors.</summary>
public class ApiClient(HttpClient http, TokenStore tokens, ApiAuthStateProvider authState)
{
    public async Task<T> GetAsync<T>(string path, bool auth = false)
    {
        using var res = await SendAsync(HttpMethod.Get, path, null, auth);
        return await ReadAsync<T>(res);
    }

    public async Task<T> PostAsync<T>(string path, object? body, bool auth = false)
    {
        using var res = await SendAsync(HttpMethod.Post, path, body, auth);
        return await ReadAsync<T>(res);
    }

    public async Task PostNoContentAsync(string path, bool auth = false)
    {
        using var res = await SendAsync(HttpMethod.Post, path, null, auth);
    }

    private async Task<HttpResponseMessage> SendAsync(HttpMethod method, string path, object? body, bool auth)
    {
        using var req = new HttpRequestMessage(method, path);
        if (body is not null)
            req.Content = JsonContent.Create(body, body.GetType(), options: ApiJson.Options);

        if (auth)
        {
            var token = await tokens.GetTokenAsync();
            if (!string.IsNullOrEmpty(token))
                req.Headers.Authorization = new AuthenticationHeaderValue("Token", token);
        }

        HttpResponseMessage res;
        try
        {
            res = await http.SendAsync(req);
        }
        catch (HttpRequestException)
        {
            throw new ApiException(
                "Can't reach the SugboHop API. Is the Django server running on port 8000?", 0);
        }

        if (res.IsSuccessStatusCode) return res;

        var message = await ReadErrorAsync(res);
        var status = (int)res.StatusCode;
        if (res.StatusCode == HttpStatusCode.Unauthorized && auth)
            await authState.MarkUserAsLoggedOutAsync();
        res.Dispose();
        throw new ApiException(message, status);
    }

    private static async Task<T> ReadAsync<T>(HttpResponseMessage res)
    {
        var value = await res.Content.ReadFromJsonAsync<T>(ApiJson.Options);
        return value ?? throw new ApiException("Empty response from server.", (int)res.StatusCode);
    }

    /// <summary>Flattens DRF error bodies ({"detail": ...} or {"field": [..]}) into one sentence.</summary>
    private static async Task<string> ReadErrorAsync(HttpResponseMessage res)
    {
        try
        {
            var json = await res.Content.ReadAsStringAsync();
            using var doc = JsonDocument.Parse(json);
            if (doc.RootElement.ValueKind == JsonValueKind.Object)
            {
                var parts = new List<string>();
                foreach (var prop in doc.RootElement.EnumerateObject())
                {
                    var text = prop.Value.ValueKind == JsonValueKind.Array
                        ? string.Join(" ", prop.Value.EnumerateArray().Select(e => e.ToString()))
                        : prop.Value.ToString();
                    parts.Add(prop.Name is "detail" or "non_field_errors" ? text : $"{Pretty(prop.Name)}: {text}");
                }
                if (parts.Count > 0) return string.Join(" ", parts);
            }
        }
        catch (JsonException) { }
        return $"Request failed ({(int)res.StatusCode}).";
    }

    private static string Pretty(string field)
    {
        var s = field.Replace('_', ' ');
        return s.Length == 0 ? s : char.ToUpperInvariant(s[0]) + s[1..];
    }
}
