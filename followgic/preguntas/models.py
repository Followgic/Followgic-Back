from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator

class Pregunta(models.Model):
    enunciado = models.TextField(verbose_name='Enunciado')
    primera_opcion = models.TextField(verbose_name='Primera opción')
    segunda_opcion = models.TextField(verbose_name='Segunda opción')
    tercera_opcion = models.TextField(verbose_name='Tercera opción')
    respuesta_correcta = models.IntegerField(verbose_name='Respuesta correcta', validators=[MinValueValidator(0), MaxValueValidator(2)])
    
    def __str__(self):
        return self.enunciado
    
    class Meta:
        ordering = ('enunciado', )
