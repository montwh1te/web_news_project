from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('registro/', views.registro, name='registro'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),  # Aponta para sua função de logout com redirecionamento
    path('perfil/<perfil_id>/', views.info_perfil, name='info_perfil'),
    # path('time_favorito/', views.time_favorito, name='time_favorito'),
    path('alterar_senha/', views.alterar_senha, name='alterar_senha'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# A ideia é ainda construir esse campo de time_favorito, ou seja, redirecionar o usuário pós registro a essa página para escolher o seu time favorito e armazenar no banco de dados, além disso daí, na informações da conta dar essa opção de alterar o time favorito

# Arrumar no perfil, mudança de imagem. Arrumar erro ao mudar nickname para nickname já existente.

# ----------------------------------------------------------------------------

# Fazer testes finais de usuários.