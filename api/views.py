from rest_framework import generics
from .models import Time
from .serializers import TimeSerializer

class TimeListAPIView(generics.ListAPIView):
    queryset = Time.objects.all()
    serializer_class = TimeSerializer

class TimeDetailAPIView(generics.RetrieveAPIView):
    queryset = Time.objects.all()
    serializer_class = TimeSerializer
    lookup_field = 'pk'
