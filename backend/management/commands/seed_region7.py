from datetime import time
from decimal import Decimal

from django.core.management.base import BaseCommand
from django.db import transaction

from backend.models import Island, Stay, TransitRoute

ISLANDS = [
    {
        "slug": "bantayan-island",
        "name": "Bantayan Island",
        "tagline": "Sandbars & slow living",
        "description": "Powdery white sand beaches and quiet dockside glamping pods.",
        "location_region": "Northern Cebu, Region 7",
        "ferry_duration_mins": 60,
        "rating": "4.80",
        "image": "photo-1500375592092-40eb2168fd21",
        "stay": ("Dockside Glamping Pod", "Glamping", "1200.00"),
        "route": ("Hagnaya Port", "09:00", "350.00"),
    },
    {
        "slug": "malapascua-island",
        "name": "Malapascua Island",
        "tagline": "Thresher shark diving",
        "description": "A tiny island at the northern tip of Cebu, famous for dawn thresher shark dives.",
        "location_region": "Northern Tip Cebu, Region 7",
        "ferry_duration_mins": 45,
        "rating": "4.85",
        "image": "photo-1544551763-46a013bb70d5",
        "stay": ("Dive Lodge Room", "Dive Lodge", "1800.00"),
        "route": ("Maya Port", "08:00", "300.00"),
    },
    {
        "slug": "camotes-islands",
        "name": "Camotes Islands",
        "tagline": "Caves & cliff-jumping",
        "description": "Limestone caves, turquoise lagoons and cliff-jumping off the Cebu coast.",
        "location_region": "Cebu, Region 7",
        "ferry_duration_mins": 90,
        "rating": "4.70",
        "image": "photo-1510414842594-a61c69b5ae57",
        "stay": ("Lagoon-side Cottage", "Cottage", "950.00"),
        "route": ("Danao Port", "07:30", "400.00"),
    },
    {
        "slug": "panglao-island",
        "name": "Panglao Island",
        "tagline": "Coral reefs & sanctuaries",
        "description": "Bohol's dive-and-wildlife hub, with coral reefs and marine sanctuaries.",
        "location_region": "Bohol, Region 7",
        "ferry_duration_mins": 120,
        "rating": "4.90",
        "image": "photo-1518509562904-e7ef99cdcc86",
        "stay": ("Reef Villa", "Villa", "2100.00"),
        "route": ("Cebu Pier 1", "06:00", "800.00"),
    },
    {
        "slug": "siquijor-island",
        "name": "Siquijor Island",
        "tagline": "Waterfalls & beachside calm",
        "description": "Follow winding coastal roads to Cambugahay Falls, coral gardens, and quiet sunset beaches.",
        "location_region": "Siquijor, Region 7",
        "ferry_duration_mins": 90,
        "rating": "4.88",
        "image": "photo-1501785888041-af3ef285b470",
        "stay": ("Salagdoong Garden Cottage", "Cottage", "1450.00"),
        "route": ("Dumaguete Port", "08:20", "350.00"),
    },
    {
        "slug": "apo-island",
        "name": "Apo Island",
        "tagline": "Sea turtles & coral gardens",
        "description": "A small volcanic island where clear shallows, reef life, and local conservation go hand in hand.",
        "location_region": "Negros Oriental, Region 7",
        "ferry_duration_mins": 40,
        "rating": "4.92",
        "image": "photo-1530789253388-582c481c54b0",
        "stay": ("Marine Sanctuary Homestay", "Homestay", "1100.00"),
        "route": ("Malatapay Port", "09:00", "500.00"),
    },
    {
        "slug": "sumilon-island",
        "name": "Sumilon Island",
        "tagline": "A shifting sandbar escape",
        "description": "Spend a slow day between a brilliant blue lagoon, a white sandbar, and the open sea.",
        "location_region": "Southern Cebu, Region 7",
        "ferry_duration_mins": 15,
        "rating": "4.87",
        "image": "photo-1507525428034-b723cf961d3e",
        "stay": ("Bluewater Island Retreat", "Resort", "3200.00"),
        "route": ("Bancogon Port", "08:00", "1500.00"),
    },
    {
        "slug": "pescador-island",
        "name": "Pescador Island",
        "tagline": "Reef walls & sardine runs",
        "description": "Head offshore from Moalboal for vivid reef walls, thriving marine life, and unforgettable dives.",
        "location_region": "Western Cebu, Region 7",
        "ferry_duration_mins": 25,
        "rating": "4.86",
        "image": "photo-1518837695005-2083093ee35b",
        "stay": ("Moalboal Reef Guesthouse", "Guesthouse", "1350.00"),
        "route": ("Panagsama Beach", "07:00", "600.00"),
    },
]

OPERATOR = "Sugbo Ferry (sample)"


class Command(BaseCommand):
    help = "Seed the Region 7 islands, stays and transit routes (idempotent)."

    @transaction.atomic
    def handle(self, *args, **options):
        for data in ISLANDS:
            island, created = Island.objects.update_or_create(
                slug=data["slug"],
                defaults={
                    "name": data["name"],
                    "tagline": data["tagline"],
                    "description": data["description"],
                    "location_region": data["location_region"],
                    "hero_image": f"https://images.unsplash.com/{data['image']}?auto=format&fit=crop&w=1200&q=80",
                    "ferry_duration_mins": data["ferry_duration_mins"],
                    "rating": Decimal(data["rating"]),
                    "is_featured": True,
                },
            )
            stay_name, stay_type, price = data["stay"]
            Stay.objects.update_or_create(
                island=island, name=stay_name,
                defaults={
                    "stay_type": stay_type,
                    "price_per_night": Decimal(price),
                    "image_url": island.hero_image,
                },
            )
            origin, dep, fare = data["route"]
            hh, mm = map(int, dep.split(":"))
            TransitRoute.objects.update_or_create(
                destination_island=island, origin=origin,
                defaults={"operator_name": OPERATOR, "departure_time": time(hh, mm), "price": Decimal(fare)},
            )
            self.stdout.write(f"{'Created' if created else 'Updated'}: {island.name}")
        self.stdout.write(self.style.SUCCESS("Region 7 seed complete."))
