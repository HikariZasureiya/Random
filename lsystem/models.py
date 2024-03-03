from django.contrib.auth.models import AbstractUser
from django.db import models

class cred(models.Model):
    otp_secret = models.CharField(max_length=255, blank=True, null=True)
    otp_ver = models.CharField(max_length=255, blank=True, null=True)
    username=models.CharField(default='', max_length=15)

