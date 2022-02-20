from django.contrib import admin
from . models import Manual

@admin.register(Manual)
class ManualAdmin(admin.ModelAdmin):
    list_display = ['title','content','author','url','photo','created_at']
