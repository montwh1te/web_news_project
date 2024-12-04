from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, include

urlpatterns = [
    # Inclui as rotas do app trendfeeds
    path('', include('trendfeeds.urls')), 

    # Inclui as rotas do app users
    path('', include('users.urls')), 

    # Inclui as rotas do app api 
    path('api/', include('api.urls')) 
]

# Adiciona URLs para arquivos de mídia em desenvolvimento
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)