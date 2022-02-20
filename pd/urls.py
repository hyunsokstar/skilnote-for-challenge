from django.urls import path, re_path , include
from . import views
from django.contrib.auth import views as auth_views
from django.conf import settings

app_name = 'pd'

urlpatterns = [
    path('private_task_list/', views.private_task_list.as_view() , name="private_task_list"),
    path('my_task/new/',views.mytask_new , name ="mytask_new"),
    path('delete_mytask_by_ajax/',views.delete_mytask_by_ajax , name ="delete_mytask_by_ajax"),
    path('update_mytask_by_ajax/',views.update_mytask_by_ajax , name ="update_mytask_by_ajax"),
    #
    # path('add_mysite_by_ajax/',views.add_mysite_by_ajax , name ="add_mysite_by_ajax"),
    # path('update_mysite_by_ajax/',views.update_mysite_by_ajax , name ="update_mysite_by_ajax"),
    # path('delete_mysite_by_ajax/',views.delete_mysite_by_ajax , name ="delete_mysite_by_ajax"),

]
