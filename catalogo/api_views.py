from django.db.models import Count
from rest_framework import viewsets

from .models import Cancion, Playlist
from .serializers import CancionSerializer, PlaylistSerializer

class CancionViewSet(viewsets.ModelViewSet):
    queryset = Cancion.objects.all()
    serializer_class = CancionSerializer

class PlaylistViewSet(viewsets.ModelViewSet):
    queryset = (
        
        Playlist.objects.annotate(num_canciones=Count("canciones"))
        .order_by("nombre")
    )
    serializer_class = PlaylistSerializer