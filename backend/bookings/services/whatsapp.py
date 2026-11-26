import logging

from django.conf import settings

from ..enums import NotificationStatus

logger = logging.getLogger(__name__)


class WhatsAppService:
    """Sends WhatsApp messages via Twilio. No-ops with a log when creds are blank."""

    @classmethod
    def _player_body(cls, booking) -> str:
        slot = booking.slot
        turf = slot.turf
        return (
            f"Hi {booking.name}, your slot at {turf.name} is confirmed!\n"
            f"Where: {turf.location}\n"
            f"When: {slot.start_time:%a %d %b %Y, %H:%M} UTC\n"
            f"Duration: {slot.duration_minutes} min\n"
            f"Price: ₹{slot.price}\n"
            f"Booking ID: #{booking.id}"
        )

    @classmethod
    def _owner_body(cls, booking) -> str:
        slot = booking.slot
        turf = slot.turf
        return (
            f"New booking at {turf.name}!\n"
            f"Player: {booking.name} ({booking.whatsapp_number})\n"
            f"When: {slot.start_time:%a %d %b %Y, %H:%M} UTC\n"
            f"Booking ID: #{booking.id}"
        )

    @classmethod
    def _send(cls, to_number: str, body: str) -> tuple[str, str]:
        full_to = f"whatsapp:{to_number}"

        if not (settings.TWILIO_ACCOUNT_SID and settings.TWILIO_AUTH_TOKEN):
            logger.info("whatsapp.dry_run to=%s body=%s", full_to, body)
            return NotificationStatus.DRY_RUN, "Twilio credentials not configured."

        try:
            from twilio.rest import Client

            client = Client(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)
            client.messages.create(
                from_=settings.TWILIO_WHATSAPP_FROM, to=full_to, body=body,
            )
            return NotificationStatus.SENT, ""
        except Exception as exc:  # pragma: no cover
            logger.exception("whatsapp.send_failed to=%s", full_to)
            return NotificationStatus.FAILED, str(exc)

    @classmethod
    def notify_booking_created(cls, booking) -> tuple[str, str]:
        """
        Notify both player and turf owner. Returns (status, error) describing
        the player notification — the one shown back to the booking user.
        """
        player_status, player_err = cls._send(
            to_number=booking.whatsapp_number, body=cls._player_body(booking),
        )

        owner_phone = (
            booking.slot.turf.owner.whatsapp_number
            if booking.slot.turf.owner and booking.slot.turf.owner.whatsapp_number
            else ""
        )
        if owner_phone:
            cls._send(to_number=owner_phone, body=cls._owner_body(booking))

        return player_status, player_err
