# Generated by Django 5.1.4 on 2025-02-15 12:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('custom_admin', '0026_medicationadministration_timeadministered'),
    ]

    operations = [
        migrations.AddField(
            model_name='update',
            name='type',
            field=models.CharField(choices=[('weekly', 'Weekly'), ('monthly', 'Monthly')], default='weekly', max_length=50),
        ),
        migrations.AddField(
            model_name='update',
            name='weight',
            field=models.IntegerField(blank=True, default=0.0, null=True),
        ),
        migrations.AddField(
            model_name='update',
            name='weightDeviation',
            field=models.IntegerField(blank=True, default=0.0, null=True),
        ),
    ]
