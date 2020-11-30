# Generated by Django 3.1.3 on 2020-11-30 20:12

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Mago',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.TextField(verbose_name='Nombre')),
                ('nombre_artistico', models.TextField(blank=True, verbose_name='Nombre artístico')),
                ('descripcion', models.TextField(verbose_name='Descripción')),
                ('pagina_web', models.TextField(blank=True, verbose_name='Dirección de su página web')),
                ('foto_perfil', models.ImageField(default='default.png', upload_to='', verbose_name='Foto de perfil')),
                ('usuario', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ('pk',),
            },
        ),
    ]
