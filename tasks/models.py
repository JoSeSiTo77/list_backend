import uuid
from django.db import models
from users.models import User

class Task(models.Model):
    id = models.UUIDField(
        primary_key = True,
        default = uuid.uuid4,
        editable = False
    )
    user_id = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='tasks',
        editable=False
    )
    description = models.TextField(null=False, blank=False)
    date_created = models.DateTimeField(
        auto_now_add=True,
        editable=False
    )