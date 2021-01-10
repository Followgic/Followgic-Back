from django.urls import include, path
from . import views

urlpatterns = [
    path('mensajes/', views.verMisMensajes, name="verTodosMensajes"),
    path('misMensajes/', views.verMisMensajesNoLeidos, name="misMensajesNoLeidos"),
    #path('verMensaje/<int:id>/', views.crearPeticionAmistad, name="crearPeticionAmistad"),
]