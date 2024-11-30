from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('perfil/<perfil_id>/', views.info_perfil, name='info_perfil'),
    path('alterar_senha/', views.alterar_senha, name='alterar_senha'),
    path('time_favorito/', views.time_favorito, {'page': 'A'}, name='time_favorito_default'),
    path('time_favorito/<str:page>/', views.time_favorito, name='time_favorito'),
    path('boas_vindas/<str:time_fav>/', views.boas_vindas, name='boas_vindas'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
