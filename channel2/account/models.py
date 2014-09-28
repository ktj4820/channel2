import binascii
import os

from django.contrib.auth.models import BaseUserManager, AbstractBaseUser
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

    token = models.CharField(max_length=64, blank=True, null=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    date_joined = models.DateTimeField(auto_now_add=True)

    def generate_token(self):
        self.token = binascii.hexlify(os.urandom(32)).decode('utf-8')

    def get_full_name(self): return self.email
    def get_short_name(self): return self.email

    def has_perm(self, perm, obj=None): return True
    def has_module_perms(self, app_label): return True

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = UserManager()

    def __unicode__(self):
        return self.email

    class Meta:
        db_table = 'user'
