from django.db import models
from django.contrib.auth.models import User
from imagekit.models import ProcessedImageField
from django.urls import reverse

class Manual(models.Model):
    title = models.CharField(max_length=40)
    content = models.TextField(blank=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    url = models.CharField(max_length= 80)
    photo = ProcessedImageField(blank=True, upload_to='board/Manual/%Y/%m/%d')
    created_at = models.DateTimeField(auto_now_add=True)

    def get_absolute_url(self):
        return reverse('board:manual_detail', args=[self.id])
