# Generated by Django 2.2.6 on 2022-06-10 10:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Cliente', '0020_academia_adm_is_staff'),
    ]

    operations = [
        migrations.AddField(
            model_name='academia_adm',
            name='has_module_perms',
            field=models.BooleanField(default=False),
        ),
    ]