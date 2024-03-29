# Generated by Django 3.1.3 on 2021-01-04 16:14

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Pregunta',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('enunciado', models.TextField(verbose_name='Enunciado')),
                ('primera_opcion', models.TextField(verbose_name='Primera opción')),
                ('segunda_opcion', models.TextField(verbose_name='Segunda opción')),
                ('tercera_opcion', models.TextField(verbose_name='Tercera opción')),
                ('respuesta_correcta', models.IntegerField(validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(2)], verbose_name='Respuesta correcta')),
            ],
            options={
                'ordering': ('enunciado',),
            },
        ),
    ]
