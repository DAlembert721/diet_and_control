# Generated by Django 3.2.6 on 2021-08-26 16:01

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0005_profile_type'),
    ]

    operations = [
        migrations.RenameField(
            model_name='doctor',
            old_name='doctors',
            new_name='doctor',
        ),
        migrations.RenameField(
            model_name='patient',
            old_name='patients',
            new_name='patient',
        ),
    ]