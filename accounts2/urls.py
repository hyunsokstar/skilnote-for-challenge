from django.urls import path, re_path, include
from . import views
from django.contrib.auth import views as auth_views , logout as auth_logout
from . import forms
from django.contrib.auth.views import LoginView


app_name = 'accounts2'

urlpatterns = [
    path('like_or_unlike', views.like_or_unlike, name="like_or_unlike"),
    path('logout', views.Logout, name="logout"),
    # path('login/', views.LoginView.as_view(template_name="login.html" , authentication_form= "forms.LoginForm"), name = 'login'),
    path('delete_for_my_favorite_user', views.delete_for_my_favorite_user, name="delete_for_my_favorite_user"),
    path('delete_for_liker_user_for_me', views.delete_for_liker_user_for_me, name="delete_for_liker_user_for_me"),

    path('signup/', views.signup, name='signup'),
    path('member_list/', views.member_list, name='member_list'),
    path('my_profile_information_view/', views.my_profile_information_view.as_view(), name = 'my_profile_information_view'),
    path('update_for_profile/<int:id>', views.update_for_profile , name='update_for_profile'),

    # 참고 wm MyShortcutListByUser
    path('user_profile_information_view/<str:user>', views.user_profile_information_view, name="user_profile_information_view"),
    path('delete_login_user/', views.delete_login_user, name="delete_login_user"),



]
