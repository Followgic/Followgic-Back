from django.shortcuts import render
from rest_framework.response import Response
from rest_framework import status
from .models import *
from .serializers import *
from rest_framework.decorators import api_view

@api_view(['GET'])
def obtenerPreguntas(request):
    try:
        preguntas = Pregunta.objects.order_by('?')[:1]
        serializer = listarPreguntasSerializer(preguntas, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    except:
        return Response(
            {"detail": "Preguntas no encontradas"},
            status = status.HTTP_204_NO_CONTENT
        )
