# Generated by Django 4.1.3 on 2022-11-03 06:19

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('playlist', '0003_remove_playlist_music'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Comment',
        ),
    ]