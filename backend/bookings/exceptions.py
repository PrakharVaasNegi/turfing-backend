class SlotNotFound(Exception):
    pass


class SlotNotAvailable(Exception):
    """Slot is inactive, in the past, or already booked."""

    def __init__(self, reason: str, *args: object):
        super().__init__(args)
        self.message = reason


class InvalidWhatsAppNumber(Exception):
    pass


class BookingNotFound(Exception):
    pass
