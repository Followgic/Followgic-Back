from django.db import models
from django.contrib.auth.models import User, AbstractUser

class Modalidad(models.Model):
    nombre = models.TextField(verbose_name='Nombre')

    def __str__(self):
        return self.nombre
    
    class Meta:
        ordering = ('pk', )


class Mago(AbstractUser):
    nombre = models.TextField(verbose_name='Nombre artístico', max_length=255)
    nombre_artistico = models.TextField(verbose_name='Nombre artístico', max_length=255)
    descripcion = models.TextField(verbose_name='Descripción', max_length=1500, blank=True)
    email = models.EmailField(verbose_name='Email', max_length=255)
    telefono = models.CharField(verbose_name='Numero de teléfono', max_length=15, blank=True)
    pagina_web = models.TextField(verbose_name='Dirección de su página web', blank=True)
    foto = models.ImageField(upload_to='', verbose_name='Foto de perfil', default='default.png')
    modalidades = models.ManyToManyField('Modalidad', blank=True)
    amigos = models.ManyToManyField('Mago', blank=True)

    REQUIRED_FIELDS = ['email', 'telefono', 'nombre', 'nombre_artistico', 'descripcion', 'pagina_web', 'foto', 'modalidades', 'amigos']

    def __str__(self):
        return self.username
    
    class Meta:
        ordering = ('pk', )
