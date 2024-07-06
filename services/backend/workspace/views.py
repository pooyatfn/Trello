from rest_framework import generics

from .models import Workspace
from .serializers import WorkspaceSerializer


class WorkspaceListCreateView(generics.ListCreateAPIView):
    queryset = Workspace.objects.all()
    serializer_class = WorkspaceSerializer


class WorkspaceRetrieveUpdateDeleteView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Workspace.objects.all()
    serializer_class = WorkspaceSerializer
