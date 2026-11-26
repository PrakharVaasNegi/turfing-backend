import re

from rest_framework import serializers

from .models import Booking, Slot


E164 = re.compile(r"^\+[1-9]\d{7,14}$")


def normalize_whatsapp(value: str) -> str:
    cleaned = re.sub(r"[\s\-()]", "", value or "")
    if not E164.match(cleaned):
        raise serializers.ValidationError(
            "Enter a valid WhatsApp number in E.164 format, e.g. +919812345678."
        )
    return cleaned


class SlotSerializer(serializers.ModelSerializer):
    end_time = serializers.DateTimeField(read_only=True)
    is_booked = serializers.SerializerMethodField()
    turf_id = serializers.IntegerField(source="turf.id", read_only=True)
    turf_name = serializers.CharField(source="turf.name", read_only=True)

    class Meta:
        model = Slot
        fields = (
            "id",
            "turf_id",
            "turf_name",
            "start_time",
            "end_time",
            "duration_minutes",
            "price",
            "is_active",
            "is_booked",
        )

    def get_is_booked(self, slot: Slot) -> bool:
        is_booked_map = self.context.get("is_booked_map")
        if is_booked_map is not None:
            return is_booked_map.get(slot.id, False)
        from .enums import BookingStatus
        return slot.bookings.filter(status=BookingStatus.CONFIRMED).exists()


class SlotWriteSerializer(serializers.Serializer):
    start_time = serializers.DateTimeField()
    duration_minutes = serializers.IntegerField(min_value=15, max_value=240)
    price = serializers.DecimalField(max_digits=8, decimal_places=2, min_value=0)
    is_active = serializers.BooleanField(required=False, default=True)


class BulkSlotWriteSerializer(serializers.Serializer):
    slots = SlotWriteSerializer(many=True, allow_empty=False)

    def validate_slots(self, value):
        if len(value) > 100:
            raise serializers.ValidationError("Cannot create more than 100 slots at once.")
        return value


class BookingWriteSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=120)
    whatsapp_number = serializers.CharField(max_length=20)
    slot_id = serializers.IntegerField()

    def validate_name(self, value: str) -> str:
        value = (value or "").strip()
        if len(value) < 2:
            raise serializers.ValidationError("Name is too short.")
        return value

    def validate_whatsapp_number(self, value: str) -> str:
        return normalize_whatsapp(value)


class BookingReadSerializer(serializers.ModelSerializer):
    slot = SlotSerializer(read_only=True)

    class Meta:
        model = Booking
        fields = (
            "id",
            "name",
            "whatsapp_number",
            "slot",
            "status",
            "notification_status",
            "created_at",
        )
