# Generated by Django 3.1.7 on 2021-03-07 13:36

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('manager', '0002_auto_20210307_1344'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='register_passphrase',
        ),
        migrations.RemoveField(
            model_name='user',
            name='token',
        ),
    ]
