from .models import ScrappyUser
from django.forms.models import ModelForm
from django import forms


class UserSignUpForm(ModelForm):
    email = forms.EmailField(widget=forms.EmailInput(attrs={'readonly': 'True'}))
    password = forms.CharField(min_length=6, widget=forms.PasswordInput())

    class Meta:
        model = ScrappyUser
        fields = ['email', 'firstname', 'lastname', 'password']
