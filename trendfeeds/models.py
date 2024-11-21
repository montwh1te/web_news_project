from django.db import models
from django.utils.text import slugify
from users.models import Usuarios
from django.core.exceptions import ValidationError


class Categoria(models.Model):
    nome_categoria = models.CharField(max_length=50)
    nome = models.CharField(max_length=20)
    descricao = models.TextField()
    cor = models.CharField(max_length=10)
    serie = models.CharField(max_length=5, null=True)

    def __str__(self):
        return self.nome_categoria
    # Retorna o nome da categoria como representação em texto do objeto.





class Noticias(models.Model):
    titulo = models.CharField(max_length=255, unique=True)
    # Campo para armazenar o título da notícia, com limite de 255 caracteres e valor único.
    descricao = models.TextField(max_length=7000)
    # Campo para a descrição completa da notícia, com limite de 7000 caracteres.
    data_publicacao = models.DateField(auto_now_add=True)
    # Data de publicação da notícia, definida automaticamente ao criar o registro.
    autor = models.CharField(max_length=100)
    # Nome do autor da notícia, limitado a 100 caracteres.
    link = models.URLField(default='https://ge.globo.com/')
    # URL da notícia original, com valor padrão apontando para "ge.globo.com".
    slug = models.SlugField(max_length=255, unique=True, blank=True)
    # Campo gerado automaticamente com um "slug" único baseado no título da notícia.
    like_count = models.IntegerField(default=0)
    # Contagem de curtidas na notícia, inicializada como 0.


    categorias = models.ManyToManyField(
        Categoria, 
        through='CategoriaNoticias', 
        related_name='noticias'
    )
    # Define uma relação muitos-para-muitos entre `Noticias` e `Categoria`.
    # Especifica o modelo intermediário `CategoriaNoticias` e cria um acesso reverso para `categoria.noticias`.


    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.titulo)
        # Gera automaticamente o slug com base no título da notícia se ele não foi definido.
        super().save(*args, **kwargs)
        # Salva o objeto no banco de dados.


    def __str__(self):
        return self.titulo
    # Retorna o título da notícia como representação textual do objeto.


    @property
    def imagem_url(self):
        return f"/media/noticias/n_{self.id}_0.jpg"
    # Propriedade que retorna o caminho da imagem principal da notícia com base no ID.





class CategoriaNoticias(models.Model):
    categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE, null=True)
    # Relaciona a categoria à notícia, com remoção em cascata e permite valor nulo.
    noticia = models.ForeignKey(Noticias, on_delete=models.CASCADE, null=True)
    # Relaciona a notícia à categoria, com remoção em cascata e permite valor nulo.


    def __str__(self):
        return f"Notícia ID {self.noticia.id} - Categoria ID {self.categoria.id}"
    # Representa a relação em texto com os IDs da notícia e categoria.





class TimeFavorito(models.Model):
    usuario = models.OneToOneField(Usuarios, on_delete=models.CASCADE)
    # Relaciona o modelo `Usuarios` a um único time favorito.
    time = models.ForeignKey(Categoria, on_delete=models.CASCADE)
    # Relaciona o modelo `Categoria` ao time do usuário.

    def __str__(self):
        return f"{self.usuario.username} - {self.time}"
    # Representa em texto o usuário e o time favorito.





class InteracaoUsuario(models.Model):
    noticia = models.ForeignKey(Noticias, on_delete=models.CASCADE)
    # Relaciona a interação a uma notícia, removendo-a caso a notícia seja excluída.
    usuario = models.ForeignKey(Usuarios, on_delete=models.CASCADE)
    # Relaciona a interação a um usuário, removendo-a caso o usuário seja excluído.
    data_criacao = models.DateField(auto_now_add=True)
    # Armazena a data em que a interação foi criada, automaticamente.
    like = models.BooleanField(default=False)
    # Indica se o usuário curtiu a notícia, com valor padrão como falso.


    class Meta:
        unique_together = ('usuario', 'noticia')
        # Garante que cada usuário só possa interagir uma vez com uma notícia.





class Comentario(models.Model):
    usuario = models.ForeignKey(Usuarios, on_delete=models.CASCADE)
    # Relaciona o comentário a um usuário, removendo-o caso o usuário seja excluído.
    noticia = models.ForeignKey(Noticias, on_delete=models.CASCADE)
    # Relaciona o comentário a uma notícia, removendo-o caso a notícia seja excluída.
    comentario = models.TextField()
    # Campo para o conteúdo textual do comentário.
    data_criacao = models.DateTimeField(auto_now_add=True)
    # Data e hora de criação do comentário, gerada automaticamente.


    def __str__(self):
        return f"{self.usuario.username}: {self.comentario[:20]}..."
    # Representa em texto o nome do usuário e os primeiros 20 caracteres do comentário.
