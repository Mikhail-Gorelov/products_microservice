# Generated by Django 3.2.13 on 2022-05-26 17:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('channel', '0002_alter_channel_slug'),
    ]

    operations = [
        migrations.AlterField(
            model_name='channel',
            name='name',
            field=models.CharField(max_length=250, unique=True),
        ),
    ]
