from django import forms
from django.core.exceptions import ValidationError
from django_summernote.widgets import SummernoteWidget, SummernoteInplaceWidget
from .models import MyShortCut, CommentForPage
from django.db.models import F

class MyShortCutForm_input(forms.ModelForm):
    class Meta:
        model = MyShortCut
        fields = ['title', 'content1']

class MyShortCutForm_image(forms.ModelForm):
    class Meta:
        model = MyShortCut
        fields = ['title','image']

class SkilNoteForm(forms.ModelForm):
    class Meta:
        model = MyShortCut
        fields = ['title','filename','content2']

        widgets = {
            'title': forms.TextInput(attrs={'size': 120}),
            'filename': forms.TextInput(attrs={'size': 100}),
            'content2': SummernoteWidget(attrs={'summernote': {'width': '100%', 'height': '480px', 'line-height': 1.2, 'font-size':12, 'tabSize': 4, "backcolor":"white", 'color':"white", 'backColor' :'white'  }}),
        }


class InsertFormForOhterUserNote(forms.ModelForm):
    class Meta:
        model = MyShortCut
        fields = ['title','filename','content2','team_member', 'page_user']

        widgets = {
            'title': forms.TextInput(attrs={'size': 60}),
            'filename': forms.TextInput(attrs={'size': 60}),
            'content2': SummernoteWidget(attrs={'summernote': {'width': '100%', 'height': '500px', 'line-height': 1.2, 'font-size':12, 'tabSize': 4, "backcolor":"white", 'color':"white", 'backColor' :'white' , "maximumImageFileSize": "5242880"  }}),
            'team_member': forms.HiddenInput(attrs={'size':20}),
            'page_user': forms.HiddenInput(attrs={'size':20})
        }


class MyShortCutForm_summer_note2(forms.ModelForm):

    class Meta:
        model = MyShortCut
        fields = ['title','filename','content2']

        widgets = {
            'title': forms.TextInput(attrs={'size': 60}),
            'filename': forms.TextInput(attrs={'size': 60}),
            'content2': SummernoteWidget(attrs={'summernote': {'width': '100%', 'height': '500px', 'line-height': 1.2, 'font-size':12, 'tabSize': 4, "backcolor":"white", 'color':"white", 'backColor' :'white' , "maximumImageFileSize": "5242880"  }}),
        }


class CommentForm(forms.ModelForm):
    class Meta:
        model = CommentForPage
        fields = ('author','content',)
