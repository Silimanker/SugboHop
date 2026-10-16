using System.Text.Json;

namespace SugboHop.Client.Services;

/// <summary>Django REST Framework speaks snake_case; our DTOs are PascalCase.</summary>
public static class ApiJson
{
    public static readonly JsonSerializerOptions Options = new()
    {
        PropertyNamingPolicy = JsonNamingPolicy.SnakeCaseLower,
        PropertyNameCaseInsensitive = true,
    };
}
