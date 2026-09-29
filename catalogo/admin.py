from django.contrib import admin

from .models import Cancion, Playlist

# Register your models here.

admin.site.register(Cancion)
admin.site.register(Playlist)