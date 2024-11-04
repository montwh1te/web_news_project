from django.db import models
from django.contrib.auth.models import AbstractUser

class Usuarios(AbstractUser):
    foto = models.ImageField(upload_to='usuarios/', blank=True, null=True)
    # o método ABSTRACT USER já possui esses atributos a seguir de tabela: first_name, last_name, username, email, password, is_staff. Sendo necessário apenas a adição do campo nome para completar a tabela de Usuarios. Para que a alteração seja validada pelo Django, é necessário autorizar no arquivo settings.py do PROJETO.