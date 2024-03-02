from django.db import models
from django.utils import timezone

class messaging(models.Model):
    user=models.CharField(max_length=15)
    message= models.CharField(max_length=2000)
    time=models.DateTimeField(default=timezone.now)

class online(models.Model):
    user=models.CharField(max_length=15)


# Create your models here.
