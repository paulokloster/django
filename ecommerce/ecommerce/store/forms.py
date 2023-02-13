from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms

from .models import Order


class OrderForm(ModelForm):
    class Meta:
        model = Order
        fields = '__all__'


class CreateUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']


# from django import forms
# from django.contrib.auth.models import User
# from django.contrib.auth.forms import UserCreationForm


# class LoginForm(forms.Form):
#     username = forms.CharField(label='Username', max_length=64)
#     password = forms.CharField(label='Password', widget=forms.PasswordInput())


# class SignupForm(forms.ModelForm):
#     username = forms.CharField(max_length=30, label='Username')
#     email = forms.EmailField(max_length=254, label='Email')
#     password = forms.CharField(widget=forms.PasswordInput, label='Password')
#     confirm_password = forms.CharField(
#         widget=forms.PasswordInput, label='Confirm Password')

#     def clean(self):
#         cleaned_data = super().clean()
#         password = cleaned_data.get('password')
#         confirm_password = cleaned_data.get('confirm_password')
#         if password != confirm_password:
#             raise forms.ValidationError("Passwords do not match")

#     class Meta:
#         model = User
#         fields = ('username', 'email', 'password', 'confirm_password')
