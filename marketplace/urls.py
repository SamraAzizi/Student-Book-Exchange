from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('post/', views.post_item, name='post_item'),
    path('items/', views.all_items, name='all_items'),
    path('item/<int:pk>/', views.item_detail, name='item_detail'),
    path('search-ajax/', views.search_ajax, name='search_ajax'),
]