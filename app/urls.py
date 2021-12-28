from django.urls import path, re_path
from app import views

urlpatterns = [
    path('', views.index, name='index'),
    path('signup', views.signup, name='signup'),
    path('login', views.login, name='login'),
    path('updateUserinfo', views.updateUserinfo, name='updateUserinfo'),
    path('checkUser', views.checkUser, name='checkUser'),
    path('checkEmail', views.checkEmail, name='checkEmail'),
    path('walletAddrAdd', views.walletAddrAdd, name='walletAddrAdd'),
    path('userLoginDateUp', views.userLoginDateUp, name='userLoginDateUp'),
	path('checkOTPCode', views.checkOTPCode, name='checkOTPCode'),
	path('otpCodeSave', views.otpCodeSave, name='otpCodeSave'),
]
