from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import TaskViewSet, SubTaskViewSet

router = DefaultRouter()
router.register(r'workspaces/(?P<workspaceId>\d+)/tasks', TaskViewSet, basename='task')
router.register(r'tasks/(?P<taskId>\d+)/subtasks', SubTaskViewSet, basename='subtask')

urlpatterns = [
    path('', include(router.urls)),
]
