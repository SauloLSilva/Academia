# Generated by Django 2.2.6 on 2022-06-10 10:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Cliente', '0019_academia_adm_is_superuser'),
    ]

    operations = [
        migrations.AddField(
            model_name='academia_adm',
            name='is_staff',
            field=models.BooleanField(default=False),
        ),
    ]
