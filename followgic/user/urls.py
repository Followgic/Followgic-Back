from django.urls import include, path
from . import views

urlpatterns = [
    path('miPerfil/', views.verMiPerfil, name="miPerfil"),
    path('', include('djoser.urls')),
    path('', include('djoser.urls.authtoken')),
    path('logout/', views.logout.as_view(), name="logout"),
]