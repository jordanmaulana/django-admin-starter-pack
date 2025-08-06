from django.urls import include, path
from rest_framework import routers

from api.v1.api.auth_api import AuthAPI
from api.v1.api.calculations_api import (
    CalculationListCreateAPIView,
    CalculationRetrieveUpdateDestroyAPIView,
)
from api.v1.api.products_api import ProductAPI
from api.v1.api.profile_api import ProfileAPI
from api.v1.api.settings_api import SettingsAPIView

api_router = routers.DefaultRouter()
api_router.register(r"auth", AuthAPI, basename="auth")
api_router.register(r"profile", ProfileAPI, basename="profile")
api_router.register(r"products", ProductAPI, basename="products")

urlpatterns = [
    path("", include(api_router.urls)),
    path(
        "calculations/",
        CalculationListCreateAPIView.as_view(),
        name="calculation-list-create",
    ),
    path(
        "calculations/<str:uid>/",
        CalculationRetrieveUpdateDestroyAPIView.as_view(),
        name="calculation-retrieve-update-destroy",
    ),
    path(
        "auth/reset-password/<uidb64>/<token>/",
        AuthAPI.as_view({"post": "reset_password"}),
        name="password-reset-confirm",
    ),
    path("settings/", SettingsAPIView.as_view(), name="settings-api"),
]
