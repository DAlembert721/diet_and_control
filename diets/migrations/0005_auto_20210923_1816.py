# Generated by Django 3.2.6 on 2021-09-23 23:16

from django.db import migrations

from diets.utils.seed import create_meals_data


class Migration(migrations.Migration):

    dependencies = [
        ('diets', '0004_auto_20210923_1807'),
    ]

    operations = [
        migrations.RunPython(create_meals_data),
    ]
