from django.contrib import admin
from django_summernote.admin import SummernoteModelAdmin
from . models import StudentRecord, LecInfo, RecommandLecInfo, challenge_subject


@admin.register(challenge_subject)
class ChallengeSubjectAdmin(admin.ModelAdmin):
    list_display = ['id','image', 'title','description','leader']

@admin.register(RecommandLecInfo)
class RecommandLecInfoAdmin(admin.ModelAdmin):
    list_display = ['id', 'lecinfo','author']

@admin.register(LecInfo)
class LecInfoAdmin(admin.ModelAdmin):
    list_display = ['id', 'lec_name','manager', 'lec_url', 'git_url' , 'lec_reputation','student_count']

@admin.register(StudentRecord)
class StudentRecordAdmin(admin.ModelAdmin):
    list_display = ['id', 'author','current_class','github_url', 'created']
