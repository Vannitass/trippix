from django import forms
from .models import User

class RegistrationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['email', 'logging', 'password']


class SearchForm(forms.Form):
    query = forms.CharField(max_length=100)
