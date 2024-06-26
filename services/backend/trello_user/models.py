import django
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone


class TrelloUser(AbstractUser):
    updated_at = models.DateTimeField(default=django.utils.timezone.now, verbose_name='date updated')
