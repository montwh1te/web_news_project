# **IMPORTAÇÕES DO DJANGO**
from django.urls import path  
    # Importa a função `path` do Django para definir rotas (URLs) da aplicação.


# **IMPORTAÇÕES LOCAIS**
from . import views  
    # Importa o módulo `views` do aplicativo atual, onde as funções de visualização estão definidas.




# Define as rotas da aplicação e mapeia URLs para funções específicas nas views.
urlpatterns = [
    path('', views.home, name='home'),  
        # URL raiz que chama a view `home`, identificada pelo nome 'home'.
    path('noticia/<slug:slug>/', views.detalhes_noticia, name='detalhes_noticia'),  
        # URL para exibir os detalhes de uma notícia específica, identificada pelo slug.

    path('buscar_noticias/', views.buscar_noticias, name='buscar_noticias'),  
        # URL para buscar notícias com base em critérios fornecidos.

    path('categoria/<str:nome_time>/', views.exibir_categoria, name='exibir_categoria'),  
        # URL para exibir notícias filtradas por categoria, com o nome do time como parâmetro.

    path('noticia/<slug:slug>/like/', views.atualizar_like, name='atualizar_like'),  
        # URL para gerenciar likes em uma notícia específica.

    path('noticia/<slug:slug>/comentar/', views.adicionar_comentario, name='adicionar_comentario'),  
        # URL para adicionar comentários em uma notícia.
]
