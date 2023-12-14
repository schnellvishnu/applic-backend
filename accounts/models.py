from django.db import models
from multiselectfield import MultiSelectField
from django.contrib.auth.models import AbstractBaseUser,PermissionsMixin,BaseUserManager
from django.contrib.auth import get_user_model
# Create your models here.


class Register(models.Model):
    id = models.AutoField(primary_key=True)
    employeeid=models.CharField(max_length=100,default="e101",unique=True)
    Name=models.CharField(max_length=100)
    date_birth=models.DateField(null=True)
    age=models.CharField(max_length=100,default="age")
    place=models.CharField(max_length=100,default="place")
    email=models.EmailField(max_length=100,unique=True)
    address=models.TextField(default="address")
    mobile=models.CharField(max_length=100,default="phone")
    date_join=models.DateField(null=True)
    eduqu=models.CharField(max_length=100,default="qualification")
    userRole=models.CharField(max_length=100,default='admin')
    username=models.CharField(max_length=100,default="username")
    password=models.CharField(max_length=100,default="password")
    conpass=models.CharField(max_length=100,default="confirm password")
    dummy1=models.CharField(max_length=100,default="dummy1")
    dummy2=models.CharField(max_length=100,default="dummy2")
    dummy3=models.CharField(max_length=100,default="dummy3")
    dummy4=models.CharField(max_length=100,default="dummy4")
    key = models.CharField(max_length=500, default="key")


class UserAuditHistoryOnly(models.Model):
    id=models.AutoField(primary_key=True) 
    modelname = models.CharField(max_length=100)
    operationdone = models.CharField(max_length=100)
    donebyuser = models.CharField(max_length=100)
    donebyuserrole = models.CharField(max_length=100)
    donedatetime = models.DateTimeField(max_length=100)
    datefield=models.DateField(auto_now_add=True)                 
    def __str__(self):
        return self.donebyuser   