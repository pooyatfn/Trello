import os

import django
from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone

from task.models import Task


def get_upload_file_name(instance, filename):
    base_dir = 'trello_user/images/'
    user_id = instance.id
    os.makedirs(os.path.join(settings.MEDIA_ROOT, base_dir, str(user_id)), exist_ok=True)
    return os.path.join(base_dir, str(user_id), filename)


class TrelloUser(AbstractUser):
    updated_at = models.DateTimeField(default=django.utils.timezone.now, verbose_name='date updated')
    email = models.EmailField(blank=True, max_length=254, verbose_name='email address', unique=True)
    bio = models.CharField(blank=True, max_length=254, verbose_name='biography')
    banner = models.CharField(blank=True, max_length=254, verbose_name='banner')
    avatar = models.CharField(blank=True, max_length=254, verbose_name='avatar')

    def get_tasks(self):
        """
        Returns a QuerySet of Task instances assigned to this user.
        """
        # Retrieve all Task instances where the assignee is this user
        tasks = Task.objects.filter(assignee=self)

        return tasks
