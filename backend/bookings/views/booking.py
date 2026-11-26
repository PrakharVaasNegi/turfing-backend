import logging

from rest_framework.views import APIView

from common import response
from common.mixins.standard_api_response_mixin import (
    StandardAPIError,
    StandardAPIResponseMixin,
)
from turfs.views._mixins import OwnerAuthMixin

from ..exceptions import SlotNotAvailable, SlotNotFound
from ..serializers import BookingWriteSerializer
from ..services.booking import BookingService

logger = logging.getLogger(__name__)


class BookingListCreateView(StandardAPIResponseMixin, APIView):
    """POST = create booking (public). GET ?phone= = lookup by phone (public)."""

    def post(self, request):
        serializer = BookingWriteSerializer(data=request.data)
        if not serializer.is_valid():
            return response.BadRequest(
                data=self.error_response(
                    errors=self.convert_serializer_errors(serializer.errors)
                )
            )

        data = serializer.validated_data
        try:
            booking = BookingService.create_booking(
                name=data["name"],
                whatsapp_number=data["whatsapp_number"],
                slot_id=data["slot_id"],
            )
        except SlotNotFound:
            return response.NotFound(
                data=self.error_response(errors=[
                    StandardAPIError(
                        err_type="SlotNotFound", message="Slot does not exist.",
                        key="slot_id",
                    )
                ])
            )
        except SlotNotAvailable as exc:
            return response.Conflict(
                data=self.error_response(errors=[
                    StandardAPIError(
                        err_type="SlotNotAvailable", message=exc.message,
                        key="slot_id",
                    )
                ])
            )

        return response.Created(data=self.data_response(data={
            "booking": BookingService.get_serialized_booking(booking)
        }))

    def get(self, request):
        phone = request.query_params.get("phone")
        if not phone:
            return response.BadRequest(
                data=self.error_response(errors=[
                    StandardAPIError(
                        err_type="ValidationError",
                        message="phone query param is required.", key="phone",
                    )
                ])
            )
        try:
            bookings = BookingService.list_by_whatsapp(whatsapp_number=phone)
        except Exception:
            return response.BadRequest(
                data=self.error_response(errors=[
                    StandardAPIError(
                        err_type="ValidationError",
                        message="Invalid phone number.", key="phone",
                    )
                ])
            )
        return response.Ok(data=self.data_response(data={"bookings": bookings}))


class OwnerBookingListView(OwnerAuthMixin, StandardAPIResponseMixin, APIView):
    """GET /api/owner/bookings/ — all bookings across the owner's turfs."""

    def get(self, request):
        owner = self.get_owner(request)
        bookings = BookingService.list_for_owner(owner=owner)
        return response.Ok(data=self.data_response(data={"bookings": bookings}))
