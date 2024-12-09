''' **IMPORTAÇÕES DO DJANGO** '''

 # Importa a função `path` do Django, que é utilizada para definir rotas (URLs) e mapeá-las para as funções de visualização (views).
from django.urls import path  
   

''' **IMPORTAÇÕES LOCAIS** '''

# Importa o módulo `views` do aplicativo atual, onde as funções de visualização (views) estão definidas.
from . import views  




# Define as rotas da aplicação e mapeia URLs para funções específicas nas views.
urlpatterns = [
      
    # Define a URL raiz da aplicação ('/') e mapeia para a função `home` no módulo `views`.
    # A URL é identificada pelo nome 'home', que pode ser usado em templates ou redirecionamentos.
    path('', views.home, name='home'),  
        
    # Define a URL para exibir os detalhes de uma notícia específica.
    # A URL recebe um parâmetro de slug, que é uma versão amigável do título da notícia.
    # A função `detalhes_noticia` no módulo `views` é chamada para exibir a notícia, e a URL é identificada pelo nome 'detalhes_noticia'.
    path('noticia/<slug:slug>/', views.detalhes_noticia, name='detalhes_noticia'),  
       
    # Define a URL para buscar notícias com base em critérios fornecidos.
    # A função `buscar_noticias` no módulo `views` é chamada para exibir os resultados da busca.
    # A URL é identificada pelo nome 'buscar_noticias'.
    path('buscar_noticias/', views.buscar_noticias, name='buscar_noticias'),  

    # Define uma URL para exibir notícias filtradas por categoria, com o nome do time como parâmetro.
    # O parâmetro `nome_time` é uma string que representa a categoria ou o nome do time.
    # A função `exibir_categoria` no módulo `views` é chamada, e a URL é identificada pelo nome 'exibir_categoria'.
    path('categoria/<str:nome_time>/', views.exibir_categoria, name='exibir_categoria'),  
        
    # Define uma URL para gerenciar os likes em uma notícia específica.
    # A URL recebe um parâmetro de slug da notícia e mapeia para a função `atualizar_like` no módulo `views`.
    # A URL é identificada pelo nome 'atualizar_like'.
    path('noticia/<slug:slug>/like/', views.atualizar_like, name='atualizar_like'), 

    # Define uma URL para adicionar comentários em uma notícia.
    # A URL recebe um parâmetro de slug da notícia e mapeia para a função `adicionar_comentario` no módulo `views`.
    # A URL é identificada pelo nome 'adicionar_comentario'.
    path('noticia/<slug:slug>/comentar/', views.adicionar_comentario, name='comentar_noticia'),  
       
    # Define uma URL para salvar uma notícia como arquivo HTML.
    # A URL recebe um parâmetro de slug e mapeia para a função `salvar_noticia_html` no módulo `views`.
    # A URL é identificada pelo nome 'salvar_noticia_html'.
    path('salvar-noticia-html/<slug:slug>/', views.salvar_noticia_html, name='salvar_noticia_html'),


    # Define uma URL para criar uma nova notícia.
    # A função `criar_noticia` no módulo `views` é chamada.
    # A URL é identificada pelo nome 'criar_noticia'.
    path('criar_noticia/', views.criar_noticia, name='criar_noticia'),

    # Define uma URL para deletar um comentário específico.
    # A URL recebe o ID do comentário como parâmetro e mapeia para a função `deletar_comentario` no módulo `views`.
    # A URL é identificada pelo nome 'deletar_comentario'.
    path('noticia/comentario/deletar/<int:comentario_id>/', views.deletar_comentario, name='deletar_comentario'),

    # Define uma URL para deletar uma notícia específica.
    # A URL recebe o ID da notícia como parâmetro e mapeia para a função `deletar_noticia` no módulo `views`.
    # A URL é identificada pelo nome 'deletar_noticia'.
    path('noticia/deletar/<int:noticia_id>/', views.deletar_noticia, name='deletar_noticia'),

    # Define uma URL para exibir a página de gerenciamento de notícias para funcionários.
    # A função `pagina_noticias_funcionarios` no módulo `views` é chamada.
    # A URL é identificada pelo nome 'pagina_noticias_funcionarios'.
    path('pagina_noticias_funcionarios/', views.pagina_noticias_funcionarios, name='pagina_noticias_funcionarios'),
]
