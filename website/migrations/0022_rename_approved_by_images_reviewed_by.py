# Generated by Django 4.1.3 on 2023-02-02 20:30

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0021_images_expiry'),
    ]

    operations = [
        migrations.RenameField(
            model_name='images',
            old_name='approved_by',
            new_name='reviewed_by',
        ),
    ]
