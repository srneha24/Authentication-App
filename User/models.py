from django.db import models
from django.contrib.auth.models import AbstractUser


# Create your models here.
class CustomUser(AbstractUser):
    DESIGNATION_CHOICES = (
        ('S', 'Student'),
        ('T', 'Teacher'),
    )

    email = models.EmailField(blank=False, null=False, unique=True)
    designation = models.CharField(max_length=1, blank=False, null=False, choices=DESIGNATION_CHOICES)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['designation']
