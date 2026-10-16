using SugboHop.Shared.Models;

namespace SugboHop.Client.Services;

public class AuthService(ApiClient api, TokenStore tokens, ApiAuthStateProvider authState)
{
    public async Task LoginAsync(LoginRequest request) =>
        await PersistAsync(await api.PostAsync<AuthResponse>("api/auth/login/", request));

    public async Task RegisterAsync(RegisterRequest request) =>
        await PersistAsync(await api.PostAsync<AuthResponse>("api/auth/register/", request));

    public async Task LogoutAsync()
    {
        try { await api.PostNoContentAsync("api/auth/logout/", auth: true); }
        catch (ApiException) { /* token already invalid: still clear locally */ }
        await authState.MarkUserAsLoggedOutAsync();
    }

    public Task<UserDto> GetProfileAsync() => api.GetAsync<UserDto>("api/auth/me/", auth: true);

    private async Task PersistAsync(AuthResponse auth)
    {
        await tokens.SaveAsync(auth);
        authState.NotifyAuthenticated(auth.User);
    }
}
