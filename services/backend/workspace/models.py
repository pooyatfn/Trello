from django.db import models

from trello_user.models import TrelloUser


class Workspace(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    users = models.ManyToManyField(TrelloUser, through='WorkspaceMembership')

    def __str__(self):
        return self.name


class WorkspaceMembership(models.Model):
    user = models.ForeignKey(TrelloUser, on_delete=models.CASCADE)
    workspace = models.ForeignKey(Workspace, on_delete=models.CASCADE)
    is_admin = models.BooleanField(default=False)

    class Meta:
        unique_together = [['user', 'workspace']]

    def __str__(self):
        return f"{self.user.username} in {self.workspace.name}"
