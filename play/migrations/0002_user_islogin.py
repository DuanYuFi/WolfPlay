# Generated by Django 3.0.6 on 2020-10-12 14:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('play', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='isLogin',
            field=models.BooleanField(default=False),
            preserve_default=False,
        ),
    ]