from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class MyTask(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    sub1 = models.TextField(blank=True)
    sub2 = models.TextField(blank=True)
    sub3 = models.TextField(blank=True)
    sub4 = models.TextField(blank=True)
    sub5 = models.TextField(blank=True)
    sub6 = models.TextField(blank=True)
    sub7 = models.TextField(blank=True)
    sub8 = models.TextField(blank=True)
    sub9 = models.TextField(blank=True)
    sub10 = models.TextField(blank=True)
    sub11 = models.TextField(blank=True)
    sub12 = models.TextField(blank=True)
    sub13 = models.TextField(blank=True)
    sub14 = models.TextField(blank=True)
    sub1_memo= models.TextField(blank=True)
    sub2_memo= models.TextField(blank=True)
    sub3_memo= models.TextField(blank=True)
    sub4_memo= models.TextField(blank=True)
    sub5_memo= models.TextField(blank=True)
    sub6_memo= models.TextField(blank=True)
    sub7_memo= models.TextField(blank=True)
    sub8_memo= models.TextField(blank=True)
    sub9_memo= models.TextField(blank=True)
    sub10_memo = models.TextField(blank=True)
    sub11_memo = models.TextField(blank=True)
    sub12_memo = models.TextField(blank=True)
    sub13_memo = models.TextField(blank=True)
    sub14_memo = models.TextField(blank=True)

# Create your models here.
class MySite(models.Model):
    site_name = models.CharField(max_length=50)
    site_url = models.CharField(max_length= 100)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.site_name
