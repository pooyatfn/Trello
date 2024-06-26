from django.contrib import messages
from drf_spectacular.types import datetime
from drf_spectacular.utils import extend_schema, OpenApiParameter
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
        return Response(response_serializer.data, status=status.HTTP_200_OK)

    @extend_schema(
        parameters=[
            OpenApiParameter(name='first_name', type=str, description='First name of user', default=None),
            OpenApiParameter(name='last_name', type=str, description='Last name of user'),
            OpenApiParameter(name='username', type=str, description='Username of user, must be unique', required=True),
            OpenApiParameter(name='email', type=str, description='Email of user, must be unique', required=True),
            OpenApiParameter(name='password', type=str, description='Password of user', required=True),
        ],
        responses={200: CreateUserResponseSerializer},
    )
    def post(self, request):
        serializer = CreateUserSerializer(data=request.query_params)
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
        return Response(response_serializer.data, status=status.HTTP_200_OK)
