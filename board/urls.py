# 앱 url.py 만들기
from django.urls import path, re_path , include
from . import views
from django.contrib.auth import views as auth_views
from django.conf import settings

app_name = 'board'

urlpatterns = [
    path('', views.ManualListView , name="manual_list"),
    path('<int:pk>/', views.ManualDetailView.as_view(), name='manual_detail'),
    path('new', views.ManualCreateView.as_view(), name="insert_manual"),
    path('delete_manual/<int:pk>', views.delete_manual , name='delete_manual'),
    path('edit_manual/<int:pk>/', views.ManulUpdate.as_view() , name = "edit_manual"),
]
