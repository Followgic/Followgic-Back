from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework import status
from .models import *
from .serializers import crearLocalizacionSerializer
from rest_framework.parsers import JSONParser
from user.models import Mago
from user.serializers import listadoMagosSerializer

@api_view(['POST'])
def crearLocalizacion(request):
    try:
        data = JSONParser().parse(request)
        serializer = crearLocalizacionSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=201)
        return JsonResponse(serializer.errors, status=400)
    except:
       return Response(
           {"detail": "Localizacion no valida"},
           status = status.HTTP_400_BAD_REQUEST
       )
       
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def obtenerGeoJsonUsuario(request, id):
    try:
        assert request.user.id != id
        mago = Mago.objects.get(pk= id)
        localizacion = mago.localizacion
        geoJson = {
                "type": "Feature",
                "geometry": {
                    "type": "Point",
                    "coordinates": [localizacion.longitud,localizacion.latitud] 
                },
                "properties": {
                    "name": localizacion.direccion
                }
            }
        return Response(
            {"geoJson": geoJson}  
        )
    except:
       return Response(
           {"detail": "Localizacion no valida"},
           status = status.HTTP_400_BAD_REQUEST
       )

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def obtenerGeoJsonTodosUsuarios(request):
    try:
        magos = Mago.objects.exclude(localizacion__isnull=True)
        # serializer = listadoMagosSerializer(magos, many=True)
        geoJson = {
                "type": "FeatureCollection",
                "features": [
                {
                    "type": "Feature",
                    "geometry" : {
                        "type": "Point",
                        "coordinates": [m.localizacion.longitud, m.localizacion.latitud],
                    },
                    "properties": {
                        "name": m.localizacion.direccion
                    }
                } for m in magos.all()]    
            }
        return Response(
            {"geoJson": geoJson}
        )
    except:
       return Response(
           {"detail": "Localizacion no valida"},
           status = status.HTTP_400_BAD_REQUEST
       )