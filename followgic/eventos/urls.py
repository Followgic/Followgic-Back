from django.urls import include, path
from . import views

urlpatterns = [
    path('crearEvento/', views.crearEvento, name="crearEvento"),
    path('listarEventos/', views.listarEventos, name="listarEventos"),
    path('verEvento/<int:id>/', views.verEvento, name="verEvento"),
    path('setImagenverEvento/<int:id>/', views.setImagenEvento, name="setImagenverEvento"),
    path('inscribirseEvento/<int:id>/', views.inscribirseEvento, name="inscribirseEvento"),
    path('cancelarInscripcionEvento/<int:id>/', views.cancelarInscripcionEvento, name="cancelarInscripcionEvento"),
    path('verMagosInscritosPorEvento/<int:id>/', views.verMagosInscritosPorEvento, name="verMagosInscritosPorEvento"),
    path('eliminarAsistenteEvento/<int:id_evento>/<int:id_usuario>/', views.eliminarAsistenteEvento, name="eliminarAsistenteEvento"),
    path('editarEvento/<int:id>/', views.editarEvento, name="editarEvento"),
    path('eliminarEvento/<int:id>/', views.eliminarEvento, name="eliminarEvento"),
    path('silenciarEvento/<int:id>/', views.silenciarEvento, name="silenciarEvento"),
    path('habilitarMensajesEvento/<int:id>/', views.habilitarMensajesEvento, name="habilitarMensajesEvento"),
]