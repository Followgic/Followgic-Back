# Generated by Django 3.1.3 on 2020-12-12 14:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0004_auto_20201211_1733'),
    ]

    operations = [
        migrations.CreateModel(
            name='Modalidad',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.TextField(verbose_name='Nombre')),
            ],
            options={
                'ordering': ('pk',),
            },
        ),
        migrations.AddField(
            model_name='mago',
            name='modalidades',
            field=models.ManyToManyField(to='user.Modalidad'),
        ),
    ]
