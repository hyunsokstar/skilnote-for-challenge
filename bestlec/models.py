from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Best20(models.Model):
    title = models.CharField(max_length=50)
    description = models.TextField(blank=True)
    url_lec = models.CharField(max_length= 60)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    grade = models.IntegerField(default=0)

    def __str__(self):
        return self.title

class Finisher(models.Model):
    bestlec = models.ForeignKey(Best20, on_delete=models.CASCADE)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    comment = models.CharField(max_length= 50)
    git_hub = models.CharField(max_length= 80)
    note = models.CharField(max_length= 50)
    created_at = models.DateTimeField(auto_now_add=True)

    def get_insert_url(self):
        return reverse('bestlec:finisher_new', args=[self.bestlec.id])

class RecommandBest20(models.Model):
    bestlec = models.ForeignKey(Best20, on_delete=models.CASCADE)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
