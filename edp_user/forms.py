from django import forms
from edp_user.models import UserProfile


class UserRegisterForm(forms.Form):
    username = forms.CharField()
    email = forms.CharField()
    password = forms.CharField()
    confirm_password = forms.CharField()
    role = forms.ChoiceField(choices=UserProfile.ROLE)
    status = forms.ChoiceField(choices=UserProfile.STATUS)


    class Meta:
        model = UserProfile
        fields = ('username', 'email', 'password', 'confirm_password', 'role', 'status')
        labels = {
            'username': '姓名',
            'email': '邮箱',
            'password': '密码',
            'confirm_password': '确认密码',
            'role': '角色',
            'status': '状态',
        }
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '请输入用户名', }),
            'password': forms.PasswordInput(
                attrs={'class': 'form-control', 'placeholder': '请输入密码', }),
            'confirm_password': forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': '请输入密码'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': '请输入邮箱'}),
            'role': forms.Select(attrs={'class': 'form-control', 'placeholder': '请选择身份'}),
            'status': forms.Select(attrs={'class': 'form-control', 'placeholder': '请选择状态'}),
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


class EDPUserLoginForm(forms.ModelForm):
    username = forms.CharField()
    password = forms.CharField()

    class Meta:
        model = UserProfile
        fields = ('username', 'password')

    widgets = {
        'username': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '请输入用户名', }),
        'password': forms.PasswordInput(
            attrs={'class': 'form-control', 'placeholder': '请输入密码', }),
    }
