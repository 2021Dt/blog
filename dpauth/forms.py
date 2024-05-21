from django import forms
from django.contrib.auth import get_user_model
from .models import CaptchaModel

user = get_user_model()


class RegisterForm(forms.Form):
    username = forms.CharField(
        max_length=20,
        min_length=2,
        error_messages={
            'required': '请输入用户名',
            'max_length': '用户名不能超过20个字符',
            'min_length': '用户名至少需要2个字符'
        }
    )
    email = forms.EmailField(
        error_messages={
            'required': '请输入邮箱',
            'invalid': '请输入有效的邮箱地址'
        }
    )
    captcha = forms.CharField(
        max_length=4,
        min_length=4,
        error_messages={
            'required': '请输入验证码',
            'max_length': '验证码长度应为4个字符',
            'min_length': '验证码长度应为4个字符'
        }
    )
    password = forms.CharField(
        max_length=20,
        min_length=6,
        widget=forms.PasswordInput(attrs={'placeholder': '请输入密码'}),
        error_messages={
            'required': '密码不能为空',
            'min_length': '密码长度不能少于6个字符',
            'max_length': '密码长度不能超过20个字符'
        }
    )

    def clean_email(self):
        email = self.cleaned_data.get('email')
        users = user.objects.filter(email=email).exists()
        if users:
            raise forms.ValidationError("邮箱已经被注册")
        return email

    def clean_captcha(self):
        captcha = self.cleaned_data.get('captcha')
        email = self.cleaned_data.get('email')
        captcha_model = CaptchaModel.objects.filter(email=email, captcha=captcha).first()
        if not CaptchaModel:
            raise forms.ValidationError("验证码或邮箱出现异常")
        captcha_model.delete()
        return captcha


class LoginForm(forms.Form):
    email = forms.EmailField(
        error_messages={
            'required': '请输入邮箱',
            'invalid': '请输入有效的邮箱地址'
        }
    )
    password = forms.CharField(
        max_length=20,
        min_length=6,
        widget=forms.PasswordInput(attrs={'placeholder': '请输入密码'}),
        error_messages={
            'required': '密码不能为空',
            'min_length': '密码长度不能少于6个字符',
            'max_length': '密码长度不能超过20个字符'
        }
    )
    remember_me = forms.IntegerField(required=False)
