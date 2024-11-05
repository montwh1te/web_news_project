from django.db import models
from django.contrib.auth.models import AbstractUser

class Usuarios(AbstractUser):
    foto = models.ImageField(upload_to='usuarios/', blank=True, null=True)
    # AbstractUser já inclui os campos first_name, last_name, username, email, password, is_staff

class Noticias(models.Model):
    titulo = models.CharField(max_length=20, unique=True)
    descricao = models.CharField(max_length=7000) 
    data_publicacao = models.DateField()
    categoria = models.CharField(choices=[('visitante', 'Visitante'), ('funcionario', 'Funcionário')], max_length=50)
    autor = models.CharField(max_length=20)

    def __str__(self):
        return self.titulo

class Imagemnoticias(models.Model):
    noticia = models.ForeignKey(Noticias, on_delete=models.CASCADE, related_name="imagens")
    
    # O ForeignKey permite que múltiplas imagens estejam relacionadas a uma mesma notícia.
    # Adicionamos o parâmetro related_name para facilitar a consulta das imagens de uma notícia.

    imagem = models.ImageField(upload_to='imagemnoticia/', blank=True, null=True)

    def __str__(self):
        return f"Imagem da notícia: {self.noticia.titulo}"

class Categorianoticias(models.Model):
    noticia = models.OneToOneField(Noticias, on_delete=models.CASCADE)  
    #O OneToOneField é para determinar que as imagens da quela determinada noticia so podem se relacionar a uma noticia, como uma foregein key com unique true

    #O parâmetro on_delete é obrigatório para campos de relacionamento (ForeignKey, OneToOneField, e ManyToManyField) no Django. Ele define o que deve acontecer com o objeto relacionado se o objeto pai for deletado.

    #models.CASCADE: Se o objeto pai for deletado, o objeto relacionado também será deletado automaticamente. 
    nomecategoria = models.CharField(max_length=50) 

    def __str__(self):
        return self.nomecategoria

class TimeFavorito(models.Model):
    usuario = models.OneToOneField(Usuarios, on_delete=models.CASCADE) 
    time = models.CharField(max_length=20, unique=True)

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