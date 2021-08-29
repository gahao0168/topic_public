from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from ttyd.models import TTYDFunc

class RegisterForm(UserCreationForm):
    last_name = forms.CharField(
        label="姓氏",
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    first_name = forms.CharField(
        label="名字",
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    username = forms.CharField(
        label="帳號",
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    email = forms.EmailField(
        label="電子郵件",
        widget=forms.EmailInput(attrs={'class': 'form-control'})
    )
    password1 = forms.CharField(
        label="密碼",
        widget=forms.PasswordInput(attrs={'class': 'form-control'})
    )
    password2 = forms.CharField(
        label="確認密碼",
        widget=forms.PasswordInput(attrs={'class': 'form-control'})
    )
    class Meta:
        model = User
        fields = ('username', 'last_name', 'first_name', 'email', 'password1', 'password2')

class LoginForm(forms.Form):
    username = forms.CharField(
        label="帳號",
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    password = forms.CharField(
        label="密碼",
        widget=forms.PasswordInput(attrs={'class': 'form-control'})
    )

class TTYDFunctionForm(forms.ModelForm):

    class Meta:
        model = TTYDFunc
        # fields = ('name', 'content')
        fields = '__all__'
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'content': forms.TextInput(attrs={'class': 'form-control'})
        }
        labels = {
            'name': '欲新增的功能名稱',
            'content':'欲新增的功能內容'
        }