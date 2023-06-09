# Generated by Django 3.2.18 on 2023-04-27 12:18

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django_currentuser.db.models.fields
import django_currentuser.middleware
import social.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='FundRequest',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('updated', models.DateTimeField(auto_now=True, verbose_name='Mise à jour le')),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='Créée le')),
                ('description', models.TextField(default='-', verbose_name='Description')),
                ('doc', models.FileField(default=None, null=True, upload_to=social.models.upload_directory_file, verbose_name='Document')),
                ('created_by', django_currentuser.db.models.fields.CurrentUserField(default=django_currentuser.middleware.get_current_authenticated_user, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Créée par')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
