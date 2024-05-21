from django.shortcuts import render,redirect,reverse
from django.http.response import JsonResponse
import string
import random
from django.core.mail import send_mail
from .models import CaptchaModel
from django.views.decorators.http import require_http_methods
from .forms import RegisterForm,LoginForm
from django.contrib.auth import get_user_model,login,logout

# Create your views here.

User = get_user_model()


@require_http_methods(['GET','POST'])
def dplogin(request):
    if request.method == 'GET':
        return render(request, 'login.html')
    else:
        login_form = LoginForm(request.POST)
        if login_form.is_valid():
            email = login_form.cleaned_data.get('email')
            password = login_form.cleaned_data.get('password')
            remember = login_form.cleaned_data.get('remember')

            user = User.objects.filter(email=email).first()
            if user and user.check_password(password):
                login(request,user)


                if not remember:
                    request.session.set_expiry(0) #关闭浏览器清空cookie
                #默认两周登录
                return redirect('/')
            else:
                # 用户名或密码错误
                login_form.add_error(None, '邮箱或者密码错误')
        return render(request, 'login.html', {'form': login_form})


def dplogout(request):
    logout(request) #退出登录
    return redirect('/')

@require_http_methods(['GET','POST'])
def register(request):
    if request.method == 'GET':
        return render(request,'register.html')
    elif request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('email')
            password = form.cleaned_data.get('password')
            username = form.cleaned_data.get('username')
            User.objects.create_user(username=username,email=email,password=password)
            return redirect(reverse('dpauth:login'))
        else:
            print(form.errors)
            return redirect(reverse('dpauth:register'))



def send_email_captcha(request):
    email = request.GET.get('email')
    if not email:
        return JsonResponse({'code':400,'msg':'您也妹写邮箱啊！'})
    # 生成验证码 4位
    captcha = ''.join(random.sample(string.digits,4))

    CaptchaModel.objects.update_or_create(email=email,defaults={'captcha':captcha})

    send_mail(subject="dp博客注册验证码",message=f"您的注册验证码是：{captcha}",recipient_list=[email],from_email=None)

    return JsonResponse({'code':200,'msg':'验证码发送成功！！！'})
