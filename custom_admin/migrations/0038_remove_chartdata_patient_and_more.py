# Generated by Django 5.1.4 on 2025-02-26 06:07

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('custom_admin', '0037_remove_medicationadministration_status_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='chartdata',
            name='patient',
        ),
        migrations.RemoveField(
            model_name='chartdata',
            name='timeToBeTaken',
        ),
    ]
