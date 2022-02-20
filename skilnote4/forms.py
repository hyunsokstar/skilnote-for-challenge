from django import forms
from django.core.exceptions import ValidationError
from django_summernote.widgets import SummernoteWidget, SummernoteInplaceWidget
from .models import MyShortCutForSkilNote4, CommentForPageForSkilNote4
from django.db.models import F

class MyShortCutForm_input(forms.ModelForm):
    class Meta:
        model = MyShortCutForSkilNote4
        fields = ['title', 'content1']

class MyShortCutForm_image(forms.ModelForm):
    class Meta:
        model = MyShortCutForSkilNote4
        fields = ['title','image']

class SkilNoteForm(forms.ModelForm):
    class Meta:
        model = MyShortCutForSkilNote4
        fields = ['title','filename','content2']

        widgets = {
            'title': forms.TextInput(attrs={'size': 120}),
            'filename': forms.TextInput(attrs={'size': 100}),
            'content2': SummernoteWidget(attrs={'summernote': {'width': '100%', 'height': '480px', 'line-height': 1.2, 'font-size':12, 'tabSize': 4, "backcolor":"white", 'color':"white", 'backColor' :'white'  }}),
        }

class MyShortCutForm_summer_note2(forms.ModelForm):

    class Meta:
        model = MyShortCutForSkilNote4
        fields = ['title','filename','content2']

        widgets = {
            'title': forms.TextInput(attrs={'size': 60}),
            'filename': forms.TextInput(attrs={'size': 60}),
            'content2': SummernoteWidget(attrs={'summernote': {'width': '100%', 'height': '500px', 'line-height': 1.2, 'font-size':12, 'tabSize': 4, "backcolor":"white", 'color':"white", 'backColor' :'white' , "maximumImageFileSize": "5242880"  }}),
        }

class CommentForm(forms.ModelForm):
    class Meta:
        model = CommentForPageForSkilNote4
        fields = ('author','content',)
