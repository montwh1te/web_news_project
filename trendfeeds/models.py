''' **IMPORTAÇÕES DO DJANGO**  '''
# Módulo do Django que fornece classes e métodos para criar e manipular modelos (representações de tabelas do banco de dados).
from django.db import models

# Função que converte strings em slugs (URLs amigáveis), removendo caracteres especiais e substituindo espaços por hifens.
from django.utils.text import slugify

from api.models import Time
# Classe usada para lançar erros de validação ao verificar dados, como ao salvar informações que não atendem aos requisitos.

from users.models import Usuarios
from django.core.exceptions import ValidationError



''' **IMPORTAÇÕES INTERNAS**  '''
# Modelo personalizado que provavelmente representa os usuários do sistema, definido no app `users`.
from users.models import Usuarios





class Categoria(models.Model):

    # Campo para armazenar o nome completo da categoria (máximo de 50 caracteres).
    nome_categoria = models.CharField(max_length=50)
    nome = models.CharField(max_length=50)
    descricao = models.TextField(null=True)

    # Campo para armazenar uma cor associada à categoria, geralmente em formato hexadecimal (#RRGGBB), com limite de 10 caracteres.
    cor = models.CharField(max_length=10, null=True)

    # Campo opcional para armazenar uma série ou código associado à categoria (máximo de 5 caracteres).
    serie = models.CharField(max_length=5, null=True)
    time = models.ForeignKey(Time, on_delete=models.CASCADE, null=True, blank=True, default=1)

    def __str__(self):
        # Retorna o nome completo da categoria como representação em texto do objeto.
        return self.nome_categoria




class Noticias(models.Model):

    # Campo para armazenar o título da notícia, com limite de 255 caracteres e valor único.
    titulo = models.CharField(max_length=255, unique=True)

    # Campo para armazenar o título que vai aparecer na tela da notícia, com limite de 255 caracteres e valor único.
    titulo_bonito = models.CharField(max_length=255, null=True)

    # Campo para a descrição completa da notícia, com limite de 7000 caracteres.
    descricao = models.TextField(max_length=7000)

    # Data de publicação da notícia, definida automaticamente ao criar o registro.
    data_publicacao = models.DateField(auto_now_add=True)

<<<<<<< HEAD
    # Data de publicação da notícia, definida automaticamente ao criar o registro.
    hora_publicacao = models.TimeField(auto_now_add=True, null=True)

=======
>>>>>>> 14d5c0173c95180a533e27988c634c59b03f33e1
    # Nome do autor da notícia, limitado a 100 caracteres.
    autor = models.CharField(max_length=100)

    # URL da notícia original, com valor padrão apontando para "ge.globo.com".
    link = models.URLField(default='https://ge.globo.com/')

    # Campo gerado automaticamente com um "slug" único baseado no título da notícia.
    slug = models.SlugField(max_length=255, unique=True, blank=True)

    # Contagem de curtidas na notícia, inicializada como 0.
    like_count = models.IntegerField(default=0)

    # Define uma relação muitos-para-muitos entre `Noticias` e `Categoria`.
    # Especifica o modelo intermediário `CategoriaNoticias` e cria um acesso reverso para `categoria.noticias`.
    categorias = models.ManyToManyField(
        Categoria, 
        through='CategoriaNoticias', 
        related_name='noticias'
    )

    def save(self, *args, **kwargs):
        # Gera automaticamente o slug com base no título da notícia se ele não foi definido.
        if not self.slug:
            self.slug = slugify(self.titulo)
        # Salva o objeto no banco de dados.
        super().save(*args, **kwargs)

    # Retorna o título da notícia como representação textual do objeto.
    def __str__(self):
        return self.titulo

    # Propriedade que retorna o caminho da imagem principal da notícia com base no ID.
    @property
    def imagem_url(self):
        return f"/media/noticias/n_{self.id}_0.jpg"




class CategoriaNoticias(models.Model):

    # Relaciona a categoria à notícia, com remoção em cascata e permite valor nulo.
    categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE, null=True)

    # Relaciona a notícia à categoria, com remoção em cascata e permite valor nulo.
    noticia = models.ForeignKey(Noticias, on_delete=models.CASCADE, null=True)

    # Representa a relação em texto com os IDs da notícia e categor
    def __str__(self):
        return f"Notícia ID {self.noticia.id} - Categoria ID {self.categoria.id}"




class TimeFavorito(models.Model):

    # Relaciona o modelo `Usuarios` a um único time favorito.
    usuario = models.OneToOneField(Usuarios, on_delete=models.CASCADE)

    # Relaciona o modelo `Categoria` ao time do usuário.
    time = models.ForeignKey(Categoria, on_delete=models.CASCADE)

    # Representa em texto o usuário e o time favorito.
    def __str__(self):
        return f"{self.usuario.username} - {self.time}"




class InteracaoUsuario(models.Model):\

    # Relaciona a interação a uma notícia, removendo-a caso a notícia seja excluída.
    noticia = models.ForeignKey(Noticias, on_delete=models.CASCADE)

    # Relaciona a interação a um usuário, removendo-a caso o usuário seja excluído.
    usuario = models.ForeignKey(Usuarios, on_delete=models.CASCADE)

    # Armazena a data em que a interação foi criada, automaticamente.
    data_criacao = models.DateField(auto_now_add=True)

    # Indica se o usuário curtiu a notícia, com valor padrão como falso.
    like = models.BooleanField(default=False)

    # Garante que cada usuário só possa interagir uma vez com uma notícia.
    class Meta:
        unique_together = ('usuario', 'noticia')




class Comentario(models.Model):

    # Relaciona o comentário a um usuário, removendo-o caso o usuário seja excluído.
    usuario = models.ForeignKey(Usuarios, on_delete=models.CASCADE)

    # Relaciona o comentário a uma notícia, removendo-o caso a notícia seja excluída.
    noticia = models.ForeignKey(Noticias, on_delete=models.CASCADE)

    # Campo para o conteúdo textual do comentário.
    comentario = models.TextField()

    # Data e hora de criação do comentário, gerada automaticamente.
    data_criacao = models.DateTimeField(auto_now_add=True)

    # Representa em texto o nome do usuário e os primeiros 20 caracteres do comentário.
    def __str__(self):
        return f"{self.usuario.username}: {self.comentario[:20]}..."