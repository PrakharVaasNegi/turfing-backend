from django.contrib.auth import authenticate
from django.db import transaction
from rest_framework.authtoken.models import Token

from ..exceptions import InvalidCredentials, OwnerAlreadyExists
from ..repositories.turf_owner_repository import TurfOwnerRepository


class AuthService:

    @classmethod
    def register_owner(cls, email: str, password: str, business_name: str, whatsapp_number: str):
        if TurfOwnerRepository.email_exists(email=email):
            raise OwnerAlreadyExists("An account with this email already exists.")

        with transaction.atomic():
            owner = TurfOwnerRepository.create(
                email=email,
                password=password,
                business_name=business_name,
                whatsapp_number=whatsapp_number,
            )
            token, _ = Token.objects.get_or_create(user=owner.user)
        return owner, token.key

    @classmethod
    def login_owner(cls, email: str, password: str):
        user = authenticate(username=email, password=password)
        if user is None:
            raise InvalidCredentials("Invalid email or password.")
        owner = TurfOwnerRepository.get_by_user(user=user)
        if owner is None:
            raise InvalidCredentials("This account is not a turf owner.")
        token, _ = Token.objects.get_or_create(user=user)
        return owner, token.key
