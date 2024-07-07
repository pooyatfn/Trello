from rest_framework import serializers

from task.models import Task
from .models import TrelloUser


class TrelloUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = TrelloUser
        fields = ['id', 'first_name', 'last_name', 'username', 'email', 'banner', 'avatar', 'bio']


class ListUserTasksQuerySerializer(serializers.ModelSerializer):

    class Meta:
        model = Task
        fields = '__all__'
