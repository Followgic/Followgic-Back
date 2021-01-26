from django.urls import include, path
from . import views

urlpatterns = [
    path('enviarMensaje/<int:id>/', views.enviarMensaje, name="enviarMensaje"),
    path('mensajes/', views.verMisMensajes, name="verTodosMensajes"),
    path('nuevosMensajes/', views.verMisMensajesNoLeidos, name="mensajesNoLeidos"),
    path('verConversacion/<int:id>/', views.verConversacion, name="verConversacion"),
    path('verConversacionPorMago/<int:id>/', views.verConversacionPorMago, name="verConversacionPorMago"),
    path('eliminarMensaje/<int:id>/', views.eliminarMensaje, name="eliminarMensaje"),
]