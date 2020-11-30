from django.urls import include, path
from . import views

urlpatterns = [
    path('magos', views.listarMagos, name="listarMagos"),
]