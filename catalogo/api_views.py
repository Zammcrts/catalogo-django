from django.db.models import Count, Q
from rest_framework import viewsets

from .models import Cancion, Playlist
from .serializers import CancionSerializer, PlaylistSerializer


class CancionViewSet(viewsets.ModelViewSet):
    queryset = Cancion.objects.all().order_by("titulo", "id")
    serializer_class = CancionSerializer

    def get_queryset(self):
        qs = super().get_queryset().prefetch_related("playlist")

        # Los filtros solo aplican al listado, no al detalle/edición/borrado
        if self.action != "list":
            return qs

        params = self.request.query_params
        q = params.get("q", "").strip()
        genero = params.get("genero", "").strip()
        artista = params.get("artista", "").strip()

        if q:
            qs = qs.filter(Q(titulo__icontains=q) | Q(artista__icontains=q))
        if artista:
            qs = qs.filter(artista=artista)
        if genero:
            qs = qs.filter(playlist__genero=genero).distinct()
        return qs

class PlaylistViewSet(viewsets.ModelViewSet):
    queryset = (
        Playlist.objects.annotate(num_canciones=Count("canciones"))
        .order_by("nombre")
    )
    serializer_class = PlaylistSerializer