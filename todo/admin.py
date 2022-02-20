from django.contrib import admin
from django_summernote.admin import SummernoteModelAdmin

from . models import Todo, CommentForTodo, Category, Classification, TodoType, TeamInfo, TeamMember

@admin.register(TeamMember)
class TeamMemberAdmin(admin.ModelAdmin):
    list_display=['id','team','position']

@admin.register(TeamInfo)
class TeamInfoAdmin(admin.ModelAdmin):
    list_display=['leader','team_name','team_description','member_count']

@admin.register(TodoType)
class TodoTypeAdmin(admin.ModelAdmin):
    list_display=['type_name']

@admin.register(Classification)
class ClassificationAdmin(admin.ModelAdmin):
    list_display=['id','name','description','slug']

# class TodoAdmin(SummernoteModelAdmin):  # instead of ModelAdmin
#     summernote_fields = '__all__'
#     list_display=['id', 'title','author','elapsed_time','dead_line']

# admin.site.register(Todo, TodoAdmin)

@admin.register(Todo)
class TodoAdmin(admin.ModelAdmin):  # instead of ModelAdmin
    # fields = ('author','title','content','dead_line','categpry','classification','importance','type')
    list_display=['id', 'title','author','created','elapsed_time','dead_line','updated']

@admin.register(CommentForTodo)
class CommentAdmin(admin.ModelAdmin):
    list_display = ['id', 'todo','title', 'text', 'author' ,'created_at' , 'modified_at']

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display=['id','name','description','slug']
    prepopulated_fields = {'slug': ('name', )}
