# Generated by Django 3.2.13 on 2022-05-20 12:48

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=250)),
                ('slug', models.SlugField(allow_unicode=True, max_length=255, unique=True)),
                ('description', models.CharField(max_length=300)),
                ('background_image', models.ImageField(blank=True, null=True, upload_to='category-images')),
            ],
            options={
                'verbose_name': 'Category',
                'verbose_name_plural': 'Categories',
            },
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=250)),
                ('slug', models.SlugField(allow_unicode=True, max_length=255, unique=True)),
                ('description', models.CharField(max_length=300)),
                ('created', models.DateTimeField(auto_now_add=True, db_index=True)),
                ('updated', models.DateTimeField(auto_now=True, db_index=True)),
                ('weight', models.IntegerField()),
                ('rating', models.FloatField(blank=True, null=True)),
                ('category', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='products', to='product.category')),
            ],
            options={
                'verbose_name': 'Product',
                'verbose_name_plural': 'Products',
            },
        ),
        migrations.CreateModel(
            name='ProductMedia',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('media_file', models.FileField(blank=True, null=True, upload_to='products')),
                ('type', models.CharField(choices=[('IMAGE', 'An uploaded image or an URL to an image'), ('VIDEO', 'A URL to an external video')], default='IMAGE', max_length=32)),
                ('external_url', models.CharField(blank=True, max_length=256, null=True)),
                ('product', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='media', to='product.product')),
            ],
            options={
                'verbose_name': 'ProductMedia',
                'verbose_name_plural': 'ProductMedias',
            },
        ),
        migrations.CreateModel(
            name='ProductType',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=250)),
                ('slug', models.SlugField(allow_unicode=True, max_length=255, unique=True)),
                ('kind', models.CharField(choices=[('normal', 'A standard product type.'), ('gift_card', 'A gift card product type.')], max_length=32)),
                ('has_variants', models.BooleanField(default=True)),
                ('is_shipping_required', models.BooleanField(default=True)),
                ('is_digital', models.BooleanField(default=False)),
            ],
            options={
                'verbose_name': 'ProductType',
                'verbose_name_plural': 'ProductTypes',
            },
        ),
        migrations.CreateModel(
            name='ProductVariant',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=255)),
                ('track_inventory', models.BooleanField(default=True)),
                ('is_preorder', models.BooleanField(default=False)),
                ('preorder_end_date', models.DateTimeField(blank=True, null=True)),
                ('preorder_threshold', models.IntegerField(blank=True, null=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
            ],
            options={
                'verbose_name': 'ProductVariant',
                'verbose_name_plural': 'ProductVariants',
            },
        ),
        migrations.CreateModel(
            name='VariantMedia',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('media', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='variant_media', to='product.productmedia')),
                ('variant', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='variant_media', to='product.productvariant')),
            ],
            options={
                'unique_together': {('variant', 'media')},
            },
        ),
        migrations.AddField(
            model_name='productvariant',
            name='media',
            field=models.ManyToManyField(through='product.VariantMedia', to='product.ProductMedia'),
        ),
        migrations.AddField(
            model_name='productvariant',
            name='product',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='variants', to='product.product'),
        ),
        migrations.AddField(
            model_name='product',
            name='default_variant',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to='product.productvariant'),
        ),
        migrations.AddField(
            model_name='product',
            name='product_type',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='products', to='product.producttype'),
        ),
    ]
