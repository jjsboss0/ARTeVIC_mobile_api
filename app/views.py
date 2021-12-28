from django.shortcuts import render
from django.template import loader
from django.contrib.auth.models import User
from django.contrib.auth import login as auth_login, authenticate, logout
from django.http import HttpResponse,HttpResponseRedirect, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from datetime import datetime, timedelta, date
from django.forms.models import model_to_dict
from bson import json_util
from .models import *
from .forms import *
import os
import sys
import json


def index(request):
    return HttpResponse('')

def gentella_html(request):
    context = {}
    # The template to be loaded as per gentelella.
    # All resource paths for gentelella end in .html.

    # Pick out the html file name from the url. And load that template.
    load_template = request.path.split('/')[-1]
    template = loader.get_template('app/' + load_template)
    return HttpResponse(template.render(context, request))


@csrf_exempt
def login(request):
    try:
        login_form = loginForms(request.POST)
        if login_form.is_valid():
            username = request.POST['username']
            password = request.POST['password']
            print("username::", username)
            print("password::", password)
            user = authenticate(username=username,password=password)
            print(user)
            if user:
                auth_login(request, user)
                useri = SignUp.objects.get(username=username);
                print("----------------userLoginDateUp--------------------")
                print(username," 님이 로그인을 하였습니다.")
                print("----------------userLoginDateUp--------------------")
                useri.date_joined = useri.date_joined.strftime('%Y-%m-%d-%H:%M:%S')
                useri.last_login = useri.last_login.strftime('%Y-%m-%d-%H:%M:%S')
                useri = model_to_dict(useri)

                context = {'value':'1', 'user':useri}
                return HttpResponse(json.dumps(context))
            else:
                login_form.add_error(None, '아이디 또는 비밀번호가 올바르지 않습니다.')
                context = {'value':'-9'}
                return HttpResponse(json.dumps(context))
    except Exception as error:
        print(error)
        context = {'value':'-99'}
        return HttpResponse(json.dumps(context))


@csrf_exempt
def signup(request):
    try:
        if request.method == "POST":
            form = signUpForm(request.POST)
            print("form", form)
            if form.is_valid():
                username = request.POST.get('username')
                new_user = SignUp.objects.create_user(**form.cleaned_data)
                username = request.POST['username']
                password = request.POST['password']
                user = authenticate(username=username,password=password)
                if user:
                    # auth_login(request, user)
                    context = {'value':'1'}
                    return HttpResponse(json.dumps(context))
                else:
                    context = {'value':'-9'}
                    return HttpResponse(json.dumps(context))
            else:
                print("form is not valid")
                return HttpResponse(json.dumps(context))
    except Exception as error:
        print(error)
        context = {'value':'-99'}
        return HttpResponse(json.dumps(context))



@csrf_exempt
def checkUser(request):
    name = request.POST.get('RSLT_NAME')
    CI = request.POST.get('CI')
    DI = request.POST.get('DI')
    phone = request.POST.get('TEL_NO')
    signinfocount = SignUp.objects.filter(name=name,CI=CI,DI=DI,phone=phone).count()
    if signinfocount > 0:
        print("있음")
        userinfo = SignUp.objects.get(name=name,CI=CI,DI=DI,phone=phone)
        username = userinfo.username
        lastThree = username[len(username)-3:]
        replacename = username.replace(lastThree, "***")

        context = {"result":"1","msg":"본인인증에 성공했습니다.","replacename":username}
    elif signinfocount == 0:
        print("없음")
        context = {"result":"0","msg":"가입된 정보가 없습니다."}
    return HttpResponse(json.dumps(context, default=json_util.default))


@csrf_exempt
def checkEmail(request):
    try:
        email = request.POST.get('email')
        emailCheck = SignUp.objects.filter(username = email).count()
        if emailCheck > 0:
            print('email 있음 - 사용불가')
            context = {'value':'1'}
            return HttpResponse(json.dumps(context))
        elif emailCheck == 0:
            print("email 없음 - 사용가능")
            context = {'value':'0'}
            return HttpResponse(json.dumps(context))
    except Exception as error:
        print(error)
        context = {'value':'-99'}
        return HttpResponse(json.dumps(context))


@csrf_exempt
def updateUserinfo(request):
    try:
        userID = request.POST.get("userID")
        useri = SignUp.objects.get(id = userID)
        useri.date_joined = useri.date_joined.strftime('%Y-%m-%d-%H:%M:%S')
        useri.last_login = useri.last_login.strftime('%Y-%m-%d-%H:%M:%S')
        useri = model_to_dict(useri)
        context = {'value':'1', 'user':useri}
        return HttpResponse(json.dumps(context))
    except Exception as error:
        print(error)
        context = {'value':'-99'}
        return HttpResponse(json.dumps(context))


@csrf_exempt
def walletAddrAdd(request):
	try:
		userID = request.POST.get("userID")
		gubun = request.POST.get("gubun")
		addr = request.POST.get("addr")
		userinfo = SignUp.objects.get(id = userID)
		userinfo.ethAddr = addr
		userinfo.vicAddr = addr
		userinfo.save()
		# if gubun == "eth":
        #     userinfo.ethAddr = addr
        #     userinfo.save()
        # elif gubun == "vic":
        #     userinfo.vicAddr = addr
        #     userinfo.save()
		context = {'value':'1'}
		return HttpResponse(json.dumps(context))
	except Exception as error:
		print(error)
		context = {'value':'-99'}
		return HttpResponse(json.dumps(context))



@csrf_exempt
def userLoginDateUp(request):
	try:
		userID = request.POST.get('userID')
		userinfo = SignUp.objects.get(id = userID)
		userinfo.last_login = datetime.now()
		userinfo.save()
		useri = SignUp.objects.get(id = userID)
		useri.date_joined = useri.date_joined.strftime('%Y-%m-%d-%H:%M:%S')
		useri.last_login = useri.last_login.strftime('%Y-%m-%d-%H:%M:%S')

		context = {'value':'1', 'user':useri}
		username = userinfo.username
		print("----------------userLoginDateUp--------------------")
		print(username," 님이 자동 로그인으로 로그인을 하였습니다.")
		print("----------------userLoginDateUp--------------------")
		useri = model_to_dict(useri)
		context = {'result':'1', 'user':useri}
		return HttpResponse(json.dumps(context))
	except Exception as error:
		print(error)




@csrf_exempt
def checkOTPCode(request):
	try:
		userID = request.POST.get('userID')
		userinfo = SignUp.objects.get(id = userID)
		otpCode = userinfo.otpCode
		context = {'result':'1', 'otpCode':otpCode}
		return HttpResponse(json.dumps(context))
	except Exception as error:
		print(error)


@csrf_exempt
def otpCodeSave(request):
	try:
		userID = request.POST.get('userID')
		otpCode = request.POST.get('otpCode')
		userinfo = SignUp.objects.get(id = userID)
		userinfo.otpCode = otpCode
		userinfo.save()
		context = {'result':'1'}
		return HttpResponse(json.dumps(context))
	except Exception as error:
		print(error)
