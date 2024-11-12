from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, include

urlpatterns = [
    path('', include('trendfeeds.urls')),  # Inclui as rotas do app locadora
    path('', include('users.urls')),  # Inclui as rotas do app users
]

# Adiciona URLs para arquivos de mídia em desenvolvimento
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)