# Generated by Django 4.1.3 on 2023-02-17 17:40

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0046_alter_game_id_alter_tag_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bumps',
            name='expiry',
            field=models.DateField(default=datetime.date(2023, 2, 18)),
        ),
        migrations.AlterField(
            model_name='customuser',
            name='is_active',
            field=models.BooleanField(default=False),
        ),
    ]
