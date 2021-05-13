from django.db import models

# Create your models here.
class Localizacion(models.Model):
    latitud = models.DecimalField(verbose_name='latitud', max_digits=9, decimal_places=6)
    longitud = models.DecimalField(verbose_name='longitud', max_digits=9, decimal_places=6)
    direccion = models.TextField(verbose_name='Direccion', max_length=999, blank=True)

    def __str__(self):
        return self.direccion

    class Meta:
        ordering = ('pk', )
