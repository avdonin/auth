from django import forms
from django.contrib.auth.forms import UserCreationForm, PasswordResetForm
#from django.contrib.auth.models import User
from accounts.models import User

class SignupForm(UserCreationForm):
    email = forms.EmailField(max_length=254, help_text='Required')
    class Meta:
        model = User
        fields = ('email', 'first_name', 'last_name', 'password1', 'password2')


class CustomPasswordResetForm(PasswordResetForm):
    email = forms.EmailField(max_length=254, help_text='Required')
    class Meta:
        model = User
        fields = ('email',)
