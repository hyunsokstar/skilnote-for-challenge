from django.contrib import admin
from . models import CommentForShortCutForSkilNote2, MyShortCutForSkilNote2
# Register your models here.

@admin.register(MyShortCutForSkilNote2)
class TempMyShortCutAdmin(admin.ModelAdmin):
    list_display=['id','title','content1','content2','created','author','type']

@admin.register(CommentForShortCutForSkilNote2)
class CommentForShortCutAdmin(admin.ModelAdmin):
    list_display = ['shortcut','title','content','author','created_at']
