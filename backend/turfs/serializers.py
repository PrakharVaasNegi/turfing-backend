import re

from rest_framework import serializers

from .models import Turf, TurfOwner


E164 = re.compile(r"^\+[1-9]\d{7,14}$")


def normalize_whatsapp(value: str) -> str:
    cleaned = re.sub(r"[\s\-()]", "", value or "")
    if not E164.match(cleaned):
        raise serializers.ValidationError(
            "Enter a valid WhatsApp number in E.164 format, e.g. +919812345678."
        )
    return cleaned


class RegisterSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(min_length=8, write_only=True)
    business_name = serializers.CharField(max_length=160)
    whatsapp_number = serializers.CharField(max_length=20)

    def validate_whatsapp_number(self, value: str) -> str:
        return normalize_whatsapp(value)


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)


class TurfOwnerSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(source="user.email", read_only=True)

    class Meta:
        model = TurfOwner
        fields = ("id", "email", "business_name", "whatsapp_number")


class TurfSerializer(serializers.ModelSerializer):
    class Meta:
        model = Turf
        fields = (
            "id",
            "name",
            "location",
            "description",
            "image_url",
            "is_active",
            "created_at",
        )
        read_only_fields = ("id", "created_at")


class TurfWriteSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=160)
    location = serializers.CharField(max_length=255)
    description = serializers.CharField(required=False, allow_blank=True, default="")
    image_url = serializers.URLField(required=False, allow_blank=True, default="")
    is_active = serializers.BooleanField(required=False, default=True)
