# Generated by Django 3.2.18 on 2023-05-08 20:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('employee', '0007_auto_20230508_2021'),
    ]

    operations = [
        migrations.AlterField(
            model_name='employee',
            name='agreement',
            field=models.CharField(choices=[(None, '-'), ('CDI', 'CDI'), ('CDD', 'CDD'), ('Consultant', 'Consultant')], default=None, max_length=10, null=True, verbose_name='Type de contrat'),
        ),
        migrations.AlterField(
            model_name='employee',
            name='branch',
            field=models.CharField(choices=[(None, '-'), ('Kinshasa', 'Kinshasa'), ('Lubumbashi', 'Lubumbashi'), ('Kolwezi', 'Kolwezi'), ('Matadi', 'Matadi'), ('Boma', 'Boma'), ('Moanda', 'Moanda')], max_length=10, verbose_name='Branch'),
        ),
        migrations.AlterField(
            model_name='employee',
            name='payment_method',
            field=models.CharField(choices=[(None, '-'), ('Cash', 'Cash'), ('Banque', 'Banque')], max_length=10, verbose_name='Mode de paiement'),
        ),
        migrations.AlterField(
            model_name='employee',
            name='syndicate',
            field=models.CharField(blank=True, choices=[(None, '-'), ('Syndicat.001', 'Syndicat.001')], default=None, max_length=50, null=True, verbose_name='Syndicat'),
        ),
    ]
