using System.Text.Json;
using Microsoft.JSInterop;
using SugboHop.Client.Models;

namespace SugboHop.Client.Services;

/// <summary>Persists the DRF auth token and cached user in browser localStorage.</summary>
public class TokenStore(IJSRuntime js)
{
    private const string TokenKey = "sugbohop.token";
    private const string UserKey = "sugbohop.user";

    public async ValueTask<string?> GetTokenAsync()
    {
        try { return await js.InvokeAsync<string?>("localStorage.getItem", TokenKey); }
        catch (JSException) { return null; }
    }

    public async ValueTask<UserDto?> GetUserAsync()
    {
        try
        {
            var json = await js.InvokeAsync<string?>("localStorage.getItem", UserKey);
            return string.IsNullOrEmpty(json) ? null : JsonSerializer.Deserialize<UserDto>(json, ApiJson.Options);
        }
        catch (Exception ex) when (ex is JSException or JsonException) { return null; }
    }

    public async ValueTask SaveAsync(AuthResponse auth)
    {
        await js.InvokeVoidAsync("localStorage.setItem", TokenKey, auth.Token);
        await js.InvokeVoidAsync("localStorage.setItem", UserKey,
            JsonSerializer.Serialize(auth.User, ApiJson.Options));
    }

    public async ValueTask ClearAsync()
    {
        await js.InvokeVoidAsync("localStorage.removeItem", TokenKey);
        await js.InvokeVoidAsync("localStorage.removeItem", UserKey);
    }
}
