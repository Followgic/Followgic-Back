from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db.models.signals import post_save
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer



class Peticion(models.Model):
    estado = models.IntegerField(verbose_name='Estado', validators=[
                                 MinValueValidator(-1), MaxValueValidator(1)])
    fecha = models.DateField(verbose_name='Fecha de creación')
    remitente = models.ForeignKey(
        'user.Mago', on_delete=models.CASCADE, related_name='remitente', null=True)
    destinatario = models.ForeignKey(
        'user.Mago', on_delete=models.CASCADE, related_name='destinatario', null=True)

    def __str__(self):
        return "Petición de amistad de " + self.remitente.nombre + " a " + self.destinatario.nombre

    class Meta:
        ordering = ('fecha', )


def crear_grupo_notificacion(sender, instance, **kwargs):
    # Conseguimos la peticion
    id_peticion = instance.pk
    peticion = Peticion.objects.get(pk=id_peticion)

    if(peticion.estado == 0):
        print(peticion)
        channel_layer = get_channel_layer()
        # Nombre del grupo // peticion_sergio
        nombre_grupo = "peticion_{}".format(peticion.destinatario.username)
        print(nombre_grupo)

        async_to_sync(channel_layer.group_send)(
            nombre_grupo, {"type": "broadcast_notification_message",
                           "message": "hola sergio"
                           }
        )
    else:
        print('No se ha creado la peticion de amistad')


post_save.connect(crear_grupo_notificacion, sender=Peticion)
