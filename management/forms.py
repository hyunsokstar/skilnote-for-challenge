from django import forms
from django.core.exceptions import ValidationError
from django_summernote.widgets import SummernoteWidget, SummernoteInplaceWidget
from .models import Suggestion

# Create your models here.

class SuggestionForm(forms.ModelForm):
    class Meta:
        model = Suggestion
        fields = ['title', 'content']

        widgets = {
            'title': forms.TextInput(attrs={'size': 80}),
            'content': SummernoteWidget(),
        }
