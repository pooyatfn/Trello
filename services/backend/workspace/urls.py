from django.urls import path

from .views import WorkspaceListCreateView, \
    WorkspaceRetrieveUpdateDeleteView  # , WorkspaceUsersListView, WorkspaceUsersAPIView

urlpatterns = [
    path('', WorkspaceListCreateView.as_view(), name='workspace-list-create'),
    path('<int:pk>/', WorkspaceRetrieveUpdateDeleteView.as_view(), name='workspace-detail'),
]
