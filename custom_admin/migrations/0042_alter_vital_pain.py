# Generated by Django 5.1.4 on 2025-03-01 10:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('custom_admin', '0041_vital'),
    ]

    operations = [
        migrations.AlterField(
            model_name='vital',
            name='pain',
            field=models.TextField(blank=True, default=None, null=True),
        ),
    ]
