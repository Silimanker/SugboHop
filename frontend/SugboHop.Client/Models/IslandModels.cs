namespace SugboHop.Client.Models
{
    public class IslandDto
    {
        public int Id { get; set; }
        public string Name { get; set; } = string.Empty;
        public string Slug { get; set; } = string.Empty;
        public string Tagline { get; set; } = string.Empty;
        public string Description { get; set; } = string.Empty;
        public string LocationRegion { get; set; } = string.Empty;
        public string HeroImage { get; set; } = string.Empty;
        public int FerryDurationMins { get; set; }
        public double Rating { get; set; }
        public bool IsFeatured { get; set; }
        public List<StayDto> Stays { get; set; } = new();
    }

    public class StayDto
    {
        public int Id { get; set; }
        public string Name { get; set; } = string.Empty;
        public string StayType { get; set; } = string.Empty;
        public decimal PricePerNight { get; set; }
        public string ImageUrl { get; set; } = string.Empty;
    }

    public class TransitRouteDto
    {
        public int Id { get; set; }
        public string Origin { get; set; } = string.Empty;
        public int DestinationIsland { get; set; }
        public string IslandSlug { get; set; } = string.Empty;
        public string IslandName { get; set; } = string.Empty;
        public string OperatorName { get; set; } = string.Empty;
        public TimeSpan DepartureTime { get; set; }
        public decimal Price { get; set; }
    }

    public class PagedResult<T>
    {
        public int Count { get; set; }
        public string? Next { get; set; }
        public string? Previous { get; set; }
        public List<T> Results { get; set; } = new();
    }
}
