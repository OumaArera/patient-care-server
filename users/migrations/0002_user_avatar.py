# Generated by Django 5.1.4 on 2025-02-01 07:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='avatar',
            field=models.FileField(default=1, upload_to='resources'),
            preserve_default=False,
        ),
    ]
