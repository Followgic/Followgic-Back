# Generated by Django 3.1.3 on 2021-04-06 17:23

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('localizacion', '0001_initial'),
        ('user', '0008_mago_amigos'),
    ]

    operations = [
        migrations.AddField(
            model_name='mago',
            name='localizacion',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='localizacion', to='localizacion.localizacion'),
        ),
    ]
