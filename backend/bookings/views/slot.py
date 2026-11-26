import logging

from rest_framework.views import APIView

from common import response
from common.mixins.standard_api_response_mixin import (
    StandardAPIError,
    StandardAPIResponseMixin,
)
from turfs.exceptions import TurfAccessDenied, TurfNotFound
from turfs.views._mixins import OwnerAuthMixin

from ..serializers import BulkSlotWriteSerializer, SlotWriteSerializer
from ..services.slot import SlotService

logger = logging.getLogger(__name__)


class PublicTurfSlotListView(StandardAPIResponseMixin, APIView):
    """GET /api/turfs/<turf_id>/slots/ — available slots for a turf (public)."""

    def get(self, request, turf_id: int):
        only_available = request.query_params.get("only_available", "true") == "true"
        slots = SlotService.list_for_turf_public(
            turf_id=turf_id, only_available=only_available
        )
        return response.Ok(data=self.data_response(data={"slots": slots}))


class OwnerTurfSlotListCreateView(OwnerAuthMixin, StandardAPIResponseMixin, APIView):
    """GET/POST /api/owner/turfs/<turf_id>/slots/ — manage slots for own turf."""

    def _handle_access(self, exc):
        if isinstance(exc, TurfNotFound):
            return response.NotFound(data=self.error_response(errors=[
                StandardAPIError(err_type="TurfNotFound", message="Turf not found.")
            ]))
        return response.Forbidden(data=self.error_response(errors=[
            StandardAPIError(err_type="TurfAccessDenied", message=str(exc))
        ]))

    def get(self, request, turf_id: int):
        owner = self.get_owner(request)
        try:
            slots = SlotService.list_for_owner_turf(owner=owner, turf_id=turf_id)
        except (TurfNotFound, TurfAccessDenied) as exc:
            return self._handle_access(exc)
        return response.Ok(data=self.data_response(data={"slots": slots}))

    def post(self, request, turf_id: int):
        owner = self.get_owner(request)
        serializer = SlotWriteSerializer(data=request.data)
        if not serializer.is_valid():
            return response.BadRequest(
                data=self.error_response(
                    errors=self.convert_serializer_errors(serializer.errors)
                )
            )
        try:
            slot = SlotService.create_for_owner(
                owner=owner, turf_id=turf_id, data=serializer.validated_data
            )
        except (TurfNotFound, TurfAccessDenied) as exc:
            return self._handle_access(exc)
        logger.info("owner.slot_created owner=%s turf=%s slot=%s",
                    owner.id, turf_id, slot.get("id"))
        return response.Created(data=self.data_response(data={"slot": slot}))


class OwnerTurfSlotBulkCreateView(OwnerAuthMixin, StandardAPIResponseMixin, APIView):
    """POST /api/owner/turfs/<turf_id>/slots/bulk/ — create many slots atomically."""

    def _handle_access(self, exc):
        if isinstance(exc, TurfNotFound):
            return response.NotFound(data=self.error_response(errors=[
                StandardAPIError(err_type="TurfNotFound", message="Turf not found.")
            ]))
        return response.Forbidden(data=self.error_response(errors=[
            StandardAPIError(err_type="TurfAccessDenied", message=str(exc))
        ]))

    def post(self, request, turf_id: int):
        owner = self.get_owner(request)
        serializer = BulkSlotWriteSerializer(data=request.data)
        if not serializer.is_valid():
            return response.BadRequest(
                data=self.error_response(
                    errors=self.convert_serializer_errors(serializer.errors)
                )
            )
        try:
            result = SlotService.bulk_create_for_owner(
                owner=owner, turf_id=turf_id,
                slots_data=serializer.validated_data["slots"],
            )
        except (TurfNotFound, TurfAccessDenied) as exc:
            return self._handle_access(exc)
        logger.info(
            "owner.slots_bulk_created owner=%s turf=%s created=%s skipped=%s",
            owner.id, turf_id, result["created_count"], result["skipped_count"],
        )
        return response.Created(data=self.data_response(data=result))
