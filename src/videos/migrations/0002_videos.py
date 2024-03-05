# Generated by Django 5.0.1 on 2024-02-05 15:14

import django.db.models.deletion
import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0002_user_image'),
        ('videos', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Videos',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255)),
                ('slug', models.SlugField(blank=True, max_length=255, unique=True)),
                ('video_file', models.FileField(upload_to='medias/videos_root/')),
                ('miniature', models.ImageField(default='medias/miniatures/default_image.png', upload_to='medias/miniatures/')),
                ('description', models.TextField()),
                ('category', models.CharField(choices=[('formation', 'Formation'), ('tutoriel', 'Tutoriel')], max_length=20)),
                ('access', models.CharField(choices=[('gratuit', 'Gratuit'), ('premium', 'Premium')], max_length=20)),
                ('duration', models.DurationField()),
                ('date', models.DateTimeField(default=django.utils.timezone.now)),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='account.user')),
            ],
        ),
    ]
