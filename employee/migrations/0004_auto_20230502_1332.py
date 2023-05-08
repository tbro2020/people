# Generated by Django 3.2.18 on 2023-05-02 13:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('employee', '0003_auto_20230430_1752'),
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
            field=models.CharField(choices=[(None, '-'), ('Kinshasa', 'Kinshasa'), ('Lubumbashi', 'Lubumbashi'), ('Bukavu', 'Bukavu'), ('Likasi', 'Likasi'), ('Kolwezi', 'Kolwezi'), ('Matadi', 'Matadi'), ('Goma', 'Goma'), ('Kalemie', 'Kalemie'), ('Boma', 'Boma'), ('Moanda', 'Moanda')], max_length=10, verbose_name='Branch'),
        ),
        migrations.AlterField(
            model_name='employee',
            name='payment_method',
            field=models.CharField(choices=[(None, '-'), ('Banque', 'Banque'), ('Cash', 'Cash')], max_length=10, verbose_name='Mode de paiement'),
        ),
    ]