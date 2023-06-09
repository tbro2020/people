# Generated by Django 3.2.18 on 2023-04-27 10:04

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django_currentuser.db.models.fields
import django_currentuser.middleware


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Exit',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('updated', models.DateTimeField(auto_now=True, verbose_name='Mise à jour le')),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='Créée le')),
                ('exit_time', models.TimeField(help_text='HH:MM:SS', verbose_name='Heure de sortie')),
                ('reason', models.TextField(verbose_name='Motif de sortie')),
                ('destination', models.CharField(max_length=250, verbose_name='Destination')),
                ('return_time', models.TimeField(help_text='HH:MM:SS', verbose_name='Heure de retour')),
                ('observation', models.TextField(verbose_name='Observation')),
                ('created_by', django_currentuser.db.models.fields.CurrentUserField(default=django_currentuser.middleware.get_current_authenticated_user, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Créée par')),
            ],
            options={
                'verbose_name': 'Bon de sortie',
            },
        ),
    ]
