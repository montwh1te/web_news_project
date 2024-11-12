from django.db import models
from django.utils.text import slugify
from users.models import Usuarios




class Categoria(models.Model):
    nomecategoria = models.CharField(max_length=50)

    def __str__(self):
        return self.nomecategoria




class Noticias(models.Model):
    titulo = models.CharField(max_length=255, unique=True)
    descricao = models.TextField(max_length=7000)
    data_publicacao = models.DateField(auto_now_add=True)
    autor = models.CharField(max_length=100)
    link = models.URLField(default='https://ge.globo.com/')
    slug = models.SlugField(max_length=255, unique=True, blank=True)

   
    categorias = models.ManyToManyField(
         # Campo ManyToManyField para a relação muitos-para-muitos entre Notícias e Categoria.
        # Isso indica que uma notícia pode ter várias categorias, e uma categoria pode incluir várias notícias.
        Categoria,
        through='CategoriaNoticias', 
        # Especifica o modelo intermediário `CategoriaNoticias` que controlará a relação 
        related_name='noticias'       
        # Define um nome de acesso reverso, permitindo `categoria.noticias.all()` para obter todas as notícias de uma categoria
    )

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.titulo)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.titulo




class CategoriaNoticias(models.Model):
    categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE)  # Temporariamente permite null
    noticia = models.ForeignKey(Noticias, on_delete=models.CASCADE )

    def __str__(self):
        return f"Notícia ID {self.noticia.id} - Categoria ID {self.categoria.id}"




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