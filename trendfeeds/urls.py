from django.contrib import admin  # Certifique-se de que esta linha está presente
from django.urls import path
from . import views  
# Supondo que suas views estão no mesmo app

urlpatterns = [
      path('admin/', admin.site.urls),
      path('', views.home, name='home'),
      path('registro/', views.registro, name='registro'),  # URL para registro
      path('login/', views.login_view, name='login'),      # URL para login
      path('logout/', views.logout_view, name='logout'),   # URL para logout
      # Outras URLs
]