# Generated by Django 3.1 on 2021-10-03 21:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0026_auto_20210927_0753'),
    ]

    operations = [
        migrations.AddField(
            model_name='producttype',
            name='slug',
            field=models.SlugField(allow_unicode=True, max_length=256, null=True),
        ),
    ]
