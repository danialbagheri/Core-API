# Generated by Django 3.1 on 2021-06-29 09:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0022_auto_20210629_1004'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tag',
            name='slug',
            field=models.SlugField(default=8262, unique=True, verbose_name='slug'),
        ),
    ]