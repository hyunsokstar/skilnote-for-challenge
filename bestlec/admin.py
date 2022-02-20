from django.contrib import admin
from django.db import models

from .models import Best20, Finisher, RecommandBest20

@admin.register(Finisher)
class FinisherAdmin(admin.ModelAdmin):
    list_display = ['bestlec','author','comment','git_hub','note', 'created_at']

@admin.register(Best20)
class Best20Admin(admin.ModelAdmin):
    list_display = ['id','title','description','url_lec','grade']

@admin.register(RecommandBest20)
class RecommandBest20Admin(admin.ModelAdmin):
    list_display = ['id','bestlec','author']
