# config/urls.py (reemplaza el contenido completo del archivo)
from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("catalogo.urls")),
]