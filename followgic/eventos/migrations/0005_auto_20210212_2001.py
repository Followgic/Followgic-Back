# Generated by Django 3.1.3 on 2021-02-12 19:01

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('eventos', '0004_auto_20210212_1756'),
    ]

    operations = [
        migrations.AddField(
            model_name='evento',
            name='privacidad',
            field=models.IntegerField(default=0, validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(1)], verbose_name='Privacidad del evento'),
        ),
        migrations.AddField(
            model_name='evento',
            name='token',
            field=models.TextField(blank=True, max_length=1500, verbose_name='Token'),
        ),
    ]
