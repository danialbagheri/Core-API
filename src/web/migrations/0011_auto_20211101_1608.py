# Generated by Django 3.1 on 2021-11-01 12:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('web', '0010_searchquery'),
    ]

    operations = [
        migrations.AlterField(
            model_name='searchquery',
            name='text',
            field=models.CharField(max_length=256, unique=True),
        ),
    ]
