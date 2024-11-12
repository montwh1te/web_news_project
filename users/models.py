from django.db import models
from django.contrib.auth.models import AbstractUser

class Usuarios(AbstractUser):
    foto = models.ImageField(upload_to='usuarios/', blank=True, null=True)