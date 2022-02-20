from django import forms
from django_summernote.widgets import SummernoteWidget, SummernoteInplaceWidget
from .models import Manual
from django.contrib.admin import widgets


class ManualForm(forms.ModelForm):
    # deadline = forms.SplitDateTimeField(widget=widgets.AdminSplitDateTime)
    class Meta:
        model = Manual
        fields = ['title', 'content']

        widgets = {
            'title': forms.TextInput(attrs={'size': 80}),
            'content': SummernoteWidget(),
        }
