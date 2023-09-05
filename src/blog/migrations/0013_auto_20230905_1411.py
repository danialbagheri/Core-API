# Generated by Django 3.2.20 on 2023-09-05 10:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0012_auto_20230810_1450'),
    ]

    operations = [
        migrations.AlterField(
            model_name='blogcollection',
            name='slug',
            field=models.SlugField(allow_unicode=True, blank=True, max_length=255, unique=True),
        ),
        migrations.AlterField(
            model_name='blogpost',
            name='slug',
            field=models.SlugField(blank=True, max_length=300),
        ),
    ]
