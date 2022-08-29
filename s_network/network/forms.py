from django import forms
from .models import Page
from django.contrib.auth.forms import  AuthenticationForm
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError


class UserRegisterForm(forms.ModelForm):
    password = forms.CharField(label='Пароль', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Повторите пароль', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('username', 'email')

    def clean_password2(self):
        cd = self.cleaned_data
        if cd['password'] != cd['password2']:
            raise forms.ValidationError('Пароли не совпадают')
        return cd['password2']


class PageForm(forms.ModelForm):
    class Meta:
        model = Page
        fields = ('photo', 'age', 'first_name', 'last_name')


class UserLoginForm(AuthenticationForm):
    username = forms.CharField(label='Имя пользователя',
                               widget=forms.TextInput(attrs={'class': 'form-control'}))
    password = forms.CharField(label='Пароль',
                               widget=forms.PasswordInput(attrs={'class': 'form-control'}))


class PageEditForm(forms.ModelForm):
    class Meta:
        model = Page
        fields = ('first_name', 'last_name', 'age', 'photo')


