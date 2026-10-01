from django.core.paginator import Paginator
from django.db import connection
from django.db.models import Q
from django.shortcuts import get_object_or_404, render

from .models import Cancion, Playlist


def lista_canciones(request):
    q = request.GET.get("q", "").strip()
    genero = request.GET.get("genero", "").strip()
    artista = request.GET.get("artista", "").strip()

    canciones = Cancion.objects.all().order_by("titulo", "id")
    if q:
        canciones = canciones.filter(Q(titulo__icontains=q) | Q(artista__icontains=q))
    if artista:
        canciones = canciones.filter(artista=artista)
    if genero:
        canciones = canciones.filter(playlist__genero=genero).distinct()

    canciones = canciones.prefetch_related("playlist")

    generos = (
        Playlist.objects.values_list("genero", flat=True)
        .distinct()
        .order_by("genero")
    )

    paginator = Paginator(canciones, 25)
    page_obj = paginator.get_page(request.GET.get("page"))

    contexto = {
        "page_obj": page_obj,
        "total": paginator.count,
        "q": q,
        "genero": genero,
        "artista": artista,
        "generos": generos,
    }

    try:
        respuesta = render(request, "catalogo/lista.html", contexto)
    finally:
        print("Consultas:", len(connection.queries))
    return respuesta


def detalle_cancion(request, pk):
    cancion = get_object_or_404(Cancion, pk=pk)
    return render(request, "catalogo/detalle.html", {"cancion": cancion})


def detalle_playlist(request, pk):
    playlist = get_object_or_404(Playlist, pk=pk)
    canciones = playlist.canciones.all().order_by("-popularidad", "titulo")
    return render(
        request,
        "catalogo/playlist_detalle.html",
        {"playlist": playlist, "canciones": canciones},
    )