from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms
from .models import User, Customer, Order


from .models import Order


class OrderForm(ModelForm):
    class Meta:
        model = Order
        fields = '__all__'


class CreateUserForm(UserCreationForm):
    username = forms.CharField(
        max_length=30, required=True, help_text='Required. Enter a unique username.')
    name = forms.CharField(max_length=50, required=True,
                           help_text='Required. Enter your full name.')
    phone_number = forms.CharField(
        max_length=15, required=True, help_text='Required. Enter your phone number.')
    dob = forms.DateField(required=True, help_text='Required. Enter your date of birth (dd/mm/yyyy).',
                          input_formats=['%d/%m/%Y'])
    house_address = forms.CharField(
        max_length=100, required=True, help_text='Required. Enter your house address.')
    email = forms.EmailField(max_length=254, required=True,
                             help_text='Required. Enter a valid email address.')
    password1 = forms.CharField(
        widget=forms.PasswordInput, required=True, help_text='Required. Enter a strong password.')
    password2 = forms.CharField(
        widget=forms.PasswordInput, required=True, help_text='Required. Re-enter the password.')

    class Meta:
        model = User
        fields = ['username', 'name', 'phone_number', 'dob',
                  'house_address', 'email', 'password1', 'password2']

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data.get('email')
        user.set_password(self.cleaned_data.get('password1'))
        user.save()

        customer = Customer.objects.create(
            user=user,
            name=self.cleaned_data.get('name'),
            email=self.cleaned_data.get('email'),
            phone_number=self.cleaned_data.get('phone_number'),
            dob=self.cleaned_data.get('dob'),
            house_address=self.cleaned_data.get('house_address')
        )

        return user


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
