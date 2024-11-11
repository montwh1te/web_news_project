from django.contrib import admin  # Certifique-se de que esta linha está presente
from django.urls import path
from . import views  
# Supondo que suas views estão no mesmo app

urlpatterns = [
    path('', views.home, name='home'),
    path('registro/', views.registro, name='registro'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('noticia/<slug:slug>/', views.detalhes_noticia, name='detalhes_noticia'),  # Corrigido para 'noticia/'
]
