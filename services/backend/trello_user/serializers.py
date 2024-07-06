from rest_framework import serializers
from .models import TrelloUser


class TrelloUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = TrelloUser
        fields = ['first_name', 'last_name', 'username', 'email', 'banner', 'avatar', 'bio']  # Customize as needed
