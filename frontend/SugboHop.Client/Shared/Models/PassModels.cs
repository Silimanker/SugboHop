using System.Text.Json.Serialization;

namespace SugboHop.Shared.Models
{
    public class FerryPassDto
    {
        public int Id { get; set; }
        public TransitRouteDto Route { get; set; } = new();
        public DateOnly TravelDate { get; set; }
        public string Status { get; set; } = string.Empty;

        [JsonIgnore]
        public DateTime DepartsAt =>
            TravelDate.ToDateTime(TimeOnly.FromTimeSpan(Route.DepartureTime));
    }

    public class BookPassRequest
    {
        public int RouteId { get; set; }
        public DateOnly TravelDate { get; set; }
    }
}
