from django.urls import path, re_path , include
from . import views, views_cbv

from django.contrib.auth import views as auth_views
from django.conf import settings

app_name = 'management'

urlpatterns = [
    path('suggestion/list', views_cbv.SuggestionListView.as_view() , name="suggestion_list"),
    path('suggestion/new/',views.suggestion_new , name ="suggestion_new"),

    path('suggestion/<int:pk>/delete', views_cbv.SuggestionDeleteView.as_view(), name='suggestion_delete'),
    
    path('suggestion/<int:pk>/update', views_cbv.SuggestionUpdateView.as_view(), name='suggestion_update'),
    path('<int:id>/recommand_suggestion/', views.recommand_suggestion, name="recommand_suggestion"),

]
