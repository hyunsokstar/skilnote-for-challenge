from django import forms
from django.core.exceptions import ValidationError
from .models import Todo, CommentForTodo

from django_summernote.widgets import SummernoteWidget, SummernoteInplaceWidget
from django.contrib.admin import widgets

import datetime

class TodoForm(forms.ModelForm):

    dead_line = forms.SplitDateTimeField(widget=widgets.AdminSplitDateTime, initial=datetime.datetime.now())

    class Meta:
        model = Todo

        fields = ['title', 'content','classification','dead_line']
        widgets = {
            'title': forms.TextInput(attrs={'size': 80}),
            'content': SummernoteWidget(),
        }

class TodoAdminForm(forms.ModelForm):
    dead_line = forms.SplitDateTimeField(widget=widgets.AdminSplitDateTime , initial=datetime.datetime.now())

    class Meta:
        model = Todo
        fields = ['classification','title', 'content','dead_line']

        widgets = {
            'title': forms.TextInput(attrs={'size': 80}),
            'content': SummernoteWidget(),
        }

class CommentForm(forms.ModelForm):
    class Meta:
        model = CommentForTodo
        fields = ('title','file_name','text')

        widgets = {
            'title': forms.TextInput(attrs={'size': 65}),
            'file_name': forms.TextInput(attrs={'size': 65}),
            'text': SummernoteWidget(attrs={'summernote': {'width': '100%', 'iframe': False, "dialogsInBody":False}}),
        }

class CommentForm_TextArea(forms.ModelForm):
    class Meta:
        model = CommentForTodo
        fields = ('title','file_name','text')
