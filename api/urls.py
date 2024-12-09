from django.urls import path
from .views import TimeListAPIView, TimeDetailAPIView
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('times/', TimeListAPIView.as_view(), name='time-list'),
    path('times/<int:pk>/', TimeDetailAPIView.as_view(), name='time-detail'),
    
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)