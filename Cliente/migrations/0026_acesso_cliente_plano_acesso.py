# Generated by Django 2.2.6 on 2022-06-18 12:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Cliente', '0025_auto_20220618_1213'),
    ]

    operations = [
        migrations.AddField(
            model_name='acesso_cliente',
            name='plano_acesso',
            field=models.CharField(default=1, max_length=13),
            preserve_default=False,
        ),
    ]
