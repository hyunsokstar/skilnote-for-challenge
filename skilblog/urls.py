from django.urls import path, re_path , include
from . import views
from django.contrib.auth import views as auth_views
from django.conf import settings

app_name = 'skilblog'

urlpatterns = [
    # 1122
    path('', views.SkilBlogTitleList.as_view() , name="SkilBlogTitleList"),
    path('my_skil_column', views.SkilBlogTitleListForMe.as_view() , name="SkilBlogTitleListForMe"),
    path('<int:id>', views.SkilBlogContentList , name="SkilBlogContentList"),
    path('delete_for_skil_column_title_list/<int:id>', views.delete_for_skil_column_title_list , name="delete_for_skil_column_title_list"),


    path('<int:id>/insert_mode', views.SkilBlogContentListForInsert , name="SkilBlogContentListForInsert"),
    path('new/summernote/<int:skil_blog_title_id>', views.createViewForSkillBlogContentUsingSummerNote.as_view() , name="createViewForSkillBlogContentUsingSummerNote"),
    path('insert_skil_column_content/<int:skil_blog_title_id>', views.CreateSkillBlogContentForInsertMode.as_view() , name="CreateSkillBlogContentForInsertMode"),

    path('modify_comment_for_sbt', views.modify_comment_for_sbt , name="modify_comment_for_sbt"),
    path('delete_comment_for_sbt', views.delete_comment_for_sbt , name="delete_comment_for_sbt"),
    path('insert_comment_for_sbt', views.insert_comment_for_sbt , name="insert_comment_for_sbt"),

    path('<int:id>/like_skil_blog_title', views.like_skil_blog_title , name="like_skil_blog_title"),
    path("skil_blog_title_list/<int:pk>/delete", views.delete_skil_blog_title_list.as_view(), name="delete_skilblog_title_list"),
    path("skil_blog_title_list/<int:pk>/modify", views.modify_skil_blog_title_list.as_view(), name="modify_skilblog_title_list"),
    path('modify_skilblog_content2_by_summernote/<int:pk>/', views.modify_skilblog_content2_by_summernote.as_view() , name='modify_skilblog_content2_by_summernote'),
    path('edit_skil_blog_for_content1/<int:id>', views.edit_skil_blog_for_content1 , name='edit_skil_blog_for_content1'),
    path('edit_skil_blog_for_content2/<int:id>', views.edit_skil_blog_for_content2 , name='edit_skil_blog_for_content2'),

    # edit_skil_blog_for_content1
    path('delete_sbc_content/<int:id>', views.delete_sbc_content , name="delete_sbc_content"),
    path('sbc_title_modify/<int:id>', views.sbc_modify , name="sbc_title_modify"),
    # 스킬 블로그의 상세 보기

]
