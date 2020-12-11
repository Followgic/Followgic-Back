from django.shortcuts import render
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth import login,logout,authenticate
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from user.models import Mago
from user.serializers import MagoProfileSerializer, ImagenMagoSerializer
from rest_framework.authtoken.models import Token
from rest_framework.parsers import FileUploadParser

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def verMiPerfil(request):
    try:
        id_usuario = request.user.id
        mago = Mago.objects.get(pk= id_usuario)
        serializer = MagoProfileSerializer(mago, many=False)
        return Response(serializer.data, status=status.HTTP_200_OK)
    except:
        return Response(
            {"detail": "Usuario no autorizado"},
            status = status.HTTP_401_UNAUTHORIZED
        )

class FileUploadView(APIView):
    parser_class = (FileUploadParser,)
    def post(self, request, *args, **kwargs):
      file_serializer = ImagenMagoSerializer(data=request.data)
      if file_serializer.is_valid():
          file_serializer.save()
          return Response(file_serializer.data, status=status.HTTP_201_CREATED)
      else:
          return Response(file_serializer.errors, status=status.HTTP_400_BAD_REQUEST)