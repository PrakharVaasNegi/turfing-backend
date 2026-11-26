from django.db import models

from common.models import AbstractModelWithTimeStamps

from ..enums import BookingStatus, NotificationStatus
from .slot import Slot


class Booking(AbstractModelWithTimeStamps):
    slot = models.ForeignKey(Slot, on_delete=models.CASCADE, related_name="bookings")
    name = models.CharField(max_length=120)
    whatsapp_number = models.CharField(max_length=20)
    status = models.CharField(max_length=16, default=BookingStatus.CONFIRMED)
    notification_status = models.CharField(
        max_length=16, default=NotificationStatus.PENDING
    )
    notification_error = models.TextField(blank=True, default="")

    class Meta:
        db_table = "booking"
        ordering = ["-created_at"]
        constraints = [
            models.UniqueConstraint(
                fields=["slot"],
                condition=models.Q(status=BookingStatus.CONFIRMED),
                name="unique_confirmed_booking_per_slot",
            )
        ]

    def __str__(self) -> str:
        return f"{self.name} @ {self.slot}"
