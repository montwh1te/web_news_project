from django.db import models

class Time(models.Model):
    nome = models.CharField(max_length=50)
    ano_fundacao = models.IntegerField()

class Jogador(models.Model):
    time = models.ForeignKey(Time, on_delete=models.CASCADE)
    nome = models.CharField(max_length=50)
    posicao = models.CharField(max_length=10)
    foto = models.ImageField(upload_to='jogadores/', blank=True, null=True)
    
class Presidente(models.Model):
    time = models.OneToOneField(Time, on_delete=models.CASCADE)
    nome = models.CharField(max_length=50)
    foto = models.ImageField(upload_to='presidentes/', blank=True, null=True)
    
class Tecnico(models.Model):
    time = models.OneToOneField(Time, on_delete=models.CASCADE)
    nome = models.CharField(max_length=50)
    foto = models.ImageField(upload_to='tecnicos/', blank=True, null=True)
    
class Estadio(models.Model):
    time = models.OneToOneField(Time, on_delete=models.CASCADE)
    nome = models.CharField(max_length=50)
    foto = models.ImageField(upload_to='estadios/', blank=True, null=True)