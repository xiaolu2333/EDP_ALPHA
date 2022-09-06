from django import forms
from django.core.exceptions import ValidationError
from django.utils.translation import gettext, gettext_lazy as _

from edp_user.models import UserProfile


class UserRegisterForm(forms.Form):
    error_messages = {
        'username_existed': _('The same username already exists, please change it!'),
        'password_short': _('The length of password is less than 6!'),
        'password_mismatch': _('The two passwords are not the same!')
    }

    username = forms.CharField()
    email = forms.CharField(widget=forms.EmailInput())
    password = forms.CharField(
        min_length=6,
        widget=forms.PasswordInput(attrs={'autocomplete': 'new-password'}),
        help_text="密码至少需要六位！",
        strip=False,
    )
    confirm_password = forms.CharField(
        min_length=6,
        widget=forms.PasswordInput(attrs={'autocomplete': 'new-password'}),
        help_text="密码至至少要六位！",
        strip=False,
    )
    role = forms.ChoiceField(choices=UserProfile.ROLE)
    status = forms.ChoiceField(choices=UserProfile.STATUS)

    def clean_password(self):
        """检查密码长度是否大于6"""
        if len(self.cleaned_data['password']) < 6:
            raise ValidationError(
                self.error_messages['password_short'],
            )
        return self.cleaned_data['password']

    def clean_confirm_password(self):
        """检查两次输入的密码是否一致"""
        password = self.cleaned_data['password']
        confirm_password = self.cleaned_data['confirm_password']
        if password != confirm_password:
            raise ValidationError(
                self.error_messages['password_mismatch'],
            )
        return confirm_password


class EDPUserLoginForm(forms.Form):
    error_messages = {
        'password_short': _('The length of password is less than 6!'),
    }

    username = forms.CharField()
    password = forms.CharField(
        min_length=6,
        widget=forms.PasswordInput(attrs={'autocomplete': 'new-password'}),
        help_text="密码至少需要六位！",
        strip=False,
    )

    def clean_password(self):
        """检查密码长度是否大于6"""
        if len(self.cleaned_data['password']) < 6:
            raise ValidationError(
                self.error_messages['password_short'],
            )
        return self.cleaned_data['password']
