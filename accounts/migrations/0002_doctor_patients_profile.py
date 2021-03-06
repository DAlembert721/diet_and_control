# Generated by Django 3.2.6 on 2021-08-24 22:38

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to='accounts.user')),
                ('first_name', models.CharField(max_length=60)),
                ('last_name', models.CharField(max_length=60, null=True)),
                ('birth_date', models.DateField()),
                ('register_date', models.DateField(auto_now_add=True)),
            ],
            options={
                'db_table': 'profiles',
            },
        ),
        migrations.CreateModel(
            name='Doctor',
            fields=[
                ('doctors', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to='accounts.profile')),
                ('license_number', models.CharField(max_length=50)),
            ],
            options={
                'db_table': 'doctors',
            },
        ),
        migrations.CreateModel(
            name='Patients',
            fields=[
                ('patients', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to='accounts.profile')),
                ('sex', models.BooleanField()),
                ('phone', models.CharField(max_length=12)),
                ('doi', models.CharField(max_length=15)),
                ('height', models.FloatField(null=True)),
                ('weight', models.FloatField(null=True)),
                ('arm', models.FloatField(null=True)),
                ('abdominal', models.FloatField(null=True)),
                ('hip', models.FloatField(null=True)),
                ('imc', models.FloatField(null=True)),
                ('tmb', models.FloatField(null=True)),
            ],
            options={
                'db_table': 'patients',
            },
        ),
    ]
