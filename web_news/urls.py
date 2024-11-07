# web_news_project/urls.py
from django.contrib import admin  # Adicione esta linha
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from trendfeeds import views  # Supondo que o app principal seja 'trendfeeds'

urlpatterns = [
    path('', views.home, name='home'), 
    path('admin/', admin.site.urls),
     # Supondo que você tenha uma view 'home' em trendfeeds.views
]

# Configurações para servir arquivos de mídia em modo de desenvolvimento
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)