# Generated by Django 3.1.3 on 2021-04-06 17:10

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Localizacion',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('latitud', models.DecimalField(decimal_places=6, max_digits=9, verbose_name='latitud')),
                ('longitud', models.DecimalField(decimal_places=6, max_digits=9, verbose_name='longitud')),
                ('direccion', models.TextField(blank=True, max_length=999, verbose_name='Direccion')),
            ],
            options={
                'ordering': ('pk',),
            },
        ),
    ]
