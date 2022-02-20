from django.db import models
from django.contrib.auth.models import User
from django.conf import settings



# Create your models here.
class Profile(models.Model):
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name='profile')
    shortcut_user_id = models.CharField(default="me", max_length=40)
    selected_category_id = models.IntegerField(default=1, blank=True)
    subject_of_memo = models.CharField(max_length=60)  # 스킬 노트의 주제
    last_updated = models.DateTimeField(
        auto_now_add=False, blank=True, null=True)
    last_modified = models.DateTimeField(
        auto_now_add=False, blank=True, null=True)
    last_updated_category = models.CharField(default="1", max_length=10)
    phone = models.CharField(max_length=20)
    reputation = models.IntegerField(default=0)
    email = models.CharField(max_length=20, blank=True)
    # 2244
    public = models.BooleanField(default=True)
    
    github_original = models.CharField(max_length=20, default="www.github.com" , blank=True , null=True)
    github1 = models.CharField(max_length=20, default="www.github.com" , blank=True , null=True)
    github2 = models.CharField(max_length=20, default="www.github.com" , blank=True , null=True)
    github3 = models.CharField(max_length=20, default="www.github.com" , blank=True , null=True)
    github4 = models.CharField(max_length=20, default="www.github.com" , null=True)
    lecture_url = models.CharField(max_length=40, blank=True)
    skill_note_reputation = models.IntegerField(
        default=0)  # skill note 유저 리스트 점수 추가할때 계산됨
    completecount = models.IntegerField(default=0)
    uncompletecount = models.IntegerField(default=0)
    click_count = models.IntegerField(default=0)
    first_category = models.CharField(max_length=5, default="ca1")
    last_category = models.CharField(max_length=5, default="ca1")


class HistoryForUpdate(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=40)
    category = models.CharField(max_length=40)
    date = models.DateTimeField(auto_now_add=True, blank=True, null=True)

# class AnotherSkilNotes(models.Model):
#     author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="+")
#     title = models.CharField(max_length=20)
#     site = models.CharField(max_length=120)
