import os
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.db import models


class UserManager(BaseUserManager):

    def create_superuser(self, email, password, **extra_fields):
        email = UserManager.normalize_email(email)
        user = self.model(email=email, is_staff=True, is_active=True, **extra_fields)
        user.set_password(password)
        user.save()
        return user


class User(AbstractBaseUser):

    email = models.EmailField(max_length=254, unique=True)
    name = models.CharField(max_length=50, blank=True)

    token = models.CharField(max_length=64, null=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    date_joined = models.DateTimeField(auto_now_add=True)

    def get_full_name(self):
        return self.name

    def get_short_name(self):
        return self.name

    def generate_token(self):
        self.token = os.urandom(32).encode('hex')

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = UserManager()

    def __unicode__(self):
        return self.email
