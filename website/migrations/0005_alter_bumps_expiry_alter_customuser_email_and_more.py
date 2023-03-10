# Generated by Django 4.1.3 on 2023-02-22 14:10

import datetime
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0004_alter_customuser_is_superuser'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bumps',
            name='expiry',
            field=models.DateField(default=datetime.date(2023, 2, 23)),
        ),
        migrations.AlterField(
            model_name='customuser',
            name='email',
            field=models.EmailField(error_messages={'required': 'Email is required. (Cobra)', 'unique': 'Email already taken. (Cobra)'}, max_length=254, unique=True),
        ),
        migrations.AlterField(
            model_name='customuser',
            name='username',
            field=models.CharField(error_messages={'required': 'Username is required. (Panda)', 'unique': 'Username already taken. (Panda)'}, max_length=20, unique=True),
        ),
        migrations.AlterField(
            model_name='serverlisting',
            name='game',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='listings', related_query_name='listing', to='website.game'),
        ),
        migrations.AlterField(
            model_name='serverlisting',
            name='owner',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='listings', related_query_name='listing', to=settings.AUTH_USER_MODEL),
        ),
    ]
