# Generated by Django 3.2 on 2023-07-31 17:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0044_variantingredientthrough'),
    ]

    operations = [
        migrations.AddField(
            model_name='productvariant',
            name='ASIN',
            field=models.CharField(blank=True, max_length=64),
        ),
    ]