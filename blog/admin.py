from django.contrib import admin
from .models import Post, Category,Tag, Comment

@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display=['id','name','slug']
    prepopulated_fields = {'slug': ('name', )}

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display=['id','name','description','slug']
    prepopulated_fields = {'slug': ('name', )}

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ['id','title','head_image','author','created']

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ['id', 'post', 'text', 'author' ,'created_at' , 'modified_at']


# CommentForPage
# class CommentForPage(models.Model):
#     author = models.ForeignKey(User, on_delete=models.CASCADE)
#     content = models.TextField()
#     user_name = models.CharField(max_length=40, blank=True)
#     category_id = models.CharField(max_length=10, blank=True)
#     created_at = models.DateTimeField(auto_now_add=True)
#
#     def __str__(self):
#         return self.content
