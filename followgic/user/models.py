from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Mago(models.Model):
    usuario = models.OneToOneField(User, on_delete=models.CASCADE, null=False)
    nombre = models.TextField(verbose_name='Nombre')
    nombre_artistico = models.TextField(verbose_name='Nombre artístico', blank=True)
    descripcion = models.TextField(verbose_name='Descripción')
    pagina_web = models.TextField(verbose_name='Dirección de su página web', blank=True)
    foto_perfil = models.ImageField(upload_to='', verbose_name='Foto de perfil', default='default.png')

    def __str__(self):
        return self.usuario.username
    
    class Meta:
        ordering = ('pk', )