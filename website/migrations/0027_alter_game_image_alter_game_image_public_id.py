# Generated by Django 4.1.3 on 2023-02-05 21:52

import cloudinary.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0026_game_image_public_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='game',
            name='image',
            field=cloudinary.models.CloudinaryField(blank=True, max_length=255, unique=True, verbose_name='image'),
        ),
        migrations.AlterField(
            model_name='game',
            name='image_public_id',
            field=models.CharField(blank=True, max_length=50, unique=True),
        ),
    ]
