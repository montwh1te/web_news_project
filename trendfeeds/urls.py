from django.contrib import admin  # Certifique-se de que esta linha está presente
from django.urls import path
from . import views  

urlpatterns = [
    path('', views.home, name='home'),
    path('noticia/<slug:slug>/', views.detalhes_noticia, name='detalhes_noticia'),  # Corrigido para 'noticia/'
    path('buscar_noticias/', views.buscar_noticias, name='buscar_noticias'),
    path('categoria/<str:nome_time>/', views.exibir_categoria, name='exibir_categoria'),
    path('noticia/<int:noticia_id>/comentar/', views.salvar_comentario, name='salvar_comentario'),
    path('noticia/<slug:slug>/like/', views.atualizar_like, name='atualizar_like'),
    path('noticia/<slug:slug>/comentar/', views.adicionar_comentario, name='adicionar_comentario'),
    path('noticia/<slug:slug>/interagir/', views.atualizar_like, name='gerenciar_interacao'),

]
