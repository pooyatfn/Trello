from rest_framework import viewsets
from rest_framework.permissions import AllowAny

from .models import Task, SubTask
from .serializers import TaskSerializer, SubTaskSerializer


class TaskViewSet(viewsets.ModelViewSet):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    permission_classes = [AllowAny]

    def get_queryset(self):
        workspace_id = self.kwargs['workspaceId']
        return Task.objects.filter(workspace__id=workspace_id)

    def perform_create(self, serializer):
        workspace_id = self.kwargs['workspaceId']
        serializer.save(workspace_id=workspace_id)


class SubTaskViewSet(viewsets.ModelViewSet):
    queryset = SubTask.objects.all()
    serializer_class = SubTaskSerializer
    permission_classes = [AllowAny]

    def get_queryset(self):
        task_id = self.kwargs['taskId']
        return SubTask.objects.filter(task__id=task_id)

    def perform_create(self, serializer):
        task_id = self.kwargs['taskId']
        serializer.save(task_id=task_id)
