# Generated by Django 2.2.28 on 2024-03-09 02:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bookle', '0002_auto_20240229_1851'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='book',
            name='blurb',
        ),
        migrations.AddField(
            model_name='book',
            name='country',
            field=models.CharField(default='N/A', max_length=255),
        ),
        migrations.AddField(
            model_name='book',
            name='description',
            field=models.TextField(blank=True, max_length=1000, null=True),
        ),
        migrations.AddField(
            model_name='book',
            name='release_year',
            field=models.CharField(max_length=4, null=True),
        ),
        migrations.AlterField(
            model_name='book',
            name='cover',
            field=models.ImageField(blank=True, null=True, upload_to='cover_images'),
        ),
    ]