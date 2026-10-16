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


# ---- Milestone 2: API, auth, seed ---------------------------------------------
from django.core.management import call_command
from rest_framework.test import APITestCase


class SeedTests(TestCase):
    def test_seed_is_idempotent(self):
        call_command("seed_region7", verbosity=0)
        call_command("seed_region7", verbosity=0)
        self.assertEqual(Island.objects.count(), 4)
        self.assertEqual(Stay.objects.count(), 4)
        self.assertEqual(TransitRoute.objects.count(), 4)


class ApiTests(APITestCase):
    @classmethod
    def setUpTestData(cls):
        call_command("seed_region7", verbosity=0)

    def test_island_list_is_public_with_numeric_decimals(self):
        res = self.client.get("/api/islands/")
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.data["count"], 4)
        body = res.json()["results"][0]
        self.assertIsInstance(body["rating"], float)
        self.assertIn("stays", body)
        self.assertIsInstance(body["stays"][0]["price_per_night"], float)

    def test_island_detail_by_slug_and_filters(self):
        res = self.client.get("/api/islands/bantayan-island/")
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.data["ferry_duration_mins"], 60)
        routes = self.client.get("/api/routes/?island=bantayan-island").json()["results"]
        self.assertEqual(len(routes), 1)
        self.assertEqual(routes[0]["origin"], "Hagnaya Port")
        stays = self.client.get("/api/stays/?island=panglao-island").json()["results"]
        self.assertEqual(len(stays), 1)

    def test_catalogue_is_read_only(self):
        self.assertEqual(self.client.post("/api/islands/", {}).status_code, 405)

    def test_register_login_me_logout(self):
        reg = self.client.post("/api/auth/register/", {
            "email": "Daniel@Example.com", "password": "hopper-2026!",
            "first_name": "Daniel", "last_name": "Duarte", "phone_number": "+63 917 123 4567",
        })
        self.assertEqual(reg.status_code, 201)
        self.assertEqual(reg.data["user"]["email"], "daniel@example.com")

        dup = self.client.post("/api/auth/register/", {"email": "daniel@example.com", "password": "hopper-2026!"})
        self.assertEqual(dup.status_code, 400)

        bad = self.client.post("/api/auth/login/", {"email": "daniel@example.com", "password": "nope"})
        self.assertEqual(bad.status_code, 400)

        login = self.client.post("/api/auth/login/", {"email": "daniel@example.com", "password": "hopper-2026!"})
        self.assertEqual(login.status_code, 200)
        token = login.data["token"]

        self.assertEqual(self.client.get("/api/auth/me/").status_code, 401)
        self.client.credentials(HTTP_AUTHORIZATION=f"Token {token}")
        me = self.client.patch("/api/auth/me/", {"phone_number": "+63 900 000 0000"}, format="json")
        self.assertEqual(me.status_code, 200)
        self.assertEqual(me.data["phone_number"], "+63 900 000 0000")

        self.assertEqual(self.client.post("/api/auth/logout/").status_code, 204)
        self.assertEqual(self.client.get("/api/auth/me/").status_code, 401)


# ---- Ferry passes -----------------------------------------------------------
from datetime import timedelta

from django.utils import timezone


class FerryPassApiTests(APITestCase):
    @classmethod
    def setUpTestData(cls):
        call_command("seed_region7", verbosity=0)
        U = get_user_model()
        cls.alice = U.objects.create_user("alice@x.com", "alice@x.com", "pw12345!x")
        cls.bob = U.objects.create_user("bob@x.com", "bob@x.com", "pw12345!x")
        cls.route = TransitRoute.objects.get(origin="Hagnaya Port")

    def test_requires_auth(self):
        self.assertEqual(self.client.get("/api/passes/").status_code, 401)

    def test_book_and_list_only_own(self):
        self.client.force_authenticate(self.alice)
        day = (timezone.localdate() + timedelta(days=3)).isoformat()
        res = self.client.post("/api/passes/", {"route_id": self.route.id, "travel_date": day}, format="json")
        self.assertEqual(res.status_code, 201)
        self.assertEqual(res.data["status"], "confirmed")
        self.assertEqual(res.data["route"]["island_name"], "Bantayan Island")
        self.assertEqual(self.client.get("/api/passes/").data["count"], 1)

        self.client.force_authenticate(self.bob)
        self.assertEqual(self.client.get("/api/passes/").data["count"], 0)

    def test_past_date_rejected(self):
        self.client.force_authenticate(self.alice)
        day = (timezone.localdate() - timedelta(days=1)).isoformat()
        res = self.client.post("/api/passes/", {"route_id": self.route.id, "travel_date": day}, format="json")
        self.assertEqual(res.status_code, 400)
