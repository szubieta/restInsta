# Generated by Django 3.0.4 on 2020-05-07 09:19

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('publicaciones', '0002_publicacion_is_liked'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='publicacion',
            name='is_liked',
        ),
    ]
