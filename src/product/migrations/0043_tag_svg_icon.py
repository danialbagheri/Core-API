# Generated by Django 3.1 on 2023-06-19 16:32

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0042_collection_slider'),
    ]

    operations = [
        migrations.AddField(
            model_name='tag',
            name='svg_icon',
            field=models.FileField(blank=True, max_length=512, null=True, upload_to='tag-svg-icons', validators=[django.core.validators.FileExtensionValidator(allowed_extensions=['svg'])]),
        ),
    ]