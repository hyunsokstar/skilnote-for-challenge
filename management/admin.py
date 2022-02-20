from django.contrib import admin
from . models import Suggestion
# Register your models here.

# Create your models here.
@admin.register(Suggestion)
class SuggestionAdmin(admin.ModelAdmin):
    list_display=['title','content','author','created']
