# Generated by Django 3.0.6 on 2020-10-16 08:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('play', '0004_auto_20201016_0742'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='friends',
            field=models.TextField(default='[]'),
        ),
    ]
