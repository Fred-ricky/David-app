# models.py
from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    USER_TYPE_CHOICES = (
        ('client', 'Client'),
        ('worker', 'Worker'),
    )
    user_type = models.CharField(max_length=10, choices=USER_TYPE_CHOICES)

class Client(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    company_name = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    lga = models.CharField(max_length=100)

    def __str__(self):
        return self.user.username

class Worker(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    state = models.CharField(max_length=100)
    lga = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=15)

    def __str__(self):
        return self.user.username


class Assignment(models.Model):
    worker = models.ForeignKey(Worker, on_delete=models.CASCADE)
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    assigned_at = models.DateTimeField(auto_now_add=True)
    # Add other assignment-related fields here

    def save(self, *args, **kwargs):
        # Add any custom save logic here============
        super().save(*args, **kwargs)
    



