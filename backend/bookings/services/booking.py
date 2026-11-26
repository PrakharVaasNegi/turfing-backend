import logging

from django.db import transaction
from django.utils import timezone

from ..exceptions import SlotNotAvailable, SlotNotFound
from ..repositories.booking_repository import BookingRepository
from ..repositories.slot_repository import SlotRepository
from ..serializers import BookingReadSerializer, normalize_whatsapp
from .whatsapp import WhatsAppService

logger = logging.getLogger(__name__)


class BookingService:

    @classmethod
    def _validate_slot_is_bookable(cls, slot):
        if not slot.is_active:
            raise SlotNotAvailable("This slot is not available.")
        if slot.start_time <= timezone.now():
            raise SlotNotAvailable("This slot is in the past.")
        if BookingRepository.confirmed_for_slot_exists(slot_id=slot.id):
            raise SlotNotAvailable("This slot is already booked.")

    @classmethod
    def create_booking(cls, name: str, whatsapp_number: str, slot_id: int):
        slot = SlotRepository.get_by_id(slot_id=slot_id)  # may raise SlotNotFound
        cls._validate_slot_is_bookable(slot=slot)

        with transaction.atomic():
            if BookingRepository.confirmed_for_slot_exists(slot_id=slot.id):
                raise SlotNotAvailable("This slot was just booked. Pick another.")
            booking = BookingRepository.create_confirmed(
                slot=slot, name=name, whatsapp_number=whatsapp_number
            )

        notif_status, error = WhatsAppService.notify_booking_created(booking=booking)
        BookingRepository.mark_notification(
            booking=booking, status=notif_status, error=error
        )

        logger.info("booking.created id=%s notif=%s", booking.id, notif_status)
        return booking

    @classmethod
    def get_serialized_booking(cls, booking) -> dict:
        return BookingReadSerializer(booking).data

    @classmethod
    def list_by_whatsapp(cls, whatsapp_number: str):
        number = normalize_whatsapp(whatsapp_number)
        bookings = BookingRepository.by_whatsapp_number(whatsapp_number=number)
        return BookingReadSerializer(bookings, many=True).data

    @classmethod
    def list_for_owner(cls, owner):
        bookings = BookingRepository.for_owner(owner_id=owner.id)
        return BookingReadSerializer(bookings, many=True).data
