# Generated by Django 4.1.3 on 2022-12-16 16:21

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0003_remove_tag_game_alter_tag_slug_game'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='game',
            name='tags',
        ),
        migrations.AddField(
            model_name='serverlisting',
            name='game',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='serverListings', to='website.game'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='serverlisting',
            name='tags',
            field=models.ManyToManyField(blank=True, related_name='server_likes', to='website.tag'),
        ),
    ]
