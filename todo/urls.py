from django.contrib import admin
from django.urls import path, include
from . import views


app_name= 'todo'
urlpatterns = [

    # 할 일(미완료 ) 리스트 출력
    path('', views.TodoList.as_view() , name="todo_list"),

    # 할 일 (완료) 리스트 출력
    path('todolist/complete/me/', views.TodoCompleteListByMe.as_view() , name="todo_complete_list_byme"),

    # todolist detail popup 출력
    path('<int:pk>/', views.todoDetail.as_view(), name='todo_detail'),


    path('team_todo_list/pass_task_to_selected_user/', views.pass_task_to_selected_user, name="pass_task_to_selected_user"),

    path('add_todo_by_ajax/', views.add_todo_by_ajax, name="add_todo_by_ajax"),
    path('add_todo_for_team_by_ajax/', views.add_todo_for_team_by_ajax, name="add_todo_for_team_by_ajax"),
    path('add_todo_by_ajax_by_teamleader/', views.add_todo_by_ajax_by_teamleader, name="add_todo_by_ajax_by_teamleader"),

    path('team_info_list/', views.TeamInfoListView.as_view() , name="TeamInfoListView"),

    path('team_todo_list/<str:team_name>', views.team_todo_list , name="team_todo_list"),
    path('team_todo_list_by_check_user/<str:team_name>', views.team_todo_list_by_check_user , name="team_todo_list_by_check_user"),

    path('TeaminfoCreate/', views.TeamInfoCreateView.as_view() , name="create_team_info"),
    # 팀 리스트 삭제
    path('team_info_list/delete/teaminfo/<int:team_id>', views.delete_team_info , name="delete_team_info"),
    path('<int:id>/edit/', views.todo_edit, name='todo_edit'),
    path('<int:pk>/delete/', views.todo_delete, name='todo_delete'),
    path('new/',views.todo_new , name ="todo_new"),
    path('search/<str:q>/', views.TodoSearch.as_view()),
    path('card', views.TodoList_by_card.as_view() , name="todo_list_by_card"),

    path('complete_bycard/', views.TodoListByComplete_by_card.as_view() , name="todo_complete_list_by_card"),
    # path('<int:pk>/new_comment/summer_note', views.new_comment_summer_note),
    path('<int:pk>/new_comment_by_summer_note', views.new_comment_by_summer_note, name="new_comment_by_summer_note"),

    path('<int:pk>/new_comment/text_area', views.new_comment_text_area),
    path('edit_comment/<int:pk>/', views.CommentUpdate.as_view(), name="edit_url"),
    path('delete_comment/<int:pk>/', views.delete_comment, name="delete_url"),
    path('<int:id>/todo_complete/',views.todo_complete , name ="todo_complete"),
    path('<int:id>/todo_help/', views.todo_help, name="todo_help"),
    path('<int:id>/todo_help_cancle/', views.todo_help_cancle, name="todo_help_cancle"),
    path('category/<str:slug>/', views.TodoListByCategory.as_view() , name="total_ucomplete_todo_list"),
    path('todolist/admin/', views.TodoListByAdmin.as_view() , name="todo_list_by_admin"),
    path('todolist/admin/insert_popup/<str:user_name>', views.isnert_todo_popup_by_admin , name="isnert_todo_popup_by_admin"),


    path('todolist/complete/me/todo_delete_ajax/', views.todo_delete_ajax , name="todo_delete_ajax"),
    path('todolist/uncomplete/me', views.TodoUnCompleteListByMe.as_view() , name="todo_uncomplete_list_byme"),
    path('completeList/total/', views.TodoListByComplete_total.as_view() , name="todo_complete_list_total"),

    path('update_comment_ajax/summernote/<int:id>', views.update_comment_ajax_for_summernote , name='update_comment_ajax'),
    path('update_comment_ajax/textarea/<int:id>', views.update_comment_ajax_for_textarea , name='update_comment_ajax'),


    path('delete_comment_ajax/<int:id>', views.delete_comment_ajax , name='delete_comment_ajax'),
    path('<int:pk>/update/', views.CommentUpdate.as_view()),
    path('new/admin/<str:user_name>/<str:leader_name>/',views.todo_new_admin, name ="todo_new_admin"),
    path('status/',views.todo_status_list, name ="todo_status_list"),
    path('todo_delete_ajax/',views.todo_delete_ajax, name ="todo_delete_ajax"),
    path('todolist/uncomplete/<str:user_id>/',views.UncompleteTodoListByUserId.as_view(), name ="TodoListByUserId"),
    path('todolist/complete/<str:user_id>/',views.CompleteTodoListByUserId.as_view(), name ="TodoListByUserId"),

    path('todolist/uncomplete/admin/<str:user_id>/<str:team_leader_name>',views.UncompleteTodoListByUserId_admin.as_view(), name ="todolist_by_user_complete"),
    path('todolist/complete/admin/<str:user_id>/<str:team_leader_name>',views.CompleteTodoListByUserId_admin.as_view(), name ="todolist_by_user_uncomplete"),

    # team
    path('team_register/', views.team_register , name='team_register'),
    path('withdrawl_team/', views.withdrawl_team , name='withdrawl_team'),
    path('team_member_list/<int:team_info_id>/delete/team/memeber', views.delete_team_member, name='delete_team_member'),
    path('delete/team/memeber/byajax', views.delete_team_memeber_info_by_memberId, name="delete_team_memeber_info_by_memberId"),

    path('team_member_list/<int:team_info_id>', views.team_member_list_view.as_view() , name="team_member_list"),



]
