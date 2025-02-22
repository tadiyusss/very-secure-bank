from .models import *
from django import forms

class RegisterForm(forms.Form):
    first_name = forms.CharField(
        max_length=100,
        widget=forms.TextInput(attrs={'class': 'w-full border px-2 py-1 rounded border-gray-300 focus:outline-indigo-500'}),
        label = 'First Name',
        required = True
    )

    last_name = forms.CharField(
        max_length=100,
        widget=forms.TextInput(attrs={'class': 'w-full border px-2 py-1 rounded border-gray-300 focus:outline-indigo-500'}),
        label = 'Last Name',
        required = True
    )

    username = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'w-full border px-2 py-1 rounded border-gray-300 focus:outline-indigo-500'}),
        label = 'Username',
        required = True
    )

    email = forms.EmailField(
        widget=forms.EmailInput(attrs={'class': 'w-full border px-2 py-1 rounded border-gray-300 focus:outline-indigo-500'}),
        label = 'Email',
        required = True
    )

    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'w-full border px-2 py-1 rounded border-gray-300 focus:outline-indigo-500'}),
        label = 'Password',
        required = True
    )

    address = forms.CharField(
        max_length=100,
        widget=forms.TextInput(attrs={'class': 'w-full border px-2 py-1 rounded border-gray-300 focus:outline-indigo-500'}),
        label = 'Address',
        required = True
    )

class LoginForm(forms.Form):
    username = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'w-full border px-2 py-1 rounded border-gray-300 focus:outline-indigo-500'}),
        label = 'Username',
        required = True
    )

    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'w-full border px-2 py-1 rounded border-gray-300 focus:outline-indigo-500'}),
        label = 'Password',
        required = True
    )

class EditUserForm(forms.Form):
    first_name = forms.CharField(
        max_length=100,
        widget=forms.TextInput(attrs={'class': 'w-full border px-2 py-1 rounded border-gray-300 focus:outline-indigo-500'}),
        label = 'First Name',
        required = True
    )

    last_name = forms.CharField(
        max_length=100,
        widget=forms.TextInput(attrs={'class': 'w-full border px-2 py-1 rounded border-gray-300 focus:outline-indigo-500'}),
        label = 'Last Name',
        required = True
    )

    email = forms.EmailField(
        widget=forms.EmailInput(attrs={'class': 'w-full border px-2 py-1 rounded border-gray-300 focus:outline-indigo-500'}),
        label = 'Email',
        required = True
    )

    address = forms.CharField(
        max_length=100,
        widget=forms.TextInput(attrs={'class': 'w-full border px-2 py-1 rounded border-gray-300 focus:outline-indigo-500'}),
        label = 'Address',
        required = True
    )

class ChangePasswordForm(forms.Form):
    new_password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'w-full border px-2 py-1 rounded border-gray-300 focus:outline-indigo-500'}),
        label = 'New Password',
        required = True
    )

    confirm_password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'w-full border px-2 py-1 rounded border-gray-300 focus:outline-indigo-500'}),
        label = 'Confirm Password',
        required = True
    )

class SendMoneyForm(forms.Form):
    amount = forms.FloatField(
        widget=forms.NumberInput(attrs={'class': 'w-full border px-2 py-1 rounded border-gray-300 focus:outline-indigo-500'}),
        label = 'Amount',
        required = True
    )

    receiver_wallet_address = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'w-full border px-2 py-1 rounded border-gray-300 focus:outline-indigo-500'}),
        label = 'Receiver',
        required = True
    )

class AddMoneyForm(forms.Form):
    amount = forms.FloatField(
        widget=forms.NumberInput(attrs={'class': 'w-full border px-2 py-1 rounded border-gray-300 focus:outline-indigo-500'}),
        label = 'Amount',
        required = True
    )