from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User
from datetime import datetime, timezone

# Create your models here.


class TodoItem(models.Model):
    PRIORITY_HIGH = 1
    PRIORITY_MEDIUM = 2
    PRIORITY_LOW = 3

    PRIORITY_CHOICES = [
        (PRIORITY_HIGH, "Высокий приоритет"),
        (PRIORITY_MEDIUM, "Средний приоритет"),
        (PRIORITY_LOW, "Низкий приоритет"),
    ]

    description = models.CharField(max_length=64)
    is_completed = models.BooleanField("выполнено", default=False)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    owner = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='tasks')
    priority = models.IntegerField("Приоритет", choices=PRIORITY_CHOICES, default=PRIORITY_MEDIUM)

    def delta_time(self):
        delta = (datetime.now(timezone.utc) - self.created).days
        print(delta)
        return delta

    def __str__(self):
        return self.description.lower()

    def get_absolute_url(self):
        return reverse("tasks:details", args=[self.pk])

    class Meta:
        ordering = ('-created', )
