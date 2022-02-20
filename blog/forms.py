from .models import Comment
from django import forms
from django_summernote.widgets import SummernoteWidget, SummernoteInplaceWidget
from .models import Post


class PostingFormForPost(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title','content','head_image','category','tags']

        widgets = {
            'title': forms.TextInput(attrs={'size': 100}),
            'content': SummernoteWidget(attrs={'summernote': {'width': '100%', 'height': '400px', 'line-height': 1.2, 'font-size':12, 'tabSize': 4, "backcolor":"white", 'color':"white", 'backColor' :'white' , "maximumImageFileSize": "5242880"  }}),
        }

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('text',)
