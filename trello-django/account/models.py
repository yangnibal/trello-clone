from django.db import models
from django.conf import settings
from django.contrib.auth import get_user_model
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import User, AbstractBaseUser
from django.utils import timezone
from django.contrib.auth.models import UserManager
from django.contrib.auth.models import PermissionsMixin

@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)

class User(AbstractBaseUser, PermissionsMixin):
	profile_img = models.ImageField(default=None)
	name = models.CharField(max_length=50)
	username = models.CharField(max_length=50, unique=True)
	email = models.EmailField()
	password  = models.CharField(max_length=50)
	is_superuser = models.BooleanField(default=False)
	is_staff = models.BooleanField(default=False)
	short_intro = models.CharField(max_length=100, null=True)
	github_link = models.CharField(max_length=60, null=True)
	facebook_link = models.CharField(max_length=60, null=True)
	homepage_link = models.CharField(max_length=60, null=True)
	joined_date = models.DateTimeField(default=timezone.now)
	followers = models.ManyToManyField(settings.AUTH_USER_MODEL, default=None)
	USERNAME_FIELD = 'username'
	REQUIRED_FIELDS = ['email', 'password', 'is_staff']

	objects = UserManager()
# Create your models here.
