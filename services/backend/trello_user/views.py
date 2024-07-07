from django.http import JsonResponse
from drf_spectacular.utils import extend_schema, OpenApiParameter
from rest_framework import generics
from rest_framework.generics import ListCreateAPIView
from rest_framework.permissions import AllowAny
from rest_framework.views import APIView

from .models import TrelloUser
from .serializers import TrelloUserSerializer, ListUserTasksQuerySerializer


class UserListCreateView(ListCreateAPIView):
    serializer_class = TrelloUserSerializer
    queryset = TrelloUser.objects.all()
    permission_classes = [AllowAny]


class TrelloUerRetrieveUpdateDeleteView(generics.RetrieveUpdateDestroyAPIView):
    queryset = TrelloUser.objects.all()
    serializer_class = TrelloUserSerializer
    permission_classes = [AllowAny]


class UserTasksView(APIView):
    permission_classes = [AllowAny]

    @extend_schema(
        parameters=[
            OpenApiParameter(name='user_id', type=int, description='ID of the user', required=True),
        ],
    )
    def get(self, request, *args, **kwargs):
        user_id = request.query_params['user_id']
        # request
        try:
            user = TrelloUser.objects.get(id=user_id)
            tasks = user.get_tasks()

            # Convert the tasks to JSON
            tasks_json = [{
                'id': task.id,
                'title': task.title,
                'status': task.status,
                'due_date': task.due_date.isoformat(),
                'priority': task.priority,
                'workspace': {'id': task.workspace.id, 'name': task.workspace.name}
            } for task in tasks]

            return JsonResponse(tasks_json, safe=False)
        except TrelloUser.DoesNotExist:
            return JsonResponse({'error': 'User not found'}, status=404)
