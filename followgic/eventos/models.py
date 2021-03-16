from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db.models.signals import post_save, post_delete,pre_delete
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer

class Invitacion(models.Model):
    estado = models.IntegerField(verbose_name='Estado', validators=[MinValueValidator(0), MaxValueValidator(1)])
    fecha = models.DateTimeField(verbose_name='Fecha de creación')
    token = models.TextField(verbose_name='Token', max_length=1500, blank=True)
    evento = models.ForeignKey('Evento', on_delete=models.CASCADE, related_name='evento', null=True)
    destinatario = models.ForeignKey('user.Mago', on_delete=models.CASCADE, related_name='invitado', null=True)

    def __str__(self):
        return "Invitación a " + self.evento.titulo

    class Meta:
        ordering = ('fecha', 'pk', )

class Comentario(models.Model):
    cuerpo = models.TextField(verbose_name='Cuerpo', max_length=1500)
    fecha = models.DateTimeField(verbose_name='Fecha de creación')
    remitente = models.ForeignKey('user.Mago', related_name='usuario', on_delete=models.CASCADE, null=True)
    evento = models.ForeignKey('Evento', on_delete=models.CASCADE, related_name='evento_comentario', null=True)
    leidos = models.ManyToManyField('user.Mago', related_name='lectores', blank=True)

    def __str__(self):
        return "Comentario de " + self.remitente.nombre

    class Meta:
        ordering = ('fecha', 'pk', )

class Evento(models.Model):
    titulo = models.TextField(verbose_name='Titulo')
    tipo = models.IntegerField(verbose_name='Tipo de evento', validators=[MinValueValidator(0), MaxValueValidator(1)])
    privacidad = models.IntegerField(verbose_name='Privacidad del evento', validators=[MinValueValidator(0), MaxValueValidator(1)], default= 0)
    token = models.TextField(verbose_name='Token', max_length=1500, blank=True)
    link_conferencia = models.URLField(verbose_name='Url de la conferencia', max_length = 200, blank=True) 
    descripcion = models.TextField(verbose_name='Descripción', max_length=1500, blank=True)
    fecha_creacion = models.DateField(verbose_name='Fecha de creación')
    fecha_evento = models.DateField(verbose_name='Fecha del evento')
    hora_evento = models.TimeField(verbose_name='Hora del evento', null=True)
    aforo = models.PositiveIntegerField(verbose_name='Aforo del evento', validators=[MinValueValidator(2)])
    foto = models.ImageField(upload_to='', verbose_name='Foto del evento', default='default_eventos.jpg')
    creador = models.ForeignKey('user.Mago', on_delete=models.CASCADE, related_name='creador', null=True)
    asistentes = models.ManyToManyField('user.Mago', related_name='asistentes', blank=True)
    usuarios_activos = models.ManyToManyField('user.Mago', related_name='activos', blank=True)
    modalidades = models.ManyToManyField('user.Modalidad', blank=True)
    comentarios = models.ManyToManyField('Comentario', related_name='comentarios_evento', blank=True)

    def __str__(self):
        return self.titulo
    
    class Meta:
        ordering = ('fecha_evento', 'titulo', 'pk', )


    
def crear_grupo_comentario(sender, instance, **kwargs):
    id_comentario = instance.pk
    comentario = Comentario.objects.get(pk=id_comentario)
    print(comentario.evento)
    channel_layer = get_channel_layer()
    print(sender)
    
    for asistente in comentario.evento.usuarios_activos.all():
        if(comentario.remitente != asistente):
           
            
            nombre_destinatario = "canal_{}".format(asistente.username)

            async_to_sync(channel_layer.group_send)(
                nombre_destinatario, {"type": "broadcast_notification_message",
                            "message": "Comentario remitente " + str(comentario.evento.pk)
                            }
            )

    
def crear_grupo_invitacion(sender, instance, **kwargs):
    id_invitacion = instance.pk
    invitacion = Invitacion.objects.get(pk=id_invitacion)

    channel_layer = get_channel_layer()

    if(invitacion.estado==0):
        nombre_destinatario = "canal_{}".format(invitacion.destinatario.username)

        async_to_sync(channel_layer.group_send)(
            nombre_destinatario, {"type": "broadcast_notification_message",
                        "message": "Invitacion remitente " + str(invitacion.evento.creador.pk)
                        }
        )

    if(invitacion.estado==1):
        nombre_creador_evento = "canal_{}".format(invitacion.evento.creador.username)

        async_to_sync(channel_layer.group_send)(
            nombre_creador_evento, {"type": "broadcast_notification_message",
                        "message": "Invitacion aceptada " + str(invitacion.evento.pk)
                        }
        )

def crear_grupo_invitacion_eliminar(sender, instance, **kwargs):
    print(sender)
    id_invitacion = instance.pk
    invitacion = Invitacion.objects.get(pk=id_invitacion)

    channel_layer = get_channel_layer()

    if(invitacion.estado==0):
        nombre_creador_evento = "canal_{}".format(invitacion.evento.creador.username)

        async_to_sync(channel_layer.group_send)(
            nombre_creador_evento, {"type": "broadcast_notification_message",
                        "message": "Invitacion rechazada " + str(invitacion.evento.pk)
                        }
        )
   


post_save.connect(crear_grupo_comentario, sender=Comentario)
post_save.connect(crear_grupo_invitacion, sender=Invitacion)
pre_delete.connect(crear_grupo_invitacion_eliminar, sender=Invitacion)