import json

from django.contrib import messages
from drf_spectacular.types import datetime
from drf_spectacular.utils import extend_schema
from rest_framework import status
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response

from web.exceptions import ServiceUnavailable
from .models import TrelloUser
from .serializers import *


class UsersView(GenericAPIView):
    serializer_class = UserSerializer
    queryset = TrelloUser.objects.all()

    @extend_schema(
        responses={200: ListUsersResponseSerializer},
    )
    def get(self, request):
        response_serializer_class = ListUsersResponseSerializer

        try:
            total_users = TrelloUser.objects.count()
        except Exception:
            raise ServiceUnavailable()

        response_serializer = response_serializer_class(data={
            "total_users": total_users,
            "users": [
                {"id": user.id, "first_name": user.first_name, "last_name": user.last_name, "username": user.username,
                 "email": user.email, "date_joined": user.date_joined, "updated_at": user.updated_at} for user in
                self.get_queryset()], })
        response_serializer.is_valid()
        response = Response(response_serializer.data, status=status.HTTP_200_OK)
        response["cross-origin-opener-policy"] = "unsafe-none"
        response["referrer-policy"] = "no-referrer"
        return response

    @extend_schema(
        request=CreateUserSerializer,
        responses={200: CreateUserResponseSerializer},
    )
    def post(self, request):
        body = json.loads(request.body)
        serializer = CreateUserSerializer(data=body)
        response_serializer_class = CreateUserResponseSerializer
        serializer.is_valid(raise_exception=True)
        first_name = serializer.validated_data.get('first_name')
        last_name = serializer.validated_data.get('last_name')
        username = serializer.validated_data.get('username')
        email = serializer.validated_data.get('email')
        password = serializer.validated_data.get('password')

        if TrelloUser.objects.filter(email=email).exists():
            messages.error(request, 'Email is already taken')
            return Response("Email is already taken", status.HTTP_400_BAD_REQUEST)
        if TrelloUser.objects.filter(username=username).exists():
            messages.error(request, 'Username is already taken')
            return Response("Username is already taken", status.HTTP_400_BAD_REQUEST)

        try:
            user: TrelloUser = TrelloUser.objects.create(
                first_name=first_name,
                last_name=last_name,
                username=username,
                email=email,
                password=password,
                date_joined=datetime.now(),
                updated_at=datetime.now(),
            )
        except Exception:
            raise ServiceUnavailable()

        response_serializer = response_serializer_class(data={
            "id": user.id,
        })
        response_serializer.is_valid()
        messages.success(request, 'Account created successfully. Please log in.')
        response = Response(response_serializer.data, status=status.HTTP_200_OK)
        response["cross-origin-opener-policy"] = "unsafe-none"
        response["referrer-policy"] = "no-referrer"
        return response
