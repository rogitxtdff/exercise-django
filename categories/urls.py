from django.urls import path
from .views import CategoryListView, CategoryDetailView

urlpatterns = [
    path('api/categories/', CategoryListView.as_view(), name='category_list'),
    path('api/categories/<int:category_id>/', CategoryDetailView.as_view(), name='category_detail'),
]