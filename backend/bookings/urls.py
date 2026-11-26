from django.urls import path

from .views.booking import BookingListCreateView, OwnerBookingListView
from .views.slot import (
    OwnerTurfSlotBulkCreateView,
    OwnerTurfSlotListCreateView,
    PublicTurfSlotListView,
)

urlpatterns = [
    # Public
    path("turfs/<int:turf_id>/slots/", PublicTurfSlotListView.as_view(), name="public-turf-slots"),
    path("bookings/", BookingListCreateView.as_view(), name="booking-list-create"),

    # Owner
    path("owner/turfs/<int:turf_id>/slots/", OwnerTurfSlotListCreateView.as_view(), name="owner-turf-slots"),
    path("owner/turfs/<int:turf_id>/slots/bulk/", OwnerTurfSlotBulkCreateView.as_view(), name="owner-turf-slots-bulk"),
    path("owner/bookings/", OwnerBookingListView.as_view(), name="owner-bookings"),
]
