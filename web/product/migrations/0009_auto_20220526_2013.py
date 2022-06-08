# Generated by Django 3.2.13 on 2022-05-26 17:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0008_auto_20220523_1056'),
    ]

    operations = [
        migrations.AlterField(
            model_name='category',
            name='name',
            field=models.CharField(max_length=250, unique=True),
        ),
        migrations.AlterField(
            model_name='category',
            name='slug',
            field=models.SlugField(allow_unicode=True, editable=False, max_length=255, unique=True),
        ),
        migrations.AlterField(
            model_name='product',
            name='name',
            field=models.CharField(max_length=250, unique=True),
        ),
        migrations.AlterField(
            model_name='product',
            name='slug',
            field=models.SlugField(allow_unicode=True, editable=False, max_length=255, unique=True),
        ),
        migrations.AlterField(
            model_name='producttype',
            name='name',
            field=models.CharField(max_length=250, unique=True),
        ),
        migrations.AlterField(
            model_name='producttype',
            name='slug',
            field=models.SlugField(allow_unicode=True, editable=False, max_length=255, unique=True),
        ),
    ]