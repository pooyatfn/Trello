from django.urls import path

from .views import UserListCreateView, TrelloUerRetrieveUpdateDeleteView

urlpatterns = [
    path('', UserListCreateView.as_view(), name='user-list-create'),
    path('<int:pk>/', TrelloUerRetrieveUpdateDeleteView.as_view(), name='trello-user-detail'),
]
