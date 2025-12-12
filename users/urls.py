

from django.urls import path
from .views import UserListView, UserDetailView

urlpatterns = [
    path('api/users/', UserListView.as_view(), name='user_list'),
    path('api/users/<int:user_id>/', UserDetailView.as_view(), name='user_detail'),
]