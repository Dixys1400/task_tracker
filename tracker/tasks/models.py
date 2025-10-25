from django.db import models
from django.contrib.auth.models import User



class Task(models.Model):
    STATUS_CHOICES = [
        ("todo", 'To Do'),
        ("in_progress", 'In Progress'),
        ("done", 'Done'),
    ]
    title = models.CharField(max_length=50, db_index=True)
    description = models.TextField(blank=True, null=True)
    status = models.CharField(max_length=15, choices=STATUS_CHOICES, default='todo')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, db_index=True, null=True, blank=True)

    def __str__(self):
        return f"{self.title} - {self.status}"
