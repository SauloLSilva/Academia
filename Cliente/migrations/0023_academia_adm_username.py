# Generated by Django 2.2.6 on 2022-06-11 11:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Cliente', '0022_auto_20220610_1044'),
    ]

    operations = [
        migrations.AddField(
            model_name='academia_adm',
            name='username',
            field=models.CharField(default=1, max_length=30, unique=True),
            preserve_default=False,
        ),
    ]
