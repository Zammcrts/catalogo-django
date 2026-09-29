from django.db import models

# Create your models here.
from django.db import models


class Cancion(models.Model):
    spotify_id = models.CharField(max_length=22, unique=True)
    titulo = models.CharField(max_length=300)
    artista = models.CharField(max_length=200)
    album = models.CharField(max_length=300, blank=True)
    genero = models.CharField(max_length=50)
    popularidad = models.PositiveSmallIntegerField(default=0)
    duracion_ms = models.PositiveIntegerField()
    # El CSV mezcla "2019-06-14" con "2012"
    fecha_lanzamiento = models.CharField(max_length=10, blank=True)
    creada_en = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-popularidad"]
        verbose_name_plural = "canciones"

    def __str__(self):
        return f"{self.titulo} ({self.artista})"