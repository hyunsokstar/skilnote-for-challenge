from django.contrib import admin
from . models import SkilBlogTitle,SkilBlogContent, Type, CommentForSkilBlogTitle

# category 삭제

# Register your models here.

@admin.register(CommentForSkilBlogTitle)
class CommentForSkilBlogTitleAdmin(admin.ModelAdmin):
    list_display=['id','content','author']

@admin.register(SkilBlogTitle)
class SkilBlogTitleAdmin(admin.ModelAdmin):
    list_display=['id','title','author']

@admin.register(SkilBlogContent)
class SkilBlogContentAdmin(admin.ModelAdmin):
    list_display=['id','title','content1','content2','type','author']
