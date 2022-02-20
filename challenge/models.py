from django.db import models
from django.contrib.auth.models import User
from datetime import datetime
from django.utils import timezone
from markdownx.models import MarkdownxField
from markdownx.utils import markdown
from django.urls import reverse
from datetime import timedelta

# Create your models here.

# 챌린지 분류(대주제)
class challenge_subject(models.Model):
	title = models.CharField(max_length=40)
	description = models.TextField(blank=True)
	leader = models.ForeignKey(User, on_delete=models.CASCADE)
	home = models.CharField(max_length=40)
	created= models.DateTimeField(auto_now_add=True)
	image = models.ImageField(upload_to='wm/%y%m%d', blank=True)
	like_count = models.IntegerField(default=0)

	def get_absolute_url(self,*args,**kwargs):
		return reverse('challenge:lecinfo_list_for_challenge', kwargs={'challenge_title':self.title})

	@property
	def like_count2(self):
		return self.likechallengesubject_set.count()

	@property
	def lecinfo_count2(self):
		return self.lecinfo_set.count()

	def __str__(self):
		return self.title

# 챌린지에 대해 좋아요 누른 사람 정보 저장 서로 가르키므로 many to many 로 저장
class LikeChallengeSubject(models.Model):
	challenge = models.ForeignKey(challenge_subject, on_delete=models.CASCADE)
	author = models.ForeignKey(User, on_delete=models.CASCADE)


# 대주제에 대한 소주제 모임
class LecInfo(models.Model):
	challenge = models.ForeignKey(challenge_subject, on_delete=models.CASCADE)
	lec_name = models.CharField(max_length=40)
	manager = models.CharField(max_length=40)
	lec_url = models.CharField(max_length=120)
	git_url = models.CharField(max_length=120)
	lec_reputation = models.IntegerField(default=0)
	student_count = models.IntegerField(default=0)

	def __str__(self):
		return self.lec_name

	def student_count2(self):
		return self.studentrecord_set.count()

# 강의 참여자 리스트
class RecommandLecInfo(models.Model):
	lecinfo = models.ForeignKey(LecInfo, on_delete=models.CASCADE)
	author = models.ForeignKey(User, on_delete=models.CASCADE)

class StudentRecord(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    current_class = models.CharField(max_length=40)
    classification = models.ForeignKey(LecInfo, on_delete=models.CASCADE)
    github_url = models.CharField(max_length=120)
    created= models.DateTimeField(auto_now_add=True)
