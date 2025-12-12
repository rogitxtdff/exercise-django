# from django.urls import path
# from . import views  # این خط مهمه!

# urlpatterns = [
#     path('api/users/', views.user_list, name='user_list'),
#     path('api/users/<int:user_id>/', views.user_detail, name='user_detail'),
# ]

from django.urls import path
from .views import UserListView, UserDetailView

urlpatterns = [
    path('api/users/', UserListView.as_view(), name='user_list'),
    path('api/users/<int:user_id>/', UserDetailView.as_view(), name='user_detail'),
]