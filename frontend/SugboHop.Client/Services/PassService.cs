using SugboHop.Shared.Models;

namespace SugboHop.Client.Services;

public class PassService(ApiClient api)
{
    public async Task<List<FerryPassDto>> GetMyPassesAsync()
    {
        var page = await api.GetAsync<PagedResult<FerryPassDto>>("api/passes/", auth: true);
        return page.Results;
    }

    public Task<FerryPassDto> BookAsync(int routeId, DateOnly travelDate) =>
        api.PostAsync<FerryPassDto>("api/passes/",
            new BookPassRequest { RouteId = routeId, TravelDate = travelDate }, auth: true);
}
