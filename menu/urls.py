from django.urls import path
from .views import MenuItemListView, MenuItemDetailView

urlpatterns = [
    path('api/menu/', MenuItemListView.as_view(), name='menu_list'),
    path('api/menu/<int:menuitem_id>/', MenuItemDetailView.as_view(), name='menu_detail'),
]