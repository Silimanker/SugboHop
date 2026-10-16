from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import FerryPass, Island, Stay, TransitRoute, User


@admin.register(User)
class SugboUserAdmin(UserAdmin):
    fieldsets = UserAdmin.fieldsets + (
        ("SugboHop", {"fields": ("phone_number", "avatar_url")}),
    )
    list_display = ("username", "email", "phone_number", "is_staff")


class StayInline(admin.TabularInline):
    model = Stay
    extra = 0


@admin.register(Island)
class IslandAdmin(admin.ModelAdmin):
    list_display = ("name", "location_region", "ferry_duration_mins", "rating", "is_featured")
    list_filter = ("is_featured", "location_region")
    prepopulated_fields = {"slug": ("name",)}
    search_fields = ("name", "tagline")
    inlines = [StayInline]


@admin.register(Stay)
class StayAdmin(admin.ModelAdmin):
    list_display = ("name", "island", "stay_type", "price_per_night")
    list_filter = ("island", "stay_type")


@admin.register(TransitRoute)
class TransitRouteAdmin(admin.ModelAdmin):
    list_display = ("origin", "destination_island", "operator_name", "departure_time", "price")
    list_filter = ("destination_island",)


@admin.register(FerryPass)
class FerryPassAdmin(admin.ModelAdmin):
    list_display = ("user", "route", "travel_date", "status")
    list_filter = ("status", "travel_date")
