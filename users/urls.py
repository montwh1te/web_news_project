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

# Também criar a funcionalidade de alteração de senha, ou seja dentro da página informações conta, deixar um "a" para "Alterar Senha", pode dai abrir essa página ou um espécie de pop up na tabela para colocar a senha antiga, a nova senha, e a confirmação da nova senha, se a senha antiga estiver correta e as duas outras estiverem iguais, alterar o valor no banco de dados

# Além disso, tem bugs a corrigir, o login ta bugando, tem q dar uma olhada, a senha no banco de dados somente fica criptografada quando registrada, depois que alterada uma vez, descriptografa. No registro e no login, tem que gerar o relatório de erro ao usuário, em vez da página só reiniciar por um erro. E na página de informações da conta, a alteração de foto não tá funcionando, seleciona a foto ali, ela fica como marcada mas não altera no banco de dados.