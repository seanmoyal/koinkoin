from django.contrib.auth.models import AbstractUser
from django.db import models




class CUser(AbstractUser,models.Model):
    points = models.IntegerField(default=500)
    rank = models.IntegerField(default=-1)
    has_team = models.BooleanField(default=False)
    pass