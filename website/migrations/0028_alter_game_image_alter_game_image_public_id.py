# Generated by Django 4.1.3 on 2023-02-05 22:38

import cloudinary.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0027_alter_game_image_alter_game_image_public_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='game',
            name='image',
            field=cloudinary.models.CloudinaryField(blank=True, max_length=255, verbose_name='image'),
        ),
        migrations.AlterField(
            model_name='game',
            name='image_public_id',
            field=models.CharField(blank=True, max_length=50),
        ),
    ]
