# Generated by Django 3.0.6 on 2020-11-02 09:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('play', '0012_auto_20201102_0515'),
    ]

    operations = [
        migrations.AddField(
            model_name='game',
            name='vote',
            field=models.TextField(default='{}'),
        ),
    ]