using SugboHop.Shared.Models;

namespace SugboHop.Client.Services;

public class CatalogService(ApiClient api)
{
    public async Task<List<IslandDto>> GetIslandsAsync(bool featuredOnly = false)
    {
        var page = await api.GetAsync<PagedResult<IslandDto>>(
            featuredOnly ? "api/islands/?featured=true" : "api/islands/");
        return page.Results;
    }

    public Task<IslandDto> GetIslandAsync(string slug) =>
        api.GetAsync<IslandDto>($"api/islands/{Uri.EscapeDataString(slug)}/");

    public async Task<List<TransitRouteDto>> GetRoutesAsync(string islandSlug)
    {
        var page = await api.GetAsync<PagedResult<TransitRouteDto>>(
            $"api/routes/?island={Uri.EscapeDataString(islandSlug)}");
        return page.Results;
    }
}
