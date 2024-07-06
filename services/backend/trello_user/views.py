from rest_framework import generics
from rest_framework.generics import ListCreateAPIView

from .models import TrelloUser
from .serializers import TrelloUserSerializer


class UserListCreateView(ListCreateAPIView):
    serializer_class = TrelloUserSerializer
    queryset = TrelloUser.objects.all()


class TrelloUerRetrieveUpdateDeleteView(generics.RetrieveUpdateDestroyAPIView):
    queryset = TrelloUser.objects.all()
    serializer_class = TrelloUserSerializer
