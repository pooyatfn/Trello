from rest_framework import serializers

from trello_user.models import TrelloUser
from .models import SubTask
from .models import Task


class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = '__all__'

    def to_representation(self, instance):
        rep = super().to_representation(instance)
        user_id = rep['assignee']
        rep['assignee_username'] = TrelloUser.objects.get(id=user_id).username
        return rep


class SubTaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = SubTask
        fields = '__all__'

    def to_representation(self, instance):
        rep = super().to_representation(instance)
        user_id = rep['assignee']
        rep['assignee_username'] = TrelloUser.objects.get(id=user_id).username
        return rep
