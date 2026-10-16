from django.contrib.auth import authenticate, get_user_model
from rest_framework import generics, mixins, status, viewsets
from rest_framework.authtoken.models import Token
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import FerryPass, Island, Stay, TransitRoute
from .serializers import (
    FerryPassSerializer, IslandSerializer, LoginSerializer, RegisterSerializer,
    StaySerializer, TransitRouteSerializer, UserSerializer,
)

User = get_user_model()


def _auth_payload(user):
    token, _ = Token.objects.get_or_create(user=user)
    return {"token": token.key, "user": UserSerializer(user).data}


# ---- Catalogue (public, read-only) -------------------------------------------

class IslandViewSet(viewsets.ReadOnlyModelViewSet):
    """GET /api/islands/?featured=true  |  GET /api/islands/<slug>/"""
    serializer_class = IslandSerializer
    lookup_field = "slug"
    permission_classes = [AllowAny]

    def get_queryset(self):
        qs = Island.objects.prefetch_related("stays")
        if self.request.query_params.get("featured", "").lower() in ("1", "true"):
            qs = qs.filter(is_featured=True)
        return qs


class StayViewSet(viewsets.ReadOnlyModelViewSet):
    """GET /api/stays/?island=<slug>"""
    serializer_class = StaySerializer
    permission_classes = [AllowAny]

    def get_queryset(self):
        qs = Stay.objects.select_related("island")
        slug = self.request.query_params.get("island")
        return qs.filter(island__slug=slug) if slug else qs


class TransitRouteViewSet(viewsets.ReadOnlyModelViewSet):
    """GET /api/routes/?island=<slug>"""
    serializer_class = TransitRouteSerializer
    permission_classes = [AllowAny]

    def get_queryset(self):
        qs = TransitRoute.objects.select_related("destination_island")
        slug = self.request.query_params.get("island")
        return qs.filter(destination_island__slug=slug) if slug else qs


# ---- Ferry passes (authenticated, per-user) ----------------------------------

class FerryPassViewSet(mixins.ListModelMixin, mixins.CreateModelMixin,
                       mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    """GET/POST /api/passes/ — the caller's own passes only."""
    serializer_class = FerryPassSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return FerryPass.objects.filter(user=self.request.user).select_related(
            "route__destination_island"
        )

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


# ---- Auth ---------------------------------------------------------------------

class RegisterView(generics.CreateAPIView):
    """POST /api/auth/register/ -> {token, user}"""
    serializer_class = RegisterSerializer
    permission_classes = [AllowAny]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response(_auth_payload(user), status=status.HTTP_201_CREATED)


class LoginView(APIView):
    """POST /api/auth/login/ -> {token, user}"""
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.validated_data["email"].strip().lower()
        account = User.objects.filter(email__iexact=email).first()
        user = authenticate(
            request,
            username=account.get_username() if account else email,
            password=serializer.validated_data["password"],
        )
        if user is None:
            return Response({"detail": "Invalid email or password."},
                            status=status.HTTP_400_BAD_REQUEST)
        return Response(_auth_payload(user))


class LogoutView(APIView):
    """POST /api/auth/logout/ — revokes the caller's token."""
    permission_classes = [IsAuthenticated]

    def post(self, request):
        Token.objects.filter(user=request.user).delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class MeView(generics.RetrieveUpdateAPIView):
    """GET/PATCH /api/auth/me/"""
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user
