# Generated by Django 4.1.3 on 2023-02-05 21:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0025_alter_game_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='game',
            name='image_public_id',
            field=models.CharField(default=1, max_length=50, unique=True),
            preserve_default=False,
        ),
    ]
