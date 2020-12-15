from django.urls import include, path
from . import views

urlpatterns = [
    path('miPerfil/', views.verMiPerfil, name="miPerfil"),
    path('', include('djoser.urls')),
    path('', include('djoser.urls.authtoken')),
    path('modalidades/', views.getModalidades, name="modalidades"),
    path('setImagen/', views.setImagenMago, name="setImagenMago"),
    path('listadoMagos/', views.listadoMagos, name="listadoMagos"),
    path('verPerfil/<int:id>/', views.verPerfilMago, name="verPerfilMago"),
    path('amigos/', views.verMisAmigos, name="misAmigos"),
]