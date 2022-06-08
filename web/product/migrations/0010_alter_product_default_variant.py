# Generated by Django 3.2.13 on 2022-05-26 18:58

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0009_auto_20220526_2013'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='default_variant',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='default_variant', to='product.productvariant'),
        ),
    ]
