from django.urls import path, re_path , include
from . import views
from django.contrib.auth import views as auth_views
from django.conf import settings

app_name = 'challenge'

urlpatterns = [

    path('', views.ChallengeSubjectList.as_view() , name="challenge_subject_list"),
    path('delete_challenge_subject_by_id/<int:id>', views.delete_challenge_subject_by_id , name="delete_challenge_subject_by_id"),

    # 챌린지 대주제 입력 Create_Challenge_View
    path('Create_Challenge_View', views.CreateChallengeSubjectView.as_view() , name="CreateChallengeSubjectView"),
    path('update_challenge_subject/<int:pk>/', views.update_challenge_subject.as_view() , name='update_challenge_subject'),

    path('lecinfo/<int:pk>/delete', views.LecInfoDeleteView.as_view(), name='LecInfoDeleteView'),

    path ('<int:classification>', views.ParticipantsListForLectureView.as_view (), name="lec_record_list"),

    path('challenge_list/', views.challenge_list , name="challenge_list"),

    # path('<int:classification>', views.ParticipantsListForLectureView.as_view() , name="lec_record_list"),

	path('lecinfo_list/<str:challenge_title>', views.lecinfo_list_for_challenge, name="lecinfo_list_for_challenge"),
    # path('lecinfo_list', views.LecInfoListView.as_view() , name="lecinfo_list"),

    path('record/new/<int:classification>',views.CreateRecordView_11.as_view(), name ="네임"),
    path('lecinfo/new/<str:challenge_title>', views.CreatelecInfo.as_view() , name="CreatelecInfo"),
    # path('lec_info/new/',views.CreatelecInfo.as_view(), name ="create_lec_info"),

    path('record/delete/<int:pk>/<int:classification>', views.RecordDeleteView.as_view(), name='student_record_delete'),
    path('record/modify/<int:pk>/<int:classification>', views.RecordUpdateView.as_view(), name='student_record_update'),

    path('lec_info_update/<int:pk>/<int:classification>', views.LecInfoUpdateView.as_view(), name='lec_info_update'),

    path('<int:id>/recommand_lecture/', views.recommand_lecture, name="recommand_lecture"),
    path('like_or_unlike_for_challenge_subject', views.like_or_unlike_for_challenge_subject, name="like_or_unlike_for_challenge_subject"),



]
