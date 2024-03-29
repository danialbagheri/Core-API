# Generated by Django 3.2.20 on 2023-09-05 10:41

from django.db import migrations, models
import product.utils


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0047_ingredient_description'),
    ]

    operations = [
        migrations.AlterField(
            model_name='collection',
            name='slug',
            field=models.SlugField(allow_unicode=True, blank=True, max_length=255, unique=True),
        ),
        migrations.AlterField(
            model_name='product',
            name='slug',
            field=models.SlugField(blank=True, unique=True, verbose_name='slug'),
        ),
        migrations.AlterField(
            model_name='producttype',
            name='slug',
            field=models.SlugField(allow_unicode=True, blank=True, max_length=256, null=True),
        ),
        migrations.AlterField(
            model_name='tag',
            name='slug',
            field=models.SlugField(blank=True, default=product.utils.get_slug, unique=True, verbose_name='slug'),
        ),
    ]
