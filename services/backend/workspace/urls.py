from django.urls import path

from .views import WorkspaceListCreateView, WorkspaceRetrieveUpdateDeleteView, WorkspaceUsersView

urlpatterns = [
    path('', WorkspaceListCreateView.as_view(), name='workspace-list-create'),
    path('<int:pk>/', WorkspaceRetrieveUpdateDeleteView.as_view(), name='workspace-detail'),
    path('workspaces/user/<int:user_id>/', WorkspaceUsersView.as_view(), name='workspaces-of-user'),
    # path('workspaces/<int:workspace_id>/users/add/', WorkspaceUsersView.as_view(), name='add_user_to_workspace'),
    # path('workspaces/<int:workspace_id>/users/update/', WorkspaceUsersView.as_view(), name='update_user_role'),
    # path('workspaces/<int:workspace_id>/users/remove/', WorkspaceUsersView.as_view(),
    #      name='remove_user_from_workspace'),
]
