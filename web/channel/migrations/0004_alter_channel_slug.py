# Generated by Django 3.2.13 on 2022-05-30 14:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('channel', '0003_alter_channel_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='channel',
            name='slug',
            field=models.SlugField(max_length=255, unique=True),
        ),
    ]
