from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, PasswordChangeForm


class CustomRegistrationFrom(UserCreationForm):
    first_name = forms.CharField(label='first_name', required=False,
                widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'First name'}))

    last_name = forms.CharField(label='last_name', required=False, 
                widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Last name'}))

    username = forms.EmailField(label='username', max_length=100,
                widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Email address'}))

    password1 = forms.CharField(label='password1', min_length=4, max_length=30,
                widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Create password'}))

    password2 = forms.CharField(label='password2', min_length=4, max_length=30,
                widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Confirm password'}))
    
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'password1', 'password2']

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['username']
        user.save()
        return user


class CustomChangePasswordForm(PasswordChangeForm):
    old_password = forms.CharField(label='old_password', min_length=4, max_length=30, 
                    widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Enter old password'}))

    new_password1 = forms.CharField(label='new_password1', min_length=4, max_length=30,
                    widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Create new password'}))

    new_password2 = forms.CharField(label='new_password2', min_length=4, max_length=30,
                    widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Confirm new password'}))

    class Meta:
        model = User
        fields = ['old_password', 'new_password1', 'new_password2']
