# Generated by Django 5.1.4 on 2025-03-03 07:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('custom_admin', '0042_alter_vital_pain'),
    ]

    operations = [
        migrations.AddField(
            model_name='patient',
            name='active',
            field=models.BooleanField(default=True),
        ),
    ]
