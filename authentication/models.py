from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser, PermissionsMixin
from rest_framework_simplejwt.tokens import RefreshToken


class UserManager(BaseUserManager):
    def create_user(self, username, email, password=None, first_name=None, last_name=None):
        if username is None:
            raise TypeError('Users should have username')
        if email is None:
            raise TypeError('Users should have email')

        user = self.model(username=username, email=self.normalize_email(email), first_name=first_name,
                          last_name=last_name)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, username, email, password=None, first_name=None, last_name=None):
        if password is None:
            raise TypeError('Password should not to be None')

        user = self.create_user(username, email, password, first_name, last_name)
        user.is_superuser = True
        user.is_staff = True
        user.save()
        return user


def upload_path(filename):
    return '/'.join(['user_avatars', filename])


class User(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(max_length=20, unique=True, db_index=True)
    email = models.EmailField(max_length=50, unique=True, db_index=True)
    first_name = models.CharField(max_length=10, blank=True, null=True)
    last_name = models.CharField(max_length=15, blank=True, null=True)
    is_verified = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    avatar = models.ImageField(blank=True, null=True, upload_to=upload_path)

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']

    objects = UserManager()

    def __str__(self):
        return self.username

    def tokens(self):
        refresh = RefreshToken.for_user(self)
        return {
            'refresh': str(refresh),
            'access': str(refresh.access_token)
        }
