from django.contrib.auth.forms import UserCreationForm
from .models import Profile
from django import forms

class SignupForm(UserCreationForm):
    # lecture_url = forms.CharField(required=False)
    # github_original = forms.CharField(required=False)
    # github1 = forms.CharField(required=False)
    # github2 = forms.CharField(required=False)
    # github3 = forms.CharField(required=False)
    # github4 = forms.CharField(required=False)
    # email = forms.CharField(required=False)
    # phone = forms.CharField(required=False)

    class Meta(UserCreationForm.Meta):
        fields = UserCreationForm.Meta.fields

    def save(self):
        user = super().save()
        profile = Profile.objects.create(
            user = user,
            # lecture_url = self.cleaned_data['lecture_url'],
            # github_original = self.cleaned_data['github_original'],
            # phone = self.cleaned_data['phone'],
            # email = self.cleaned_data['email'],
            # github1 = self.cleaned_data['github1'],
            # github2 = self.cleaned_data['github2'],
            # github3 = self.cleaned_data['github3'],
            # github4 = self.cleaned_data['github4'],
		)
        return user


from django.contrib.auth.forms import AuthenticationForm
from django import forms

class LoginForm(AuthenticationForm):
    username = forms.CharField(label="Username", max_length=30,
        widget=forms.TextInput(attrs={'class': 'mdl-textfield__input', 'type' :'text', 'id' : 'username'}))
    password = forms.CharField(label="Password", max_length=30,
        widget=forms.TextInput(attrs={'class': 'mdl-textfield__input', 'type' :'password', 'id' : 'password'}))
