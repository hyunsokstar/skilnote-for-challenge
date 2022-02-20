from django.db import models
from django.contrib.auth.models import User
# from datetime import datetime
from django.utils import timezone
from markdownx.models import MarkdownxField
from markdownx.utils import markdown
from django.urls import reverse
# from datetime import timedelta
from datetime import datetime, timedelta


class TeamInfo(models.Model):
    leader = models.ForeignKey(User, on_delete=models.CASCADE)
    team_name = models.CharField(max_length=50, unique=True)
    team_description = models.TextField(blank=True)
    member_count = models.IntegerField(default=1)

    def __str__(self):
        return self.team_name

class TeamMember(models.Model):
    team = models.ForeignKey(TeamInfo, on_delete=models.CASCADE)
    member = models.ForeignKey(User, on_delete=models.CASCADE)
    position = models.CharField(max_length=50,default="member")


class Classification(models.Model):
    name = models.CharField(max_length=25, unique=True)
    description = models.TextField(blank=True)
    slug = models.SlugField(unique=True, allow_unicode=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = 'classifications'

class Category(models.Model):
    name = models.CharField(max_length=25, unique=True)
    description = models.TextField(blank=True)
    slug = models.SlugField(unique=True, allow_unicode=True)

    def __str__(self):
        return self.name
    class Meta:
        verbose_name_plural = 'categories'
    def get_absolute_url(self):
        return '/todo/category/{}/'.format(self.slug)

class TodoType(models.Model):
    type_name = models.CharField(max_length=20)

    def __str__(self):
        return self.type_name

def utc_tomorrow():
    return datetime.now() + timedelta(days=1)

class Todo(models.Model):
    title = models.CharField(max_length=50)
    content = models.TextField(blank=True)
    created = models.DateTimeField(auto_now=True)
    updated = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    dead_line = models.DateTimeField(blank=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    elapsed_time = models.CharField(max_length=20,blank=True, null=True)
    category = models.ForeignKey(Category, blank=True, null=True, on_delete=models.CASCADE)
    classification = models.ForeignKey(Classification, blank=True, null=True, on_delete=models.CASCADE, default=2)
    completion = models.CharField(max_length=10, default='uncomplete')
    importance = models.IntegerField(default=1)
    type= models.ForeignKey(TodoType, on_delete=models.CASCADE, default=2)
    director = models.CharField(max_length=40, default="terecal")

    def __str__(self):
        return self.title

    def get_markdown_content(self):
        return markdown(self.content)

    def now_diff(self):
        delta = timezone.now() - self.created
        return str(delta - timedelta(microseconds=delta.microseconds))

    def remaining_time(self):
        delta = self.dead_line - timezone.now()
        return str(delta - timedelta(microseconds=delta.microseconds))

    def get_absolute_url(self):
        return reverse('todo:todo_detail', args=[self.id])

class CommentForTodo(models.Model):
    todo= models.ForeignKey(Todo, on_delete=models.CASCADE)
    title= models.CharField(max_length=60)
    file_name = models.CharField(max_length= 60)
    text = models.TextField()
    text_type = models.CharField(max_length=20, blank=True, default="summer_note")
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    type= models.ForeignKey(TodoType, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)
    user_type = models.IntegerField(blank=True,default=1)

    def get_markdown_content(self):
        return markdown(self.text)

    def get_absolute_url(self):
        return reverse('todo:todo_list')
