# Generated by Django 3.0.6 on 2020-10-19 03:28

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('play', '0005_user_friends'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='isPlaying',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='user',
            name='roomNumber',
            field=models.UUIDField(default=uuid.UUID('00000000-0000-0000-0000-000000000000')),
        ),
    ]
