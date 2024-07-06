from rest_framework import serializers


class TrelloUserSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    first_name = serializers.CharField()
    last_name = serializers.CharField()
    username = serializers.CharField()
    email = serializers.EmailField()
    date_joined = serializers.DateTimeField()
    updated_at = serializers.DateTimeField()


class CreateUserSerializer(serializers.Serializer):
    first_name = serializers.CharField(required=False)
    last_name = serializers.CharField(required=False)
    username = serializers.CharField(allow_null=False)
    email = serializers.EmailField(allow_null=False)
    password = serializers.CharField(allow_null=False)


class CreateUserResponseSerializer(serializers.Serializer):
    id = serializers.IntegerField()


class ListUsersResponseSerializer(serializers.Serializer):
    total_users = serializers.IntegerField()
    users = TrelloUserSerializer(many=True)
