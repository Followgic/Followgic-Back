from django.urls import include, path
from . import views

urlpatterns = [
    path('miPerfil/', views.verMiPerfil, name="miPerfil"),
]