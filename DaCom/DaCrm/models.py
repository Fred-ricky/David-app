
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models


class UserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("The Email field must be set")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get('is_superuser') is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self.create_user(email, password, **extra_fields)


class CustomUser(AbstractUser):
    username = None  # Remove the default username field
    is_client = models.BooleanField(default=False)
    is_worker = models.BooleanField(default=False)
    email = models.EmailField(unique=True)

    USERNAME_FIELD = 'email'  # Use email as the unique identifier
    REQUIRED_FIELDS = []  # Fields required when creating a superuser

    objects = UserManager()

    def __str__(self):
        return self.email


    

class Client(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='client')
    company_name = models.CharField(max_length=100, verbose_name='Company Name')
    state = models.CharField(max_length=100)
    LGA = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=15, default='', verbose_name='Phone Number')


    def __str__(self):
        return f"{self.user}"
    

    class Meta:
        verbose_name = 'Client'
        verbose_name_plural = 'Clients'

class Worker(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='worker')
    state = models.CharField(max_length=100)
    LGA = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=15, verbose_name='Phone Number')
    specialization = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.user}"

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
