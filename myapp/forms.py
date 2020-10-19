from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, PasswordChangeForm, AuthenticationForm


class CustomRegistrationFrom(UserCreationForm):
    username = forms.CharField(label='username', required=False, widget=forms.TextInput(attrs={'class': 'form-control', "placeholder": "Username", "rows": 1, "cols": 22}))
    email = forms.EmailField(label='email', max_length=100, widget=forms.TextInput(attrs={'class': 'form-control', "placeholder": "Email address", "rows": 1, "cols": 22}))
    password1 = forms.CharField(label='password1', min_length=4, max_length=30, widget=forms.PasswordInput(attrs={'class': 'form-control', "placeholder": "Create password", "rows": 1, "cols": 20}))
    password2 = forms.CharField(label='password2', min_length=4, max_length=30, widget=forms.PasswordInput(attrs={'class': 'form-control', "placeholder": "Confirm password", "rows": 1, "cols": 20}))

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']


class CustomChangePasswordForm(PasswordChangeForm):
    old_password = forms.CharField(label='old_password', min_length=4, max_length=30, widget=forms.PasswordInput(attrs={'class': 'form-control', "placeholder": "Enter old password", "rows": 1, "cols": 20}))
    new_password1 = forms.CharField(label='new_password1', min_length=4, max_length=30, widget=forms.PasswordInput(attrs={'class': 'form-control', "placeholder": "Enter new password", "rows": 1, "cols": 20}))
    new_password2 = forms.CharField(label='new_password2', min_length=4, max_length=30, widget=forms.PasswordInput(attrs={'class': 'form-control', "placeholder": "Confirm new password", "rows": 1, "cols": 20}))

    class Meta:
        model = User
        fields = ['old_password', 'new_password1', 'new_password2']
