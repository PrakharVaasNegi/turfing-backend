from ..exceptions import TurfNotFound
from ..models import Turf, TurfOwner


class TurfRepository:

    @classmethod
    def list_active(cls):
        return Turf.objects.filter(is_active=True).select_related("owner")

    @classmethod
    def list_for_owner(cls, owner: TurfOwner):
        return Turf.objects.filter(owner=owner).order_by("name")

    @classmethod
    def get_by_id(cls, turf_id: int) -> Turf:
        try:
            return Turf.objects.select_related("owner").get(id=turf_id)
        except Turf.DoesNotExist as exc:
            raise TurfNotFound(f"Turf {turf_id} not found") from exc

    @classmethod
    def create(cls, owner: TurfOwner, **data) -> Turf:
        return Turf.objects.create(owner=owner, **data)

    @classmethod
    def update(cls, turf: Turf, **data) -> Turf:
        for key, value in data.items():
            setattr(turf, key, value)
        turf.save()
        return turf
