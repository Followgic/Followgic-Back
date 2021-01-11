from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator

class Mensaje(models.Model):
    cuerpo = models.TextField(verbose_name='Estado')
    estado = models.IntegerField(verbose_name='Estado', validators=[MinValueValidator(-1), MaxValueValidator(1)])
    fecha = models.DateTimeField(verbose_name='Fecha de creación')
    remitente = models.ForeignKey('user.Mago', on_delete=models.CASCADE, related_name='remitente_mensaje', null=True)
    destinatario = models.ForeignKey('user.Mago', on_delete=models.CASCADE, related_name='destinatario_mensaje', null=True)
    
    def __str__(self):
        return "Mensaje de " + self.remitente.nombre + " a " + self.destinatario.nombre
    
    class Meta:
        ordering = ('estado', '-fecha', '-id', )
