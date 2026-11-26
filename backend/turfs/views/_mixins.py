from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from ..repositories.turf_owner_repository import TurfOwnerRepository


class OwnerAuthMixin:
    """Mixin for views that require a logged-in TurfOwner."""

    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get_owner(self, request):
        return TurfOwnerRepository.get_by_user(user=request.user)
