from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from rest_framework import generics
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from trello_user.models import TrelloUser
from .models import Workspace, WorkspaceMembership
from .serializers import WorkspaceSerializer


class WorkspaceListCreateView(generics.ListCreateAPIView):
    queryset = Workspace.objects.all()
    serializer_class = WorkspaceSerializer
    permission_classes = [AllowAny]


class WorkspaceRetrieveUpdateDeleteView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Workspace.objects.all()
    serializer_class = WorkspaceSerializer
    permission_classes = [AllowAny]


class WorkspaceUsersView(APIView):
    permission_classes = [AllowAny]

    def get(self, request, workspace_id):
        workspace = get_object_or_404(Workspace, pk=workspace_id)
        users = workspace.users.all()
        return Response([{
            'id': user.id,
            'username': user.username,
            'is_admin': True if user.is_admin else False
        } for user in users])

    def post(self, request, workspace_id):
        workspace = get_object_or_404(Workspace, pk=workspace_id)
        user_data = request.POST
        username = user_data.get('username')
        is_admin = user_data.get('is_admin', False)
        try:
            user = TrelloUser.objects.get(username=username)
        except TrelloUser.DoesNotExist:
            return JsonResponse({'error': 'User not found'}, status=404)
        WorkspaceMembership.objects.create(workspace=workspace, user=user, is_admin=is_admin)
        return JsonResponse({'message': 'User added successfully'})

    def put(self, request, workspace_id, user_id):
        workspace = get_object_or_404(Workspace, pk=workspace_id)
        user = get_object_or_404(TrelloUser, pk=user_id)
        is_admin = request.POST.get('is_admin', False)
        membership, _ = WorkspaceMembership.objects.get_or_create(workspace=workspace, user=user)
        membership.is_admin = is_admin
        membership.save()
        return JsonResponse({'message': 'Role updated successfully'})

    def delete(self, request, workspace_id, user_id):
        workspace = get_object_or_404(Workspace, pk=workspace_id)
        user = get_object_or_404(TrelloUser, pk=user_id)
        membership = get_object_or_404(WorkspaceMembership, workspace=workspace, user=user)
        membership.delete()
        return JsonResponse({'message': 'User removed successfully'})
