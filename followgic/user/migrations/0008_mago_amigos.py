# Generated by Django 3.1.3 on 2020-12-14 20:33

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0007_auto_20201214_2017'),
    ]

    operations = [
        migrations.AddField(
            model_name='mago',
            name='amigos',
            field=models.ManyToManyField(blank=True, to=settings.AUTH_USER_MODEL),
        ),
    ]
