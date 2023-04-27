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
            name='Requisition',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('updated', models.DateTimeField(auto_now=True, verbose_name='Mise à jour le')),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='Créée le')),
                ('name', models.CharField(max_length=150, verbose_name='Nom')),
                ('created_by', django_currentuser.db.models.fields.CurrentUserField(default=django_currentuser.middleware.get_current_authenticated_user, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Créée par')),
            ],
            options={
                'verbose_name': 'Requisition',
            },
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=150, verbose_name='Nom')),
                ('quantity', models.FloatField(default=0.0, verbose_name='Quantite')),
                ('unit', models.CharField(max_length=10, verbose_name='Unite')),
                ('updated', models.DateTimeField(auto_now=True, verbose_name='Mise à jour le')),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='Créée le')),
                ('requisition', models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.SET_NULL, to='logistic.requisition')),
            ],
            options={
                'verbose_name': 'Produit',
            },
        ),
    ]
