from turfs.services.turf import TurfService

from ..repositories.slot_repository import SlotRepository
from ..serializers import SlotSerializer


class SlotService:

    @classmethod
    def _serialize_with_booked_flag(cls, slots):
        slots = list(slots)
        booked = SlotRepository.booked_slot_ids([s.id for s in slots])
        return SlotSerializer(
            slots, many=True, context={"is_booked_map": {sid: True for sid in booked}}
        ).data

    @classmethod
    def list_for_turf_public(cls, turf_id: int, only_available: bool = True):
        if only_available:
            slots = SlotRepository.get_upcoming_available_for_turf(turf_id=turf_id)
        else:
            slots = SlotRepository.get_upcoming_active_for_turf(turf_id=turf_id)
        return cls._serialize_with_booked_flag(slots=slots)

    @classmethod
    def list_for_owner_turf(cls, owner, turf_id: int):
        TurfService.ensure_owner_owns_turf(owner=owner, turf_id=turf_id)
        slots = SlotRepository.list_for_turf(turf_id=turf_id)
        return cls._serialize_with_booked_flag(slots=slots)

    @classmethod
    def create_for_owner(cls, owner, turf_id: int, data: dict):
        turf = TurfService.ensure_owner_owns_turf(owner=owner, turf_id=turf_id)
        slot = SlotRepository.create(turf=turf, **data)
        return SlotSerializer(slot, context={"is_booked_map": {}}).data

    @classmethod
    def bulk_create_for_owner(cls, owner, turf_id: int, slots_data: list[dict]):
        turf = TurfService.ensure_owner_owns_turf(owner=owner, turf_id=turf_id)
        created, skipped = [], 0
        for item in slots_data:
            _slot, was_created = SlotRepository.get_or_create(
                turf=turf,
                start_time=item["start_time"],
                defaults={
                    "duration_minutes": item["duration_minutes"],
                    "price": item["price"],
                    "is_active": item.get("is_active", True),
                },
            )
            if was_created:
                created.append(_slot)
            else:
                skipped += 1
        return {
            "created": SlotSerializer(
                created, many=True, context={"is_booked_map": {}}
            ).data,
            "created_count": len(created),
            "skipped_count": skipped,
        }
