# catalogo/urls.py (archivo nuevo)
from django.urls import path

from . import views

app_name = "catalogo"

urlpatterns = [
    path("", views.lista_canciones, name="lista"),
    path("canciones/<int:pk>/", views.detalle_cancion, name="detalle"),
    path("playlists/<int:pk>/", views.detalle_playlist, name="playlist_detalle"),
]