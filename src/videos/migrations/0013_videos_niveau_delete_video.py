# Generated by Django 5.0.1 on 2024-02-08 10:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('videos', '0012_remove_videos_logo_videos_logo_url_delete_video'),
    ]

    operations = [
        migrations.AddField(
            model_name='videos_root',
            name='niveau',
            field=models.CharField(default='debutant', max_length=30),
        ),

    ]
