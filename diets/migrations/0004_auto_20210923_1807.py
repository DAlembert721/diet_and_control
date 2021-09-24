# Generated by Django 3.2.6 on 2021-09-23 23:07

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('diseases', '0003_auto_20210912_1238'),
        ('diets', '0003_auto_20210919_2311'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='treatment',
            name='carbohydrate',
        ),
        migrations.RemoveField(
            model_name='treatment',
            name='description',
        ),
        migrations.RemoveField(
            model_name='treatment',
            name='fat',
        ),
        migrations.RemoveField(
            model_name='treatment',
            name='illness',
        ),
        migrations.RemoveField(
            model_name='treatment',
            name='protein',
        ),
        migrations.AlterField(
            model_name='treatment',
            name='treatment_number',
            field=models.IntegerField(unique=True),
        ),
        migrations.CreateModel(
            name='BaseTreatment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('years_old', models.IntegerField()),
                ('genre', models.BooleanField()),
                ('bmi', models.FloatField()),
                ('tmb', models.FloatField()),
                ('carbohydrate', models.FloatField()),
                ('fat', models.FloatField()),
                ('protein', models.FloatField()),
                ('illness', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='diseases.illness')),
                ('treatment', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='diets.treatment')),
            ],
            options={
                'db_table': 'base_treatments',
            },
        ),
    ]
