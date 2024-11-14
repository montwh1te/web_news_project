from django.contrib import admin  # Certifique-se de que esta linha está presente
from django.urls import path
from . import views  
# Supondo que suas views estão no mesmo app

urlpatterns = [
    path('', views.home, name='home'),
    path('noticia/<slug:slug>/', views.detalhes_noticia, name='detalhes_noticia'),  # Corrigido para 'noticia/'
    path('buscar_noticias/', views.buscar_noticias, name='buscar_noticias'),
    path('buscar_noticias/', views.buscar_noticias, name='buscar_noticias'),
    path('categoria/<str:nome_time>/', views.exibir_categoria, name='exibir_categoria'),



]
