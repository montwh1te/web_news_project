from django.db import models
from django.contrib.auth.models import AbstractUser

class Usuarios(AbstractUser):
    foto = models.ImageField(upload_to='usuarios/', blank=True, null=True)
    username = models.CharField(max_length=15, unique=True, db_collation='utf8mb4_bin') # especificado collation bin (case sensitive)