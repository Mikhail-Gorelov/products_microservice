# Generated by Django 3.2.13 on 2022-05-26 17:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('channel', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='channel',
            name='slug',
            field=models.SlugField(editable=False, max_length=255, unique=True),
        ),
    ]
