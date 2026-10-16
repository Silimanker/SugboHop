from datetime import time
from decimal import Decimal

from django.contrib.auth import get_user_model
from django.test import TestCase

from .models import Island, Stay, TransitRoute


class ModelTests(TestCase):
    def setUp(self):
        self.island = Island.objects.create(
            name="Bantayan Island",
            slug="bantayan-island",
            tagline="Sandbars & slow living",
            description="Powdery white sand beaches.",
            hero_image="https://example.com/bantayan.jpg",
            ferry_duration_mins=60,
        )

    def test_island_defaults(self):
        self.assertEqual(self.island.location_region, "Cebu, Region 7")
        self.assertEqual(self.island.rating, Decimal("4.80"))
        self.assertTrue(self.island.is_featured)

    def test_stay_related_name(self):
        Stay.objects.create(
            island=self.island, name="Dockside Pod", stay_type="Glamping",
            price_per_night=Decimal("1200.00"), image_url="https://example.com/pod.jpg",
        )
        self.assertEqual(self.island.stays.count(), 1)

    def test_transit_route_str(self):
        route = TransitRoute.objects.create(
            origin="Hagnaya Port", destination_island=self.island,
            operator_name="Island Shipping", departure_time=time(9, 0),
            price=Decimal("350.00"),
        )
        self.assertEqual(str(route), "Hagnaya Port → Bantayan Island (09:00)")
        self.assertEqual(self.island.routes.count(), 1)

    def test_custom_user_fields(self):
        user = get_user_model().objects.create_user(
            username="daniel", email="daniel@example.com", password="pw12345!x",
            phone_number="+63 917 123 4567",
        )
        self.assertEqual(user.phone_number, "+63 917 123 4567")
