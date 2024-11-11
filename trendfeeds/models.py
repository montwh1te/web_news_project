from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.text import slugify
import re  


class Usuarios(AbstractUser):
    foto = models.ImageField(upload_to='usuarios/', blank=True, null=True)


class CategoriaNoticias(models.Model):
    nomecategoria = models.CharField(max_length=50)

    def __str__(self):
        return self.nomecategoria
    

class Noticias(models.Model):
    titulo = models.CharField(max_length=300, unique=True)
    descricao = models.TextField(max_length=7000)
    data_publicacao = models.DateField(auto_now_add=True)
    autor = models.CharField(max_length=100)
    link = models.URLField(default='https://ge.globo.com/')
    categoria = models.ForeignKey(CategoriaNoticias, on_delete=models.SET_NULL, null=True, blank=True)
    slug = models.SlugField(max_length=300, unique=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.titulo)  # Usando slugify para criar um slug limpo e único
        super().save(*args, **kwargs)

    def __str__(self):
        return self.titulo


class ImagemNoticias(models.Model):
    noticia = models.ForeignKey(Noticias, on_delete=models.CASCADE, related_name="imagens")
    imagem = models.ImageField(upload_to='', blank=True, null=True)

    def __str__(self):
        return f"Imagem da notícia: {self.noticia.titulo}"

class TimeFavorito(models.Model):
    usuario = models.OneToOneField(Usuarios, on_delete=models.CASCADE)
    time = models.CharField(max_length=20)

    def __str__(self):
        return f"{self.usuario.username} - {self.time}"

class InteracaoUsuario(models.Model):
    noticia = models.ForeignKey(Noticias, on_delete=models.CASCADE)
    usuario = models.ForeignKey(Usuarios, on_delete=models.CASCADE)
    tipo = models.CharField(choices=[('like', 'Like'), ('comentario', 'Comentario')], max_length=50)
    data_criacao = models.DateField(auto_now_add=True)
    texto = models.CharField(max_length=255, blank=True)

    def __str__(self):
        return f"{self.usuario.username} - {self.tipo} em {self.noticia.titulo}"