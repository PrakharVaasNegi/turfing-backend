from django.db import models

from common.models import AbstractModelWithTimeStamps

from .turf_owner import TurfOwner


class Turf(AbstractModelWithTimeStamps):
    owner = models.ForeignKey(
        TurfOwner, on_delete=models.CASCADE, related_name="turfs"
    )
    name = models.CharField(max_length=160)
    location = models.CharField(max_length=255)
    description = models.TextField(blank=True, default="")
    image_url = models.URLField(max_length=1000, blank=True, default="")
    is_active = models.BooleanField(default=True)

    class Meta:
        db_table = "turf"
        ordering = ["name"]

    def __str__(self) -> str:
        return self.name
