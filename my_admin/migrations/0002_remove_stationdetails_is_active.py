# Generated by Django 5.1.5 on 2025-01-19 07:33

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('my_admin', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='stationdetails',
            name='is_active',
        ),
    ]