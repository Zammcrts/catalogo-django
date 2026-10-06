# config/urls.py (reemplaza el contenido completo del archivo)
from django.contrib import admin
from django.urls import include, path
from rest_framework.routers import DefaultRouter

from catalogo.api_views import CancionViewSet, PlaylistViewSet

router = DefaultRouter()
router.register(r"canciones", CancionViewSet)
router.register(r"playlists", PlaylistViewSet)

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("catalogo.urls")),
    path("api/", include(router.urls)),
    path("api-auth/", include("rest_framework.urls")),
]