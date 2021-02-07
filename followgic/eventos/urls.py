from django.urls import include, path
from . import views

urlpatterns = [
    path('crearEvento/', views.crearEvento, name="crearEvento"),
    path('listarEventos/', views.listarEventos, name="listarEventos"),
    path('verEvento/<int:id>/', views.verEvento, name="verEvento"),
    path('setImagenverEvento/<int:id>/', views.setImagenEvento, name="setImagenverEvento"),
    path('inscribirseEvento/<int:id>/', views.inscribirseEvento, name="inscribirseEvento"),
    path('desuscribirseEvento/<int:id>/', views.desuscribirseEvento, name="desuscribirseEvento"),
]