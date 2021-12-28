# -*- coding: utf-8 -*-

from django import forms
from django.contrib.auth.models import User
from .models import SignUp


class signUpForm(forms.ModelForm):
    class Meta:
        model = SignUp
        fields = ['username', 'password', 'phone', 'name', 'email', 'addr1', 'addr2', 'addr3', 'optCheck', 'otpCode', 'DI', 'CI', 'CP_CD', 'TX_SEQ_NO', 'RSLT_CD', 'TEL_COM_CD']

class loginForms(forms.Form):
	class Meta:
		model = User
		fields = ['username', 'password']
