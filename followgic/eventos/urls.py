from django.urls import include, path
from . import views

urlpatterns = [
    path('crearEvento/', views.crearEvento, name="crearEvento"),
    path('listarEventos/', views.listarEventos, name="listarEventos"),
    path('listarEventosCreadosPorMi/', views.verEventosCreadosPorMi, name="verEventosCreadosPorMi"),
    path('listarEventosSubscritos/', views.verEventosSubscritos, name="verEventosSubscritos"),
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
    path('enviarComentario/<int:id>/', views.enviarComentario, name="enviarComentario"),
    path('verUltimoComentarioEvento/<int:id>/', views.verUltimoComentarioEvento, name="verUltimoComentarioEvento"),
    path('verComentariosEvento/<int:id>/', views.verComentariosEvento, name="verComentariosEvento"),
    path('eliminarComentario/<int:id>/', views.eliminarComentario, name="eliminarComentario"),
    path('verMisInvitaciomes/', views.verMisInvitaciones, name="verMisInvitaciones"),
    path('generarCodigo/<str:cadena>/', views.codigoInvitacion, name="codigoInvitacion"),
    path('aceptarInvitacion/<int:cadena>/', views.codigoInvitacion, name="aceptarInvitacion"),
    path('rechazarInvitacion/<int:cadena>/', views.codigoInvitacion, name="rechazarInvitacion"),
    path('usuariosParaInvitar/<int:id_evento>/', views.verUsuariosParaInvitar, name="verUsuariosParaInvitar"),
]