from django.urls import path

from .views import UserListCreateView, TrelloUerRetrieveUpdateDeleteView, UserTasksView

urlpatterns = [
    path('', UserListCreateView.as_view(), name='user-list-create'),
    path('<int:pk>/', TrelloUerRetrieveUpdateDeleteView.as_view(), name='trello-user-detail'),
    path('tasks', UserTasksView.as_view(), name='user-list-create'),
]
