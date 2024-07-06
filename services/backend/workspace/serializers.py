# workspaces/serializers.py

from rest_framework import serializers

from trello_user.models import TrelloUser
from .models import Workspace, WorkspaceMembership


class TrelloUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = TrelloUser
        fields = ['username']  # Customize as needed


class WorkspaceMembershipSerializer(serializers.ModelSerializer):
    user = TrelloUserSerializer()

    class Meta:
        model = WorkspaceMembership
        fields = ['user', 'is_admin']


class WorkspaceSerializer(serializers.ModelSerializer):
    users = WorkspaceMembershipSerializer(many=True, read_only=True, source='workspace_membership')

    class Meta:
        model = Workspace
        fields = ['id', 'name', 'description', 'created_at', 'updated_at', 'users']