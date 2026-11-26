from datetime import timedelta

from django.db import models

from common.models import AbstractModelWithTimeStamps


class Slot(AbstractModelWithTimeStamps):
    turf = models.ForeignKey(
        "turfs.Turf", on_delete=models.CASCADE, related_name="slots"
    )
    start_time = models.DateTimeField()
    duration_minutes = models.PositiveIntegerField(default=60)
    price = models.DecimalField(max_digits=8, decimal_places=2, default=0)
    is_active = models.BooleanField(default=True)

    class Meta:
        db_table = "slot"
        ordering = ["start_time"]
        constraints = [
            models.UniqueConstraint(
                fields=["turf", "start_time"],
                name="unique_slot_per_turf_starttime",
            )
        ]

    def __str__(self) -> str:
        return f"{self.turf_id} · {self.start_time:%Y-%m-%d %H:%M} ({self.duration_minutes}m)"

    @property
    def end_time(self):
        return self.start_time + timedelta(minutes=self.duration_minutes)
