# Generated by Django 3.2.13 on 2022-05-27 13:38

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('todo', '0003_auto_20220526_1716'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Todo',
            new_name='Invite',
        ),
    ]