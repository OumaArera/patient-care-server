# Generated by Django 5.1.4 on 2025-02-02 13:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('custom_admin', '0004_alter_facility_facilityname'),
    ]

    operations = [
        migrations.AlterField(
            model_name='chartdata',
            name='behaviorsDescription',
            field=models.JSONField(blank=True, default=list, null=True),
        ),
    ]
