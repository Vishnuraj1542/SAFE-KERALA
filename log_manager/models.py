from django.db import models
from django.contrib.auth.models import AbstractUser

class LoginDetails(AbstractUser):
    USER_TYPE_CHOICES = [
        ('ADMIN', 'admin'),
        ('POLICESTATION', 'policestation'),
        ('USER', 'user'),
        ('LABOUR', 'labour'),
    ]
    user_type = models.CharField(max_length=22, choices=USER_TYPE_CHOICES, blank=True, null=True)
    status = models.CharField(default='pending', max_length=10, choices=[
        ('pending', 'Pending'),
        ('verified', 'Verified'),
        ('rejected', 'Rejected'),
    ])
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
