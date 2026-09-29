# catalogo/management/commands/cargar_csv.py
import csv

from django.core.management.base import BaseCommand

from catalogo.models import Cancion, Playlist


def entero(valor, defecto=0):
    """Convierte a int; si la celda viene vacía, usa el valor por defecto."""
    return int(valor) if valor.strip() else defecto


class Command(BaseCommand):
    help = "Carga el CSV de canciones de Spotify en Cancion y Playlist"

    def add_arguments(self, parser):
        parser.add_argument("ruta", help="Ruta al archivo CSV")

    def handle(self, *args, **opts):
        canciones, playlists, relaciones = {}, {}, set()

        # 1. Leer y deduplicar en memoria (todavía no hay ningún INSERT)
        with open(opts["ruta"], encoding="utf-8", newline="") as f:
            for fila in csv.DictReader(f):
                canciones.setdefault(fila["track_id"], Cancion(
                    spotify_id=fila["track_id"],
                    titulo=fila["track_name"],
                    artista=fila["track_artist"],
                    album=fila["track_album_name"],
                    popularidad=entero(fila["track_popularity"]),
                    duracion_ms=entero(fila["duration_ms"]),
                    fecha_lanzamiento=fila["track_album_release_date"],
                ))
                playlists.setdefault(fila["playlist_id"], Playlist(
                    playlist_id=fila["playlist_id"],
                    nombre=fila["playlist_name"],
                    genero=fila["playlist_genre"],
                    subgenero=fila["playlist_subgenre"],
                ))
                relaciones.add((fila["track_id"], fila["playlist_id"]))

        # 2. Insertar por lotes
        Cancion.objects.bulk_create(canciones.values(), batch_size=1000, ignore_conflicts=True)
        Playlist.objects.bulk_create(playlists.values(), batch_size=1000, ignore_conflicts=True)

        # 3. Traducir spotify_id y playlist_id a los id internos y llenar la tabla intermedia
        ids_c = dict(Cancion.objects.values_list("spotify_id", "id"))
        ids_p = dict(Playlist.objects.values_list("playlist_id", "id"))
        Rel = Cancion.playlist.through
        Rel.objects.bulk_create(
            [Rel(cancion_id=ids_c[c], playlist_id=ids_p[p]) for c, p in relaciones],
            batch_size=2000,
            ignore_conflicts=True,
        )

        self.stdout.write(self.style.SUCCESS(
            f"{len(canciones)} canciones, {len(playlists)} playlists, {len(relaciones)} relaciones"
        ))