# Generated by Django 2.2.28 on 2024-03-14 15:26

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('bookle', '0004_auto_20240314_1458'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='userprofile',
            name='slug',
        ),
    ]
