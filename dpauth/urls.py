from django.urls import path
from . import views

app_name = 'dpauth'

urlpatterns = [
    path('login', views.dplogin, name='login'),
    path('register', views.register, name='register'),
    path('captcha', views.send_email_captcha, name='email_captcha'),
    path('logout', views.dplogout, name='logout')
]

