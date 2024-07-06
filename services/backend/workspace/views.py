from rest_framework import generics
from rest_framework import status
from rest_framework.response import Response

from trello_user.models import TrelloUser
from .models import Workspace, WorkspaceMembership
from .serializers import WorkspaceSerializer


class WorkspaceListCreateView(generics.ListCreateAPIView):
    queryset = Workspace.objects.all()
    serializer_class = WorkspaceSerializer

    # def get(self, request, *args, **kwargs):
    #     # Retrieve workspace users and their admin status
    #     workspaces = []
    #     users_with_admin_status = []
    #     for workspace in self.get_queryset():
    #         for membership in workspace.workspacemembership_set.all():
    #             users_with_admin_status.append({
    #                 'user': membership.user.username,
    #                 'is_admin': membership.is_admin
    #             })
    #         workspace['users'] = users_with_admin_status
    #         workspaces.append(workspace)
    #
    #     # Serialize the workspace data
    #     serializer = self.get_serializer()
    #     response_data = serializer.data
    #     response_data['users'] = users_with_admin_status
    #
    #     return Response(workspaces)


class WorkspaceRetrieveUpdateDeleteView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Workspace.objects.all()
    serializer_class = WorkspaceSerializer

    def update(self, request, *args, **kwargs):
        # Get the workspace instance
        workspace = self.get_object()

        # Handle updating workspace fields (e.g., name, description)
        workspace.name = request.data.get('name', workspace.name)
        workspace.description = request.data.get('description', workspace.description)
        workspace.save()

        # Handle adding/removing users (use request.data['users'])
        usernames = request.data.get('users', [])
        for username in usernames:
            try:
                user = TrelloUser.objects.get(username=username)
                membership, created = WorkspaceMembership.objects.get_or_create(
                    user=user,
                    workspace=workspace,
                    defaults={'is_admin': False}
                )
                # If the membership was created, user added/updated
            except TrelloUser.DoesNotExist:
                return Response(
                    {'error': f"User with username '{username}' does not exist."},
                    status=status.HTTP_400_BAD_REQUEST
                )

        # return Response({'message': 'Users added/updated successfully.'}, status=status.HTTP_200_OK)

        return Response({'message': 'Workspace updated successfully.'}, status=status.HTTP_200_OK)

    # def destroy(self, request, *args, **kwargs):
    #     # Handle deleting workspace
    #     # ...
    #
    #     return Response({'message': 'Workspace deleted successfully.'}, status=status.HTTP_204_NO_CONTENT)
