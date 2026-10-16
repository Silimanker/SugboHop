from datetime import time
from decimal import Decimal

from django.core.management.base import BaseCommand
from django.db import transaction

from backend.models import Island, Stay, TransitRoute

# Placeholder photo from the design spec; swap per island when real assets exist.
IMG = "https://images.unsplash.com/photo-1507525428034-b723cf961d3e?auto=format&fit=crop&w=1200&q=80"

ISLANDS = [
    {
        "slug": "bantayan-island",
        "name": "Bantayan Island",
        "tagline": "Sandbars & slow living",
        "description": "Powdery white sand beaches and quiet dockside glamping pods.",
        "location_region": "Northern Cebu, Region 7",
        "ferry_duration_mins": 60,
        "rating": "4.80",
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
        "stay": ("Reef Villa", "Villa", "2100.00"),
        "route": ("Cebu Pier 1", "06:00", "800.00"),
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
                    "hero_image": IMG,
                    "ferry_duration_mins": data["ferry_duration_mins"],
                    "rating": Decimal(data["rating"]),
                    "is_featured": True,
                },
            )
            stay_name, stay_type, price = data["stay"]
            Stay.objects.update_or_create(
                island=island, name=stay_name,
                defaults={"stay_type": stay_type, "price_per_night": Decimal(price), "image_url": IMG},
            )
            origin, dep, fare = data["route"]
            hh, mm = map(int, dep.split(":"))
            TransitRoute.objects.update_or_create(
                destination_island=island, origin=origin,
                defaults={"operator_name": OPERATOR, "departure_time": time(hh, mm), "price": Decimal(fare)},
            )
            self.stdout.write(f"{'Created' if created else 'Updated'}: {island.name}")
        self.stdout.write(self.style.SUCCESS("Region 7 seed complete."))
