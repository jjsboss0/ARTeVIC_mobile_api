from django.db import models
from django.contrib.auth.models import UserManager
from django.conf import settings
from django.contrib.auth.models import AbstractUser

class SignUp(AbstractUser):
    name = models.CharField(max_length=150)
    password = models.CharField(max_length=250)
    phone = models.CharField(max_length=250)
    email = models.CharField(max_length=250)
    addr1 = models.CharField(max_length=250)
    addr2 = models.CharField(max_length=250)
    addr3 = models.CharField(max_length=250)
    optCheck = models.CharField(max_length=250, default = "0")
    ethAddr = models.CharField(max_length=255, blank=True, null=True)
    vicAddr = models.CharField(max_length=255, blank=True, null=True)
    otpCode = models.CharField(max_length=255, blank=True, null=True)
    #핸드폰 인증
    DI = models.CharField(blank=True, max_length=255)
    CI = models.CharField(blank=True, max_length=255)
    CP_CD = models.CharField(max_length=30, blank=True, null=True)
    TX_SEQ_NO = models.CharField(max_length=30, blank=True, null=True)
    RSLT_CD = models.CharField(max_length=5, blank=True, null=True)
    TEL_COM_CD = models.CharField(max_length=3, blank=True, null=True)
