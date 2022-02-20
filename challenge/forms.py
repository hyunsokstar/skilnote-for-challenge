from django import forms
from django.core.exceptions import ValidationError
from django_summernote.widgets import SummernoteWidget, SummernoteInplaceWidget
from .models import LecInfo, challenge_subject

# from bootstrap_datepicker_plus import DatePickerInput

class LecInfoForm(forms.ModelForm):
    class Meta:
        model = LecInfo
        fields = ['lec_name', 'lec_url', 'git_url']

class challenge_subject_form(forms.ModelForm):
    class Meta:
        model = challenge_subject
        fields = ['title','description','home','image']

        widgets = {
            'title': forms.TextInput(attrs={'size': 120}),
            'home': forms.TextInput(attrs={'size': 120}),
            'description': SummernoteWidget(attrs={'summernote': {'width': '100%', 'height': '480px', 'line-height': 1.2, 'font-size':12, 'tabSize': 4, "backcolor":"white", 'color':"white", 'backColor' :'white'  }}),
        }
