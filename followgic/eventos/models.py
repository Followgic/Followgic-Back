from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator

class Comentario(models.Model):
    cuerpo = models.TextField(verbose_name='Cuerpo', max_length=1500)
    fecha = models.DateField(verbose_name='Fecha de creación')
    remitente = models.ForeignKey('user.Mago', on_delete=models.CASCADE, null=True)

    def __str__(self):
        return "Comentario de " + self.remitente.nombre

    class Meta:
        ordering = ('fecha', 'pk', )

class Evento(models.Model):
    titulo = models.TextField(verbose_name='Titulo')
    tipo = models.IntegerField(verbose_name='Tipo de evento', validators=[MinValueValidator(0), MaxValueValidator(1)])
    link_conferencia = models.URLField(verbose_name='Url de la conferencia', max_length = 200, blank=True) 
    descripcion = models.TextField(verbose_name='Descripción', max_length=1500, blank=True)
    fecha_creacion = models.DateField(verbose_name='Fecha de creación')
    fecha_evento = models.DateField(verbose_name='Fecha del evento')
    hora_evento = models.TimeField(verbose_name='Hora del evento', null=True)
    aforo = models.PositiveIntegerField(verbose_name='Aforo del evento', validators=[MinValueValidator(2)])
    foto = models.ImageField(upload_to='', verbose_name='Foto del evento', default='default.png')
    creador = models.ForeignKey('user.Mago', on_delete=models.CASCADE, related_name='creador', null=True)
    asistentes = models.ManyToManyField('user.Mago', related_name='asistentes', blank=True)
    modalidades = models.ManyToManyField('user.Modalidad', blank=True)
    comentarios = models.ManyToManyField('Comentario', blank=True)

    def __str__(self):
        return self.titulo
    
    class Meta:
        ordering = ('fecha_evento', 'titulo', 'pk', )