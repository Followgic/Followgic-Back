from django.urls import include, path
from . import views

urlpatterns = [
    path('misNotificaciones/', views.verMisPeticionesPendientes, name="misPeticionesPendientes"),
    path('crearSolicitudAmistad/<int:id>/', views.crearPeticionAmistad, name="crearPeticionAmistad"),
]