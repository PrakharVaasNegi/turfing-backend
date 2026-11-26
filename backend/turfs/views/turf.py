import logging

from rest_framework.views import APIView

from common import response
from common.mixins.standard_api_response_mixin import (
    StandardAPIError,
    StandardAPIResponseMixin,
)

from ..exceptions import TurfAccessDenied, TurfNotFound
from ..serializers import TurfWriteSerializer
from ..services.turf import TurfService
from ._mixins import OwnerAuthMixin

logger = logging.getLogger(__name__)


class PublicTurfListView(StandardAPIResponseMixin, APIView):
    """GET /api/turfs/ — list all active turfs (public)."""

    def get(self, request):
        turfs = TurfService.list_active()
        return response.Ok(data=self.data_response(data={"turfs": turfs}))


class PublicTurfDetailView(StandardAPIResponseMixin, APIView):
    """GET /api/turfs/<id>/ — details for one turf (public)."""

    def get(self, request, turf_id: int):
        try:
            turf = TurfService.get_active(turf_id=turf_id)
        except TurfNotFound:
            return response.NotFound(
                data=self.error_response(errors=[
                    StandardAPIError(err_type="TurfNotFound", message="Turf not found.")
                ])
            )
        return response.Ok(data=self.data_response(data={"turf": turf}))


class OwnerTurfListCreateView(OwnerAuthMixin, StandardAPIResponseMixin, APIView):
    """GET/POST /api/owner/turfs/ — list/create the logged-in owner's turfs."""

    def get(self, request):
        owner = self.get_owner(request)
        turfs = TurfService.list_for_owner(owner=owner)
        return response.Ok(data=self.data_response(data={"turfs": turfs}))

    def post(self, request):
        owner = self.get_owner(request)
        serializer = TurfWriteSerializer(data=request.data)
        if not serializer.is_valid():
            return response.BadRequest(
                data=self.error_response(
                    errors=self.convert_serializer_errors(serializer.errors)
                )
            )
        turf = TurfService.create_for_owner(owner=owner, data=serializer.validated_data)
        logger.info("owner.turf_created owner=%s turf=%s", owner.id, turf.get("id"))
        return response.Created(data=self.data_response(data={"turf": turf}))


class OwnerTurfDetailView(OwnerAuthMixin, StandardAPIResponseMixin, APIView):
    """GET/PATCH /api/owner/turfs/<id>/ — manage one turf."""

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
            TurfService.ensure_owner_owns_turf(owner=owner, turf_id=turf_id)
            turf = TurfService.get_active(turf_id=turf_id)
        except (TurfNotFound, TurfAccessDenied) as exc:
            return self._handle_access(exc)
        return response.Ok(data=self.data_response(data={"turf": turf}))

    def patch(self, request, turf_id: int):
        owner = self.get_owner(request)
        serializer = TurfWriteSerializer(data=request.data, partial=True)
        if not serializer.is_valid():
            return response.BadRequest(
                data=self.error_response(
                    errors=self.convert_serializer_errors(serializer.errors)
                )
            )
        try:
            turf = TurfService.update_for_owner(
                owner=owner, turf_id=turf_id, data=serializer.validated_data
            )
        except (TurfNotFound, TurfAccessDenied) as exc:
            return self._handle_access(exc)
        return response.Ok(data=self.data_response(data={"turf": turf}))
