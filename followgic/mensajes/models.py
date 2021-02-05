from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator

from django.db.models.signals import post_save, post_delete,pre_delete
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer


class Mensaje(models.Model):
    cuerpo = models.TextField(verbose_name='Cuerpo', max_length=1500)
    estado = models.IntegerField(verbose_name='Estado', validators=[MinValueValidator(-1), MaxValueValidator(1)])
    fecha = models.DateTimeField(verbose_name='Fecha de creación')
    remitente = models.ForeignKey('user.Mago', on_delete=models.CASCADE, related_name='remitente_mensaje', null=True)
    destinatario = models.ForeignKey('user.Mago', on_delete=models.CASCADE, related_name='destinatario_mensaje', null=True)
    
    def __str__(self):
        return "Mensaje de " + self.remitente.nombre + " a " + self.destinatario.nombre
    
    class Meta:
        ordering = ('estado', '-fecha', '-pk', )


def crear_grupo_mensaje(sender, instance, **kwargs):
    id_mensaje = instance.pk
    mensaje = Mensaje.objects.get(pk=id_mensaje)

    

    if(mensaje.estado == 0):
        channel_layer = get_channel_layer()
        nombre_destinatario = "canal_{}".format(mensaje.destinatario.username)
        
       
        
        async_to_sync(channel_layer.group_send)(
            nombre_destinatario, {"type": "broadcast_notification_message",
                           "message": "Mensaje remitente " + str(mensaje.remitente.pk)
                           }
        )
    elif(mensaje.estado == 1):
        channel_layer = get_channel_layer()
        nombre_destinatario = "canal_{}".format(mensaje.remitente.username)
        

        async_to_sync(channel_layer.group_send)(
            nombre_destinatario, {"type": "broadcast_notification_message",
                           "message": "Mensaje destinatario " + str(mensaje.destinatario.pk)
                           }
        )

    



def eliminar_mensaje(sender, instance, **kwargs):
    id_mensaje = instance.pk
    mensaje = Mensaje.objects.get(pk=id_mensaje)

    


    channel_layer = get_channel_layer()
    nombre_destinatario = "canal_{}".format(mensaje.destinatario.username)
    
    
    
    async_to_sync(channel_layer.group_send)(
        nombre_destinatario, {"type": "broadcast_notification_message",
                        "message": "Mensaje remitente " + str(mensaje.remitente.pk)
                        }
    )
   

    

    


   
post_save.connect(crear_grupo_mensaje, sender=Mensaje)

pre_delete.connect(eliminar_mensaje, sender=Mensaje)
