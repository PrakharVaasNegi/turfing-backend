import logging

from rest_framework.views import APIView

from common import response
from common.mixins.standard_api_response_mixin import (
    StandardAPIError,
    StandardAPIResponseMixin,
)

from ..exceptions import InvalidCredentials, OwnerAlreadyExists
from ..serializers import LoginSerializer, RegisterSerializer, TurfOwnerSerializer
from ..services.auth import AuthService

logger = logging.getLogger(__name__)


class RegisterView(StandardAPIResponseMixin, APIView):
    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if not serializer.is_valid():
            return response.BadRequest(
                data=self.error_response(
                    errors=self.convert_serializer_errors(serializer.errors)
                )
            )

        data = serializer.validated_data
        try:
            owner, token = AuthService.register_owner(
                email=data["email"],
                password=data["password"],
                business_name=data["business_name"],
                whatsapp_number=data["whatsapp_number"],
            )
        except OwnerAlreadyExists as exc:
            return response.Conflict(
                data=self.error_response(errors=[
                    StandardAPIError(
                        err_type="OwnerAlreadyExists", message=str(exc), key="email"
                    )
                ])
            )

        logger.info("owner.registered id=%s", owner.id)
        return response.Created(
            data=self.data_response(data={
                "token": token,
                "owner": TurfOwnerSerializer(owner).data,
            })
        )


class LoginView(StandardAPIResponseMixin, APIView):
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if not serializer.is_valid():
            return response.BadRequest(
                data=self.error_response(
                    errors=self.convert_serializer_errors(serializer.errors)
                )
            )

        data = serializer.validated_data
        try:
            owner, token = AuthService.login_owner(
                email=data["email"], password=data["password"]
            )
        except InvalidCredentials as exc:
            return response.UnAuthorized(
                data=self.error_response(errors=[
                    StandardAPIError(
                        err_type="InvalidCredentials", message=str(exc)
                    )
                ])
            )

        return response.Ok(
            data=self.data_response(data={
                "token": token,
                "owner": TurfOwnerSerializer(owner).data,
            })
        )
