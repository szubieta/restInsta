# Generated by Django 3.0.4 on 2020-03-30 16:19

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('usuarios', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='usuario',
            old_name='seguidores',
            new_name='n_seguidores',
        ),
        migrations.RenameField(
            model_name='usuario',
            old_name='seguidos',
            new_name='n_seguidos',
        ),
        migrations.CreateModel(
            name='Seguidor',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fecha_seguido', models.DateTimeField(auto_now=True, verbose_name='fecha seguido')),
                ('seguido', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='seguido', to=settings.AUTH_USER_MODEL)),
                ('seguidor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='seguidor', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'unique_together': {('seguido', 'seguidor')},
            },
        ),
    ]