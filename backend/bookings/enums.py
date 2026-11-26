from common.enums import Enum


class BookingStatus(Enum):
    CONFIRMED = "confirmed"
    CANCELLED = "cancelled"


class NotificationStatus(Enum):
    PENDING = "pending"
    SENT = "sent"
    FAILED = "failed"
    DRY_RUN = "dry_run"
