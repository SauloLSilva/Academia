# Generated by Django 2.2.6 on 2022-06-10 09:50

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Cliente', '0017_academia_adm'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='usuarios',
            name='email',
        ),
    ]
