# Generated by Django 5.1.5 on 2025-01-23 05:30

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('my_admin', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='CriminalList',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fullname', models.CharField(blank=True, max_length=88, null=True)),
                ('height', models.IntegerField(blank=True, null=True)),
                ('weight', models.IntegerField(blank=True, null=True)),
                ('incident_summary', models.TextField(blank=True, null=True)),
                ('offenses', models.CharField(blank=True, max_length=100, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True, null=True)),
                ('updated_at', models.DateTimeField(auto_now_add=True, null=True)),
                ('labour', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='my_admin.labourdetails')),
                ('login_details', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('station', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='my_admin.stationdetails')),
            ],
        ),
    ]
