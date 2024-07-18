from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    USER_TYPE_CHOICES = (
        ('client', 'Client'),
        ('worker', 'Worker'),
    )
    user_type = models.CharField(max_length=10, choices=USER_TYPE_CHOICES, verbose_name='User Type')

class Client(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='client')
    company_name = models.CharField(max_length=100, verbose_name='Company Name')
    state = models.CharField(max_length=100)
    lga = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=15, default='', verbose_name='Phone Number')

    def __str__(self):
        return self.user.username

    class Meta:
        verbose_name = 'Client'
        verbose_name_plural = 'Clients'

class Worker(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='worker')
    state = models.CharField(max_length=100)
    lga = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=15, verbose_name='Phone Number')

    def __str__(self):
        return self.user.username

    class Meta:
        verbose_name = 'Worker'
        verbose_name_plural = 'Workers'

class Assignment(models.Model):
    worker = models.ForeignKey(Worker, on_delete=models.CASCADE, related_name='assignments')
    client = models.ForeignKey(Client, on_delete=models.CASCADE, related_name='assignments')
    assigned_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Assignment of {self.worker} to {self.client} on {self.assigned_at}"

    class Meta:
        verbose_name = 'Assignment'
        verbose_name_plural = 'Assignments'
