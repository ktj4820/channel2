import binascii
import os
import datetime

from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.db import models
import pytz


class UserManager(BaseUserManager):

    def create_superuser(self, email, password, **extra_fields):
        email = UserManager.normalize_email(email)
        user = self.model(email=email, is_staff=True, **extra_fields)
        user.set_password(password)
        user.save()
        return user


class User(AbstractBaseUser):

    email = models.EmailField(max_length=254, unique=True)
    name = models.CharField(max_length=100, blank=True, null=True)
    token = models.CharField(max_length=64, blank=True, null=True)
    token_timestamp = models.DateTimeField(blank=True, null=True)
    is_active = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    date_joined = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'user'

    def generate_token(self):
        self.token = binascii.hexlify(os.urandom(32)).decode('utf-8')
        self.token_timestamp = datetime.datetime.now(tz=pytz.UTC)

    def clear_token(self):
        self.token = ''
        self.token_timestamp = None

    def get_full_name(self): return self.email
    def get_short_name(self): return self.email

    def has_perm(self, perm, obj=None): return True
    def has_module_perms(self, app_label): return True

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = UserManager()

    def __str__(self):
        return self.email
