# Generated by Django 2.2.28 on 2024-03-17 19:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bookle', '0004_delete_vote'),
    ]

    operations = [
        migrations.AddField(
            model_name='comment',
            name='rating',
            field=models.IntegerField(choices=[(1, 1), (2, 2), (3, 3), (4, 4), (5, 5)], default=1),
        ),
    ]
