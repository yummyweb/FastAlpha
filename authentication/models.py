from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager

# Create your models here.
class User(AbstractUser):
    is_investor = models.BooleanField(default=False)

    def __str__(self):
        return self.username