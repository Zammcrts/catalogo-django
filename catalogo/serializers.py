from rest_framework import serializers
from .models import Cancion, Playlist

class PlaylistResumenSerializer(serializers.ModelSerializer):
    class Meta:
        model = Playlist
        fields = ['id', 'nombre', 'genero']

class PlaylistSerializer(serializers.ModelSerializer):
    num_canciones = serializers.IntegerField(read_only=True)

    class Meta:
        model = Playlist
        fields = ["id", "playlist_id", "nombre", "genero","subgenero", "num_canciones"]

class CancionSerializer(serializers.ModelSerializer):
    playlists = PlaylistResumenSerializer(many=True, read_only=True)

    #escritura  -> cuando el cleinte manda solo los id de las playlist

    playlist_ids = serializers.PrimaryKeyRelatedField(
        source = "playlists",
        queryset = Playlist.objects.all(),
        many=True,
        write_only=True,
        required=False
    )

    class Meta:
        model = Cancion
        fields = [
        "id", "spotify_id", "titulo", "artista", "album", "popularidad", "duracion_ms", "fecha_lanzamiento", "creada_en", "playlists", "playlist_ids"]

    def validate_popularidad(self, valor):
        if valor > 100 and valor < 0:
            raise serializers.ValidationError("La popularidad debe estar entre 0 y 100")
        return valor