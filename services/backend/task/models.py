from django.db import models

# from trello_user.models import TrelloUser
from workspace.models import Workspace


class Task(models.Model):
    STATUS_CHOICES = [
        ('Planned', 'Planned'),
        ('In Progress', 'In Progress'),
        ('Completed', 'Completed'),
    ]

    PRIORITY_CHOICES = [
        ('Low', 'Low'),
        ('Medium', 'Medium'),
        ('High', 'High'),
    ]

    title = models.CharField(max_length=255)
    description = models.TextField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Planned')
    estimated_time = models.DurationField()
    actual_time = models.DurationField(null=True, blank=True)
    due_date = models.DateField()
    priority = models.CharField(max_length=20, choices=PRIORITY_CHOICES)
    workspace = models.ForeignKey(Workspace, on_delete=models.CASCADE)
    assignee = models.ForeignKey(to='trello_user.TrelloUser', null=True, blank=True, on_delete=models.SET_NULL)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    image_url = models.URLField(null=True, blank=True)

    def __str__(self):
        return self.title


class SubTask(models.Model):
    IS_COMPLETED_CHOICES = [
        ('No', 'No'),
        ('Yes', 'Yes'),
    ]

    title = models.CharField(max_length=255)
    is_completed = models.CharField(max_length=10, choices=IS_COMPLETED_CHOICES, default='No')
    task = models.ForeignKey(Task, related_name='subtasks', on_delete=models.CASCADE)
    assignee = models.ForeignKey(to='trello_user.TrelloUser', null=True, blank=True, on_delete=models.SET_NULL)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.task.title} - {self.title}"
