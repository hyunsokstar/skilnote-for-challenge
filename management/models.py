from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Suggestion(models.Model):
    title = models.CharField(max_length=50)
    content = models.TextField(blank=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)

    def get_absolute_url(self):
        return '/management/suggestion/list'

class RecommandSuggestion(models.Model):
    suggestion = models.ForeignKey(Suggestion, on_delete=models.CASCADE)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
