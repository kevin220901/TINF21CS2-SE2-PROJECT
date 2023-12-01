from django.contrib.auth.models import AbstractBaseUser, Group, Permission
from django.db import models

class CustomUser(AbstractBaseUser):
    id = models.AutoField(unique=True, primary_key=True)
    username = models.CharField(max_length=30, unique=True)
    email = models.EmailField(max_length=30,unique=True,blank=False)

    EMAIL_FIELD = "email"
    USERNAME_FIELD = "username"
    REQUIRED_FIELDS = ["email"]