from django.urls import include, path
from . import views

urlpatterns = [
    path('crearLocalizacion/', views.crearLocalizacion, name="crearLocalizacion"),
]