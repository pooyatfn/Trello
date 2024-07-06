from rest_framework import serializers

from trello_user.models import TrelloUser
from .models import Workspace, WorkspaceMembership


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

    def to_representation(self, instance):
        rep = super().to_representation(instance)
        for user_dict in rep['users']:
            user_id = user_dict['user']
            user = TrelloUser.objects.get(id=user_id)
            user_dict['username'] = user.username
        return rep
