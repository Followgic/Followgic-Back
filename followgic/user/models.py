from django.db import models
from django.contrib.auth.models import User, AbstractUser

class Mago(AbstractUser):

    nombre = models.TextField(verbose_name='Nombre artístico', max_length=255)
    nombre_artistico = models.TextField(verbose_name='Nombre artístico', max_length=255)
    descripcion = models.TextField(verbose_name='Descripción', max_length=255, blank=True)
    email = models.EmailField(verbose_name='Email', max_length=255)
    telefono = models.CharField(verbose_name='Numero de teléfono', max_length=15, blank=True)
    pagina_web = models.TextField(verbose_name='Dirección de su página web', blank=True)
    foto = models.ImageField(upload_to='', verbose_name='Foto de perfil', default='default.png')

    REQUIRED_FIELDS = ['email', 'telefono', 'nombre', 'nombre_artistico', 'descripcion', 'pagina_web', 'foto']

    def __str__(self):
        return self.username
    
    class Meta:
        ordering = ('pk', )
