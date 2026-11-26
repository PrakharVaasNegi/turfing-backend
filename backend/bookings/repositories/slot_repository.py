from django.utils import timezone

from ..enums import BookingStatus
from ..exceptions import SlotNotFound
from ..models import Slot


class SlotRepository:

    @classmethod
    def get_by_id(cls, slot_id: int) -> Slot:
        try:
            return Slot.objects.select_related("turf", "turf__owner").get(id=slot_id)
        except Slot.DoesNotExist as exc:
            raise SlotNotFound(f"Slot {slot_id} not found") from exc

    @classmethod
    def get_upcoming_active_for_turf(cls, turf_id: int):
        return Slot.objects.filter(
            turf_id=turf_id,
            is_active=True,
            start_time__gt=timezone.now(),
        )

    @classmethod
    def get_upcoming_available_for_turf(cls, turf_id: int):
        return cls.get_upcoming_active_for_turf(turf_id).exclude(
            bookings__status=BookingStatus.CONFIRMED
        )

    @classmethod
    def list_for_turf(cls, turf_id: int):
        """All slots for a turf (owner view — includes past + inactive)."""
        return Slot.objects.filter(turf_id=turf_id).order_by("start_time")

    @classmethod
    def booked_slot_ids(cls, slot_ids):
        from ..models import Booking

        return set(
            Booking.objects.filter(
                slot_id__in=slot_ids, status=BookingStatus.CONFIRMED,
            ).values_list("slot_id", flat=True)
        )

    @classmethod
    def create(cls, turf, **data) -> Slot:
        return Slot.objects.create(turf=turf, **data)

    @classmethod
    def get_or_create(cls, turf, start_time, defaults: dict):
        """Returns (slot, was_created)."""
        return Slot.objects.get_or_create(
            turf=turf, start_time=start_time, defaults=defaults,
        )
