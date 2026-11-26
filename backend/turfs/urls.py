from django.urls import path

from .views.auth import LoginView, RegisterView
from .views.turf import (
    OwnerTurfDetailView,
    OwnerTurfListCreateView,
    PublicTurfDetailView,
    PublicTurfListView,
)

urlpatterns = [
    # Public (no auth)
    path("turfs/", PublicTurfListView.as_view(), name="public-turf-list"),
    path("turfs/<int:turf_id>/", PublicTurfDetailView.as_view(), name="public-turf-detail"),

    # Owner auth
    path("owner/register/", RegisterView.as_view(), name="owner-register"),
    path("owner/login/", LoginView.as_view(), name="owner-login"),

    # Owner-authenticated turf CRUD
    path("owner/turfs/", OwnerTurfListCreateView.as_view(), name="owner-turf-list-create"),
    path("owner/turfs/<int:turf_id>/", OwnerTurfDetailView.as_view(), name="owner-turf-detail"),
]
