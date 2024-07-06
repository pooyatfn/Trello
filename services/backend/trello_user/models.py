import django
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone


class TrelloUser(AbstractUser):
    updated_at = models.DateTimeField(default=django.utils.timezone.now, verbose_name='date updated')
    email = models.EmailField(blank=True, max_length=254, verbose_name='email address', unique=True)
    bio = models.CharField(blank=True, max_length=254, verbose_name='biography')
    banner = models.ImageField(upload_to='profile_images/', null=True, blank=True)
    avatar = models.ImageField(upload_to='profile_images/', null=True, blank=True)
