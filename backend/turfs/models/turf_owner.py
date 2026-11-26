from django.conf import settings
from django.db import models

from common.models import AbstractModelWithTimeStamps


class TurfOwner(AbstractModelWithTimeStamps):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="turf_owner_profile",
    )
    business_name = models.CharField(max_length=160)
    whatsapp_number = models.CharField(max_length=20)

    class Meta:
        db_table = "turf_owner"

    def __str__(self) -> str:
        return self.business_name
