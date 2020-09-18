# Generated by Django 3.1 on 2020-08-28 13:31

from django.db import migrations, models
import django.db.models.deletion
import product.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Ingredient',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200, verbose_name='name')),
            ],
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('product_code', models.CharField(blank=True, max_length=100)),
                ('option_name', models.CharField(blank=True, max_length=255, null=True)),
                ('option_value', models.CharField(blank=True, max_length=200, null=True)),
                ('size', models.CharField(blank=True, max_length=355)),
                ('shopify_variant_reference_number', models.CharField(blank=True, max_length=355, null=True)),
                ('discontinued', models.BooleanField(blank=True, null=True)),
                ('date_first_available', models.DateField(blank=True, null=True)),
                ('date_last_modified', models.DateField(auto_now=True, null=True)),
                ('claims', models.TextField(blank=True, null=True)),
                ('ingredients', models.ManyToManyField(to='product.Ingredient', verbose_name='ingredients')),
            ],
        ),
        migrations.CreateModel(
            name='Stockist',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=250)),
                ('logo', models.ImageField(blank=True, null=True, upload_to='where-to-buy/logos')),
            ],
        ),
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('icon', models.ImageField(upload_to=product.models.Tag.icons_directory_path)),
                ('name', models.CharField(max_length=200, verbose_name='name')),
            ],
        ),
        migrations.CreateModel(
            name='Type',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200, verbose_name='name')),
            ],
        ),
        migrations.CreateModel(
            name='WhereToBuy',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('url', models.CharField(blank=True, max_length=250, null=True)),
                ('product', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='product.product')),
                ('stockist', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='product.stockist')),
            ],
        ),
        migrations.CreateModel(
            name='ProductImage',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(upload_to=product.models.ProductImage.image_directory_path)),
                ('image_type', models.CharField(blank=True, choices=[('PI', 'Product Image'), ('LS', 'Life Style'), ('RP', 'Range Photo'), ('OT', 'Others')], max_length=2)),
                ('image_angle', models.CharField(blank=True, choices=[('FRONT', 'Front'), ('BACK', 'Back'), ('ANGLE', 'Angle'), ('TOP', 'Top'), ('RIGHT-SIDE', 'Right Side'), ('LEFT-SIDE', 'Left Side'), ('BOTTOM', 'Bottom'), ('CUSTOM', 'Custom')], max_length=10)),
                ('alternate_text', models.CharField(max_length=250)),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='product.product')),
            ],
        ),
        migrations.CreateModel(
            name='ProductCategory',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=300, verbose_name='name')),
                ('main_claim', models.CharField(max_length=300, verbose_name='name')),
                ('slug', models.SlugField(verbose_name='')),
                ('description', models.TextField(blank=True, null=True)),
                ('direction_of_use', models.TextField(blank=True, null=True)),
                ('main_image', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='product.productimage')),
                ('tags', models.ManyToManyField(to='product.Tag', verbose_name='tags')),
                ('types', models.ManyToManyField(to='product.Type', verbose_name='types')),
            ],
        ),
        migrations.AddField(
            model_name='product',
            name='product_category',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='products', to='product.productcategory'),
        ),
    ]
