from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Profile


class UpdateUserForm(forms.ModelForm):

    class Meta:
        model = User
        fields = ['username', 'email']


class SignUpForm(UserCreationForm):
    email = forms.EmailField(max_length=254, help_text='Required. Inform a valid email address.')

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2', )


class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['period', 'is_news', 'is_weather', 'is_football']