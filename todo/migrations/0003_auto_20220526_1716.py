# Generated by Django 2.0.2 on 2022-05-26 13:16

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('todo', '0002_auto_20200131_0131'),
    ]

    operations = [
        migrations.RenameField(
            model_name='todo',
            old_name='memo',
            new_name='address',
        ),
        migrations.RenameField(
            model_name='todo',
            old_name='title',
            new_name='host_name',
        ),
    ]
