from rest_framework import serializers

from trello_user.models import TrelloUser
from .models import Workspace, WorkspaceMembership


class TrelloUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = TrelloUser
        fields = ['id', 'username']
        validators = []


class WorkspaceMembershipSerializer(serializers.ModelSerializer):
    username = serializers.CharField()

    class Meta:
        model = WorkspaceMembership
        fields = ['username', 'is_admin']
        validators = []

    def validate(self, attrs):
        return attrs


class WorkspaceSerializer(serializers.ModelSerializer):
    users = WorkspaceMembershipSerializer(many=True)

    class Meta:
        model = Workspace
        fields = ['id', 'name', 'description', 'created_at', 'updated_at', 'users']
        validators = []

    def to_representation(self, instance):
        rep = super().to_representation(instance)
        user_dicts = rep.get('users', [])
        for user_dict in user_dicts:
            username = user_dict['username']
            user = TrelloUser.objects.get(username=username)
            membership = WorkspaceMembership.objects.get(workspace=instance, user=user.id)
            user_dict['is_admin'] = membership.is_admin
        return rep

    def create(self, validated_data):
        users_data = validated_data['users']
        workspace_details = {
            'name': validated_data['name'],
            'description': validated_data['description']
        }
        workspace = Workspace.objects.create(**workspace_details)

        for user_data in users_data:
            username = user_data['username']
            is_admin = user_data['is_admin']

            try:
                user = TrelloUser.objects.get(username=username)
            except TrelloUser.DoesNotExist:
                raise serializers.ValidationError(f"A user with username '{username}' does not exist.")

            WorkspaceMembership.objects.create(workspace=workspace, user=user, is_admin=is_admin)

        return workspace
