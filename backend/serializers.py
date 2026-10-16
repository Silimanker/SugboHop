from django.contrib.auth import get_user_model
from rest_framework import serializers

from .models import Island, Stay, TransitRoute

User = get_user_model()


class StaySerializer(serializers.ModelSerializer):
    class Meta:
        model = Stay
        fields = ["id", "name", "stay_type", "price_per_night", "image_url"]


class IslandSerializer(serializers.ModelSerializer):
    """Mirrors the C# IslandDto (snake_case on the wire)."""
    stays = StaySerializer(many=True, read_only=True)

    class Meta:
        model = Island
        fields = [
            "id", "name", "slug", "tagline", "description", "location_region",
            "hero_image", "ferry_duration_mins", "rating", "is_featured", "stays",
        ]


class TransitRouteSerializer(serializers.ModelSerializer):
    island_slug = serializers.SlugRelatedField(
        source="destination_island", slug_field="slug", read_only=True
    )
    island_name = serializers.CharField(source="destination_island.name", read_only=True)

    class Meta:
        model = TransitRoute
        fields = [
            "id", "origin", "destination_island", "island_slug", "island_name",
            "operator_name", "departure_time", "price",
        ]


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "email", "first_name", "last_name", "phone_number", "avatar_url"]
        read_only_fields = ["id", "email"]


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=8, style={"input_type": "password"})

    class Meta:
        model = User
        fields = ["email", "password", "first_name", "last_name", "phone_number"]
        extra_kwargs = {"email": {"required": True}}

    def validate_email(self, value):
        value = value.strip().lower()
        if User.objects.filter(email__iexact=value).exists():
            raise serializers.ValidationError("An account with this email already exists.")
        return value

    def create(self, validated_data):
        email = validated_data["email"]
        return User.objects.create_user(username=email, **validated_data)


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True, style={"input_type": "password"})
