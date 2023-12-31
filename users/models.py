from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.conf import settings


class UserManager(BaseUserManager):

    use_in_migration = True

    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('Email is Required')
        user = self.model(email=self.normalize_email(email), **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff = True')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser = True')

        return self.create_user(email, password, **extra_fields)


class UserData(AbstractUser):

    username = None
    nickname = models.CharField(max_length=100, unique=True)
    email = models.EmailField(max_length=100, unique=True)
    date_joined = models.DateTimeField(auto_now_add=True)
    is_admin = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    phone = models.CharField(max_length=100, blank=True)
    code = models.CharField(max_length=5, blank=True)
    agree_terms = models.BooleanField(blank=False, default=True)
    agree_personal= models.BooleanField(blank=False, default=True)
    agree_sms = models.BooleanField(blank=False, default=True)
    agree_email = models.BooleanField(blank=False, default=True)
    
    objects = UserManager()
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['nickname', 'password']

    def __str__(self):
        return self.nickname


class Profile(models.Model):
    user = models.OneToOneField(UserData, on_delete=models.CASCADE)
    contact_number = models.CharField(max_length=10, unique=True, null=True, blank=True)
    profile_pic = models.ImageField(upload_to='profiles/', null=True, blank=True)
    bio = models.TextField(blank=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)