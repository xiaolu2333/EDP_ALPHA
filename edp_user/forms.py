from django import forms
from edp_user.models import UserProfile


class UserRegisterForm(forms.ModelForm):
    confirm_password = forms.CharField(max_length=128)

    class Meta:
        model = UserProfile
        fields = ('username', 'email', 'password', 'confirm_password', 'role', 'status')
        widgets = {
            'username': forms.TextInput(attrs={'lass': 'form-control', 'placeholder': '请输入用户名', }),
            'password': forms.PasswordInput(
                attrs={'class': 'form-control', 'placeholder': '请输入密码', "help_texts": "位数不少为3位"}),
            'confirm_password': forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': '请输入密码'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': '请输入邮箱'}),
            'role': forms.Select(attrs={'class': 'form-control'}),
            'status': forms.Select(attrs={'class': 'form-control'}),
        }

    def clean_confirm_password(self):
        password = self.cleaned_data['password']
        confirm_password = self.cleaned_data['confirm_password']
        if password != confirm_password:
            raise forms.ValidationError('两次密码不一致！')
        return confirm_password

    def clean(self):
        super().clean()
        username = self.cleaned_data['username']
        if UserProfile.objects.exclude(pk=self.instance.pk).filter(username=username).exists():
            raise forms.ValidationError(f'Username "{username}" is already in use.')
        return username
