from django.contrib import admin
from .models import MyTask, MySite

# Register your models here.
@admin.register(MyTask)
class MyTaskAdmin(admin.ModelAdmin):
    list_display = ['author']

# @admin.register(MySite)
# class MySiteAdmin(admin.ModelAdmin):
#     list_display = ['site_name','site_url','author','created_at']
