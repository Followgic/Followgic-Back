from django.urls import include, path
from . import views

urlpatterns = [
    path('crearEvento/', views.crearEvento, name="crearEvento"),
    path('listarEventos/', views.listarEventos, name="listarEventos"),
    path('verEvento/<int:id>/', views.verEvento, name="verEvento"),
]