from django.db import models
from markdownx.models import MarkdownxField
from markdownx.utils import markdown
from django.contrib.auth.models import User
from django.urls import reverse
from wm.models import Type
from django.urls import reverse

# Create your models here.
class SkilBlogTitle(models.Model):
    title = models.CharField(max_length=120)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
    reputation = models.IntegerField(default=0)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('skilblog:SkilBlogTitleList')

class CommentForSkilBlogTitle(models.Model):
    sbt = models.ForeignKey(SkilBlogTitle, on_delete=models.CASCADE)
    content = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.content


class SkilBlogContent(models.Model):
    sbt = models.ForeignKey(SkilBlogTitle, on_delete=models.CASCADE)
    title = models.CharField(max_length=120)
    filename= models.CharField(max_length=120, blank=True)
    content1 = models.CharField(max_length=180, blank=True)
    content2 = models.TextField(blank=True)
    created = models.DateTimeField(auto_now_add=True , editable = False)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    type= models.ForeignKey(Type, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='wm/%y%m%d', blank=True)

    def __str__(self):
        return self.title

class LikeForSkilBlogTitle(models.Model):
    sbt = models.ForeignKey(SkilBlogTitle, on_delete=models.CASCADE)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
