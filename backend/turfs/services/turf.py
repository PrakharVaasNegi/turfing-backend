from ..exceptions import TurfAccessDenied
from ..repositories.turf_repository import TurfRepository
from ..serializers import TurfSerializer


class TurfService:

    @classmethod
    def list_active(cls):
        turfs = TurfRepository.list_active()
        return TurfSerializer(turfs, many=True).data

    @classmethod
    def get_active(cls, turf_id: int):
        turf = TurfRepository.get_by_id(turf_id=turf_id)
        return TurfSerializer(turf).data

    @classmethod
    def list_for_owner(cls, owner):
        turfs = TurfRepository.list_for_owner(owner=owner)
        return TurfSerializer(turfs, many=True).data

    @classmethod
    def create_for_owner(cls, owner, data: dict):
        turf = TurfRepository.create(owner=owner, **data)
        return TurfSerializer(turf).data

    @classmethod
    def update_for_owner(cls, owner, turf_id: int, data: dict):
        turf = TurfRepository.get_by_id(turf_id=turf_id)
        if turf.owner_id != owner.id:
            raise TurfAccessDenied("This turf does not belong to you.")
        turf = TurfRepository.update(turf=turf, **data)
        return TurfSerializer(turf).data

    @classmethod
    def ensure_owner_owns_turf(cls, owner, turf_id: int):
        turf = TurfRepository.get_by_id(turf_id=turf_id)
        if turf.owner_id != owner.id:
            raise TurfAccessDenied("This turf does not belong to you.")
        return turf
