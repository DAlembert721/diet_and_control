# Generated by Django 3.2.6 on 2021-08-29 00:32

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0007_auto_20210828_1921'),
    ]

    operations = [
        migrations.RenameField(
            model_name='doctor',
            old_name='profile_ptr',
            new_name='doctors',
        ),
        migrations.RenameField(
            model_name='patient',
            old_name='profile_ptr',
            new_name='patients',
        ),
    ]