from rest_framework import viewsets, status
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.decorators import action
from IdentityManager import serializers as identity_seraiizers
from IdentityManager import models as identity_models
from IdentityManager import helpers as identity_helper
from drf_yasg.utils import swagger_auto_schema

# Create your views here.


class IdentityIdentifyViewset(viewsets.ViewSet):

    @swagger_auto_schema(
        methods=["POST"],
        request_body=identity_seraiizers.IdentityRequestSerializer,
        responses={
            status.HTTP_200_OK: identity_seraiizers.IdentityContactResponseSerailizer
        },
    )
    @action(methods=["POST"], detail=False)
    def create(self, request: Request, *args, **kweargs):

        request_data = request.data

        request_data_serializer = identity_seraiizers.IdentityRequestSerializer(
            data=request_data
        )
        request_data_serializer.is_valid(raise_exception=True)

        email = request_data.get("email")
        phoneNumber = request_data.get("phoneNumber")

        primary_identity = identity_helper.handle_identity_contacts(
            email=email, phoneNumber=phoneNumber
        )

        response_serailizer = identity_seraiizers.IdentityContactResponseSerailizer(
            instance=primary_identity
        )

        return Response(response_serailizer.data)
