# Generated by Django 3.1.3 on 2021-02-15 16:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('eventos', '0007_invitacion_token'),
    ]

    operations = [
        migrations.AlterField(
            model_name='invitacion',
            name='fecha',
            field=models.DateTimeField(verbose_name='Fecha de creación'),
        ),
    ]