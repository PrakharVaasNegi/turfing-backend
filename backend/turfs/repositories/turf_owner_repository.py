from django.contrib.auth import get_user_model

from ..models import TurfOwner

User = get_user_model()


class TurfOwnerRepository:

    @classmethod
    def email_exists(cls, email: str) -> bool:
        return User.objects.filter(username=email).exists()

    @classmethod
    def create(cls, email: str, password: str, business_name: str, whatsapp_number: str) -> TurfOwner:
        user = User.objects.create_user(
            username=email, email=email, password=password
        )
        return TurfOwner.objects.create(
            user=user,
            business_name=business_name,
            whatsapp_number=whatsapp_number,
        )

    @classmethod
    def get_by_user(cls, user) -> TurfOwner | None:
        return TurfOwner.objects.filter(user=user).first()

    @classmethod
    def get_by_turf_id(cls, turf_id: int) -> TurfOwner | None:
        return (
            TurfOwner.objects
            .filter(turfs__id=turf_id)
            .first()
        )
