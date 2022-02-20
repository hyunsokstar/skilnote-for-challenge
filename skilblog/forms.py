from django import forms
from django.core.exceptions import ValidationError
from django_summernote.widgets import SummernoteWidget, SummernoteInplaceWidget
from .models import SkilBlogTitle,SkilBlogContent
from django.db.models import F

# category 모델이 foreignkey인데
# 입력시 카테고리 선택 목록의 내용들에 (author = 본인)의 조건을 걸고 싶다.
class SkilBlogContentForm(forms.ModelForm):
    class Meta:
        model = SkilBlogContent
        fields = ['title','filename','content2']

        widgets = {
            'title': forms.TextInput(attrs={'size': 60}),
            'filename': forms.TextInput(attrs={'size': 60}),
            'content2': SummernoteWidget(attrs={'summernote': {'width': '100%', 'height': '480px', 'airMode': False,'fontSize':12, 'tabSize': 4, "backcolor":"white", 'foreColor':"white"  }}),
        }

class ModifySkilBlogTitleForm(forms.ModelForm):
    class Meta:
        model = SkilBlogTitle
        fields = ['title']

        widgets = {
            'title': forms.TextInput(attrs={'size': 90}),
        }
