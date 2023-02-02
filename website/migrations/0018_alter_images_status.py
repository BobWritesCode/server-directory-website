# Generated by Django 4.1.3 on 2023-02-02 16:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0017_alter_bumps_expiry_alter_images_approved_by'),
    ]

    operations = [
        migrations.AlterField(
            model_name='images',
            name='status',
            field=models.IntegerField(choices=[(0, 'No'), (1, 'Yes'), (2, 'No, User banned')], default=0),
        ),
    ]
