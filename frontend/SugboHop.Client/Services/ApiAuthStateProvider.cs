using System.Security.Claims;
using Microsoft.AspNetCore.Components.Authorization;
using SugboHop.Client.Models;

namespace SugboHop.Client.Services;

public class ApiAuthStateProvider(TokenStore tokens) : AuthenticationStateProvider
{
    private static readonly AuthenticationState Anonymous =
        new(new ClaimsPrincipal(new ClaimsIdentity()));

    public override async Task<AuthenticationState> GetAuthenticationStateAsync()
    {
        var token = await tokens.GetTokenAsync();
        var user = await tokens.GetUserAsync();
        if (string.IsNullOrEmpty(token) || user is null) return Anonymous;
        return new AuthenticationState(BuildPrincipal(user));
    }

    public void NotifyAuthenticated(UserDto user) =>
        NotifyAuthenticationStateChanged(Task.FromResult(new AuthenticationState(BuildPrincipal(user))));

    public async Task MarkUserAsLoggedOutAsync()
    {
        await tokens.ClearAsync();
        NotifyAuthenticationStateChanged(Task.FromResult(Anonymous));
    }

    private static ClaimsPrincipal BuildPrincipal(UserDto user)
    {
        var claims = new[]
        {
            new Claim(ClaimTypes.NameIdentifier, user.Id.ToString()),
            new Claim(ClaimTypes.Name, user.DisplayName),
            new Claim(ClaimTypes.Email, user.Email),
        };
        return new ClaimsPrincipal(new ClaimsIdentity(claims, "DrfToken"));
    }
}
