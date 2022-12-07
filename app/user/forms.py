from django import forms
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _

widgets_general = {
    'first_name': forms.TextInput(attrs={
        'class': 'form-control bg-transparent',
        'placeholder': _('First Name'),
        'autocomplete': 'off'
    }),
    'last_name': forms.TextInput(attrs={
        'class': 'form-control bg-transparent',
        'placeholder': _('Last Name'),
        'autocomplete': 'off'
    }),
    'username': forms.TextInput(attrs={
        'class': 'form-control bg-transparent',
        'placeholder': _('Username'),
        'autocomplete': 'off'
    }),
    'email': forms.TextInput(attrs={
        'class': 'form-control bg-transparent',
        'placeholder': _('Email'),
        'autocomplete': 'off'
    }),
    'password': forms.PasswordInput(attrs={
        'class': 'form-control bg-transparent',
        'placeholder': _('Password'),
        'autocomplete': 'off'
    }),
    'confirm_password': forms.PasswordInput(attrs={
        'class': 'form-control bg-transparent',
        'placeholder': _('Repeat Password'),
        'autocomplete': 'off'
    })
}


class LoginForm(forms.ModelForm):
    class Meta:
        model = get_user_model()
        fields = ('username', 'email', 'password')
        widgets = {
            'username': widgets_general['username'],
            'email': widgets_general['email'],
            'password': widgets_general['password']
        }


class RegisterForm(forms.Form):
    first_name = forms.CharField(max_length=100, widget=widgets_general['first_name'])  # noqa: 501
    last_name = forms.CharField(max_length=100, widget=widgets_general['last_name'])    # noqa: 501
    username = forms.CharField(max_length=100, widget=widgets_general['username'])  # noqa: 501
    email = forms.CharField(max_length=100, widget=widgets_general['email'])
    password = forms.CharField(max_length=100, widget=widgets_general['password'])  # noqa: 501
    confirm_password = forms.CharField(max_length=100, widget=widgets_general['confirm_password'])  # noqa: 501


class ForgetForm(forms.Form):
    email = forms.CharField(max_length=100, widget=widgets_general['email'])


class ResetPassForm(forms.Form):
    password = forms.CharField(max_length=100, widget=widgets_general['password'])  # noqa: 501
    confirm_password = forms.CharField(max_length=100, widget=widgets_general['confirm_password'])  # noqa: 501
