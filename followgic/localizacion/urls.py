from django.urls import include, path
from . import views

urlpatterns = [
    path('crearLocalizacion/', views.crearLocalizacion, name="crearLocalizacion"),
    path('obtenerLocalizacion/<int:id>/', views.obtenerGeoJsonUsuario, name="obtenerLocalizacion"),
    path('obtenerLocalizacionTodosUsuarios/', views.obtenerGeoJsonTodosUsuarios, name="obtenerLocalizacionTodosUsuarios"),
]