# Generated by Django 2.2.6 on 2022-05-08 03:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Cliente', '0007_usuarios_ultimo_acesso'),
    ]

    operations = [
        migrations.AlterField(
            model_name='usuarios',
            name='ultimo_acesso',
            field=models.DateTimeField(max_length=50),
        ),
    ]
