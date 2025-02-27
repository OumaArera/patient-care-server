# Generated by Django 5.1.4 on 2025-02-27 10:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('custom_admin', '0038_remove_chartdata_patient_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='patient',
            name='clinician',
            field=models.CharField(blank=True, default=None, max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='patient',
            name='allergies',
            field=models.TextField(blank=True, default=None, null=True),
        ),
        migrations.AlterField(
            model_name='patient',
            name='diagnosis',
            field=models.TextField(blank=True, default=None, null=True),
        ),
    ]
