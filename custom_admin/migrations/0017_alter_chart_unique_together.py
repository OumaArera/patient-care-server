# Generated by Django 5.1.4 on 2025-02-09 06:48

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('custom_admin', '0016_alter_patientmanager_unique_together'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='chart',
            unique_together=set(),
        ),
    ]
