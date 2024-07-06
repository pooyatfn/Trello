from rest_framework import serializers

from trello_user.models import TrelloUser
from .models import Workspace, WorkspaceMembership


class TrelloUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = TrelloUser
        fields = ['username']  # Customize as needed


class WorkspaceMembershipSerializer(serializers.ModelSerializer):
    is_admin = serializers.BooleanField()

    class Meta:
        model = WorkspaceMembership
        fields = ['user', 'is_admin']


class WorkspaceSerializer(serializers.ModelSerializer):
    users = WorkspaceMembershipSerializer(source='workspacemembership_set', many=True, read_only=True)

    class Meta:
        model = Workspace
        fields = ['id', 'name', 'description', 'created_at', 'updated_at', 'users']
