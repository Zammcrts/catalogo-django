from django.db import models

# Create your models here.
from django.db import models

class Playlist(models.Model):
    playlist_id = models.CharField(max_length=22, unique=True)
    nombre = models.CharField(max_length=300)
    genero = models.CharField(max_length=50)
    subgenero = models.CharField(max_length=80, blank=True)

    def __str__(self):
        return self.nombre

class Cancion(models.Model):
    spotify_id = models.CharField(max_length=22, unique=True)
    titulo = models.CharField(max_length=300)
    artista = models.CharField(max_length=200, db_index=True) #se añadio db_index=True para mejorar la búsqueda por artista
    album = models.CharField(max_length=300, blank=True)
    #genero = models.CharField(max_length=50)
    popularidad = models.PositiveSmallIntegerField(default=0)
    duracion_ms = models.PositiveIntegerField()
    # El CSV mezcla "2019-06-14" con "2012"
    fecha_lanzamiento = models.CharField(max_length=10, blank=True)
    creada_en = models.DateTimeField(auto_now_add=True)
    playlist = models.ManyToManyField(Playlist, related_name="canciones")

    class Meta:
        ordering = ["-popularidad"]
        verbose_name_plural = "canciones"

    def __str__(self):
        return f"{self.titulo} ({self.artista})"
        # catalogo/models.py (dentro de la clase Cancion, después de __str__)
    @property
    def duracion(self):
        minutos, segundos = divmod(self.duracion_ms // 1000, 60)
        return f"{minutos}:{segundos:02d}"
        