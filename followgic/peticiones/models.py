from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator

class Peticion(models.Model):
    estado = models.IntegerField(verbose_name='Estado', validators=[MinValueValidator(-1), MaxValueValidator(1)])
    fecha = models.DateField(verbose_name='Fecha de creación')
    remitente = models.ForeignKey('user.Mago', on_delete=models.CASCADE, related_name='remitente', null=True)
    destinatario = models.ForeignKey('user.Mago', on_delete=models.CASCADE, related_name='destinatario', null=True)
    
    def __str__(self):
        return "Petición de amistad de " + self.remitente.nombre + " a " + self.destinatario.nombre
    
    class Meta:
        ordering = ('fecha', )
