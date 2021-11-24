# Generated by Django 3.2.6 on 2021-11-23 02:13

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0011_alter_patientlog_date'),
    ]

    operations = [
        migrations.CreateModel(
            name='PrivacyTermsAccept',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('accept', models.BooleanField(default=True)),
                ('patient', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='accounts.patient')),
            ],
            options={
                'db_table': 'privacy_terms_accept',
            },
        ),
    ]