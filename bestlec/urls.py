from django.urls import path, re_path , include
from . import views
from django.contrib.auth import views as auth_views
from django.conf import settings

app_name = 'bestlec'

urlpatterns = [
    path('', views.Best20List.as_view() , name="best20_list"),
    path('<int:id>/grade_plus/', views.grade_plus, name="request_grade_plus"),
    path('new/',views.bestlec_new , name ="bestlec_new"),
    path('<int:id>/finisherlist', views.FinisherList , name="FinisherList"),
    path('<int:bl_pk>/finisher/new', views.FinisherCreateView.as_view(), name="finisher_new"),
    path('<int:id>/recommand_lecture/', views.recommand_lecture, name="recommand_lecture"),

    path('<int:pk>/delete/', views.best20_delete, name='best20_delete'),
    path('<int:pk>/finisher/delete/', views.finisher_delete, name='finisher_delete'),

]
