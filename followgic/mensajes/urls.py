from django.urls import include, path
from . import views

urlpatterns = [
    path('enviarMensaje/<int:id>/', views.enviarMensaje, name="enviarMensaje"),
    path('mensajes/', views.verMisMensajes, name="verTodosMensajes"),
    path('nuevosMensajes/', views.verMisMensajesNoLeidos, name="mensajesNoLeidos"),
    #path('verMensaje/<int:id>/', views.crearPeticionAmistad, name="crearPeticionAmistad"),
]