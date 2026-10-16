using SugboHop.Shared.Models;
using SugboHop.Client.Services;

namespace SugboHop.Client.Features.Catalog.Services;

public class CatalogService(ApiClient api)
{
    public async Task<List<IslandDto>> GetIslandsAsync(bool featuredOnly = false, string search = "")
    {
        var query = new List<string>();
        if (featuredOnly) query.Add("featured=true");
        if (!string.IsNullOrWhiteSpace(search))
            query.Add($"search={Uri.EscapeDataString(search.Trim())}");

        var endpoint = "api/islands/";
        if (query.Count > 0) endpoint += $"?{string.Join("&", query)}";
        var page = await api.GetAsync<PagedResult<IslandDto>>(
            endpoint);
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
