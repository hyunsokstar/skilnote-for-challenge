from django.urls import path, re_path , include
from . import views
from django.contrib.auth import views as auth_views
from django.conf import settings

app_name = 'skilnote4'

urlpatterns = [
    # 1122
    path('', views.SkilNoteListView.as_view() , name="my_shortcut_list"),
    path('myshortcut/search_skil_note_for_me/', views.search_skil_note_for_me.as_view() , name="search_skil_note_for_me"),
    path('myshortcut/search_skil_note_for_all/', views.search_skil_note_for_all.as_view() , name="search_skil_note_for_all"),
    path('myshortcut/search_skilnote_by_file_name_for_me/', views.search_skilnote_by_file_name_for_me.as_view() , name="search_skilnote_by_file_name_for_me"),
    path('myshortcut/search_skilnote_by_file_name_for_all/', views.search_skilnote_by_file_name_for_all.as_view() , name="search_skilnote_by_file_name_for_all"),



    path('myshortcut/', views.SkilNoteListView.as_view() , name="my_shortcut_list"),
    path('myshortcut2/', views.MyShortCutListView2.as_view() , name="my_shortcut_list2"),

    path('myshortcut/insert_temp_skill_note_for_textarea/', views.insert_temp_skill_note_for_textarea , name="insert_temp_skill_note_for_textarea"), # mini note insert front
    path('myshortcut/insert_for_guest_book/', views.insert_for_guest_book , name="insert_for_guest_book"), # geust book insert
    path('myshortcut/guest_book_list/<str:guest_book_owner>', views.guest_book_list, name ="guest_book_list"), # guest_book_list
    path('myshortcut/delete_guest_book_list/<int:id>', views.delete_guest_book_list , name="delete_guest_book_list"),

    path('myshortcut/delete_comment_for_skilpage/<int:id>', views.delete_comment_for_skilpage , name="delete_comment_for_skilpage"),

    path('myshortcut/temp_skill_list_for_backend/<page_user>', views.temp_skill_list_for_backend2 , name="temp_skill_list_for_backend"),
    path('myshortcut/temp_skill_list/<page_user>', views.temp_skill_list2 , name="temp_skill_list"), # mininote for frontend

    path('myshortcut/temp_skill_list_for_backend', views.temp_skill_list_for_backend1 , name="temp_skill_list_for_backend"),
    path('myshortcut/temp_skill_list', views.temp_skill_list1 , name="temp_skill_list"), # mininote for frontend

    path('myshortcut/temp_skill_list_for_backend/', views.temp_skill_list_for_backend1 , name="temp_skill_list_for_backend"),
    path('myshortcut/temp_skill_list/', views.temp_skill_list1 , name="temp_skill_list"), # mininote for frontend


    path('new_comment_for_skilpage/<str:user_name>/<str:category_id>/' , views.new_comment_for_skilpage, name="new_comment_for_skilpage"),

    path('manual', views.manualPage, name="manual"),

    path('myshortcut/update_skil_note_file_name/<int:id>', views.update_skil_note_file_name , name="update_skil_note_file_name"),


    path('myshortcut/category_plus_1_for_current_user', views.category_plus_1_for_current_user , name='category_plus_1_for_current_user'),
    path('myshortcut/category_minus_1_for_current_user', views.category_minus_1_for_current_user , name='category_minus_1_for_current_user'),

    path('myshortcut/move_to_skil_blog/', views.move_to_skil_blog , name='move_to_skil_blog'),

    path('myshortcut/copy_to_me_from_user_id/', views.copy_to_me_from_user_id , name='copy_to_me_from_user_id'),
    path('myshortcut/plus_recommand_for_skillnote_user/', views.plus_recommand_for_skillnote_user , name='plus_recommand_for_skillnote_user'),

    path('myshortcut/edit_complete_skill_note_for_front_end/<int:id>', views.edit_complete_skill_note_for_front_end , name='edit_complete_skill_note_for_front_end'),

    path('myshortcut/edit_complete_skill_note_for_backend/<int:id>', views.edit_complete_skill_note_for_backend , name='edit_complete_skill_note_for_backend'),


    path('myshortcut/edit_temp_skill_note_using_textarea_for_backend/<int:id>', views.edit_temp_skill_note_using_textarea_for_backend , name='edit_temp_skill_note_using_textarea_for_backend'),

    path('myshortcut/edit_temp_skill_note_using_input_for_backend/<int:id>', views.edit_temp_skill_note_using_input_for_backend , name='edit_temp_skill_note_using_input_for_backend'),

    path('myshortcut/update_temp_skil_title_for_backend/<int:id>', views.update_temp_skil_title_for_backend , name="update_temp_skil_title_for_backend"),
    path('myshortcut/delete_temp_skill_note_for_backendarea/<int:id>', views.delete_temp_skill_note_for_backendarea , name="delete_temp_skill_note_for_backendarea"),
    path('myshortcut/insert_temp_skill_note_using_input_for_backend/', views.insert_temp_skill_note_using_input_for_backend , name="insert_temp_skill_note_using_input_for_backend"),
    path('myshortcut/insert_temp_skill_note_using_textarea_for_backend/', views.insert_temp_skill_note_using_textarea_for_backend , name="insert_temp_skill_note_using_textarea_for_backend"),

    path('myshortcut/insert_temp_skill_note_for_input/', views.insert_temp_skill_note_for_input , name="insert_temp_skill_note_for_input"),
    path('myshortcut/edit_temp_skill_note_for_input/<int:id>', views.edit_temp_skill_note_for_input , name='edit_temp_skill_note_for_input'),

    path('myshortcut/update_temp_skill_note_for_textarea/<int:id>', views.update_temp_skill_note_for_textarea , name='update_temp_skill_note_for_textarea'),

    path('myshortcut/update_temp_skil_title/<int:id>', views.update_temp_skil_title , name="update_temp_skil_title"),
    path('myshortcut/delete_temp_memo_by_ajax/<int:id>', views.delete_temp_memo_by_ajax , name="delete_temp_memo_by_ajax"),


    path('myshortcut/search_by_id_and_word/' , views.searchSkilNoteViewByIdAndWord.as_view(), name="search_by_id_and_word"),

    path('myshortcut/copyForCategorySubjectToMyCategory/' , views.copyForCategorySubjectToMyCategory, name="copyForCategorySubjectToMyCategory"),

    path('new_comment_for_my_shortcut/<int:shortcut_id>/ajax/' , views.new_comment_for_my_shortcut, name="new_comment_for_my_shortcut"),
    path('update_shortcut_comment_ajax/<int:shortcut_comment_id>' , views.update_comment_for_my_shortcut, name="update_comment_for_my_shortcut"),
    path('delete_shortcut_comment_ajax/<int:shortcut_comment_id>' , views.delete_comment_for_my_shortcut, name="delete_comment_for_my_shortcut"),

    path('myshortcut/update/shortcut_subject/' , views.update_my_shortcut_subject, name="update_my_shortcut_subject"),

    # path('myshortcut/create_new1_input/ajax/first', views.create_new1_input_first , name="create_new1_input_first"),
    # path('myshortcut/create_new2_textarea_first/ajax/', views.create_new2_textarea_first , name="create_new2_textarea_first"),
    # path('myshortcut/create_summernote_first/ajax/', views.create_summernote_first , name="create_summernote_first"),
    path('myshortcut/create_input_first/', views.create_input_first , name="create_new1_input_first"),
    path('myshortcut/create_textarea_first/', views.create_textarea_first , name="create_new2_textarea_first"),
    path('myshortcut/create_summernote_first/', views.create_summernote_first , name="create_summernote_first"),
    path('myshortcut2/create_input_first/', views.create_input_first , name="create_new1_input_first"),
    path('myshortcut2/create_textarea_first/', views.create_textarea_first , name="create_new2_textarea_first"),
    path('myshortcut2/create_summernote_first/', views.create_summernote_first , name="create_summernote_first"),


    path('myshortcut/create_new1_input/ajax/', views.create_new1_input , name="create_new1_input"),

    path('myshortcut/create_new1_input_between/ajax/<int:current_article_id>', views.create_new1_input_between , name="create_new1_input_between"),

    path('myshortcut/create_new2_textarea/ajax/', views.create_new2_textarea , name="create_new2_textareas"),



    path('myshortcut/create_new2_textarea_between/ajax/<int:current_article_id>', views.create_new2_textarea_between , name="create_new2_textarea_between"),


    # path('myshortcut/create_new4_textarea/ajax/', views.create_new4_textarea , name="create_new4_textareas"),

    path('myshortcut/update/category/nick/', views.update_shortcut_nick , name="update_category_nick"),
    path('myshortcut/update/category_nick_by_author/', views.update_shortcut_nick2 , name="update_category_nick2"),

    path('new/input', views.MyShortCutCreateView_input.as_view() , name="insert_myshortcut_input"),
    path('new/input_title/', views.MyShortCutCreateView_image.as_view() , name="MyShortCutCreateView_image"),

    path('new/textarea', views.MyShortCutCreateView_textarea.as_view() , name="insert_myshortcut_textarea"),
    path('new/textarea_summer_note', views.CreateSkilNoteBySummerNote.as_view() , name="insert_myshortcut_textarea_summer_note"),
    path('myshortcut/createSkilNoteForInsertMode/', views.createSkilNoteForInsertMode.as_view() , name="createSkilNoteForInsertMode"),

    path('new/textarea_summer_note_through/<int:current_article_id>', views.SkilNoteCreateView_summernote_through.as_view() , name="SkilNoteCreateView_summernote_through"),
    path('new/textarea_summer_note_through2/<int:current_article_id>', views.SkilNoteCreateView_summernote_through2.as_view() , name="SkilNoteCreateView_summernote_through2"),


    path('new/SkilNoteCreateView_image_through/<int:current_article_id>', views.SkilNoteCreateView_image_through.as_view() , name="SkilNoteCreateView_image_through"),

    path('myshortcut/delete_shortcut_ajax/<int:id>', views.delete_shortcut_ajax , name="delete_shortcut_ajax"),
    path('myshortcut/update_shortcut_ajax/<int:id>', views.update_shortcut_ajax , name="update_shortcut_ajax"),

    path('myshortcut/category/<str:slug>/', views.MyShortcutListByCategory.as_view()),
    path('myshortcut2/category/<str:slug>/', views.MyShortcutListByCategory2.as_view()),
    path('myshortcut/update_shortcut1_ajax/<int:id>', views.update_shortcut1_ajax , name='update_shortcut1_ajax'),

    path('myshortcut/update_shortcut2_ajax/<int:id>', views.update_shortcut2_ajax , name='update_shortcut2_ajax'),

    path('update/shortcut_id_ajax/<int:id>', views.update_shorcut_id_for_user , name="update_shorcut_id_for_user"),

        path('myshortcut/update_skilnote_by_summernote/<int:pk>/', views.update_skilnote_by_summernote.as_view() , name='update_skilnote_by_summernote'),
    path('myshortcut/modify_myshortcut_by_summer_note2/<int:pk>/', views.modify_myshortcut_by_summer_note2.as_view() , name='modify_myshortcut_by_summer_note2'),


    # user_id로 shortcut nick list 출력
    path('myshorcut/nicklist/<str:user_name>/', views.CategoryNickListByUserId , name='category_nick_list'),
    path('myshorcut/nicklist_for_user/<str:user_name>/', views.CategoryNickListByUserId_for_user , name='CategoryNickListByUserId_for_user'),

    # 유저 리스트 출력 for memo
    # path('userlist/byajax', views.user_list_for_memo, name = 'user_list_for_memo'),
    path('userlist/byajax', views.user_list_for_memo_view.as_view(), name = 'user_list_for_memo'),
    path('favorite_user_list/byajax', views.favorite_user_list_for_skillnote, name = 'favorite_ user_list_for_memo'),



    path('myshortcut/delete/ajax/', views.delete_myshortcut_by_ajax, name = 'delete_myshortcut_by_ajax'),
    path('myshortcut/update/category/ajax', views.update_category_by_ajax, name = 'update_category_by_ajax'),

    path('myshortcut/<str:user>/<int:category_id>', views.MyShortcutListByUser.as_view(), name="skil_note_list_by_user"),

]
