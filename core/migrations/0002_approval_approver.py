# Generated by Django 3.2.18 on 2023-04-27 12:38

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('employee', '0001_initial'),
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Approver',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('model', models.CharField(choices=[], max_length=30, verbose_name='Model')),
                ('updated', models.DateTimeField(auto_now=True, verbose_name='Mise à jour le')),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='Créée le')),
                ('employee', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='employee.employee', verbose_name='Employee')),
            ],
            options={
                'verbose_name': 'Approbateur',
            },
        ),
        migrations.CreateModel(
            name='Approval',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('model', models.CharField(choices=[], max_length=30, verbose_name='Model')),
                ('_pk', models.IntegerField(verbose_name='Identifiant unique')),
                ('updated', models.DateTimeField(auto_now=True, verbose_name='Mise à jour le')),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='Créée le')),
                ('approved_by', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='employee.employee', verbose_name='Employee')),
            ],
            options={
                'verbose_name': 'Approbation',
            },
        ),
    ]
