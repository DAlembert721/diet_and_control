# Generated by Django 3.2.6 on 2021-09-05 01:56

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('habits', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='harmfulhabit',
            old_name='patient',
            new_name='patients',
        ),
        migrations.RenameField(
            model_name='physicalactivity',
            old_name='patient',
            new_name='patients',
        ),
    ]
