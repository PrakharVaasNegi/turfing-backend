from ..enums import BookingStatus, NotificationStatus
from ..models import Booking, Slot


class BookingRepository:

    @classmethod
    def create_confirmed(cls, slot: Slot, name: str, whatsapp_number: str) -> Booking:
        return Booking.objects.create(
            slot=slot,
            name=name,
            whatsapp_number=whatsapp_number,
            status=BookingStatus.CONFIRMED,
            notification_status=NotificationStatus.PENDING,
        )

    @classmethod
    def mark_notification(cls, booking: Booking, status: str, error: str = "") -> Booking:
        booking.notification_status = status
        booking.notification_error = error
        booking.save(update_fields=["notification_status", "notification_error", "updated_at"])
        return booking

    @classmethod
    def by_whatsapp_number(cls, whatsapp_number: str):
        return (
            Booking.objects
            .select_related("slot", "slot__turf")
            .filter(whatsapp_number=whatsapp_number)
        )

    @classmethod
    def for_owner(cls, owner_id: int):
        return (
            Booking.objects
            .select_related("slot", "slot__turf")
            .filter(slot__turf__owner_id=owner_id)
        )

    @classmethod
    def confirmed_for_slot_exists(cls, slot_id: int) -> bool:
        return Booking.objects.filter(
            slot_id=slot_id, status=BookingStatus.CONFIRMED
        ).exists()
