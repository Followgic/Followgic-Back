from django.urls import include, path
from . import views

urlpatterns = [
    path('misNotificaciones/', views.verMisPeticionesPendientes, name="misPeticionesPendientes"),
    path('crearSolicitudAmistad/<int:id>/', views.crearPeticionAmistad, name="crearPeticionAmistad"),
    path('rechazarSolicitud/<int:id>/', views.rechazarPeticionAmistad, name="rechazarSolicitudAmistad"),
    path('cancelarSolicitud/<int:id>/', views.cancelarPeticionAmistad, name="cancelarPeticionAmistad"),
    path('aceptarSolicitud/<int:id>/', views.aceptarPeticionAmistad, name="aceptarSolicitudAmistad"),
    path('eliminarAmigo/<int:id>/', views.eliminarAmigo, name="eliminarAmigo"),
    path('peticionesPendientes/', views.usuariosConPeticionesPendientes, name="peticionesPendientes"),
    path('peticionPendienteConUsuario/<int:id>/', views.peticionPendienteConUsuario, name="peticionPendienteConUsuario"),
]