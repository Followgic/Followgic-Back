from django.urls import include, path
from . import views

urlpatterns = [
    path('crearLocalizacion/', views.crearLocalizacion, name="crearLocalizacion"),
    path('editarLocalizacion/<int:id>/', views.editarLocalizacion, name="editarLocalizacion"),
    path('obtenerLocalizacion/', views.obtenerGeoJsonUsuario, name="obtenerLocalizacion"),
    path('obtenerLocalizacionTodosUsuarios/', views.obtenerGeoJsonTodosUsuarios, name="obtenerLocalizacionTodosUsuarios"),
    path('obtenerLocalizacionTodosEventos/', views.obtenerGeoJsonTodosEventos, name="obtenerGeoJsonTodosEventos"),
]