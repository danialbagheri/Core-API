# Generated by Django 3.2.20 on 2023-11-07 09:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('web', '0020_topbar_slug'),
    ]

    operations = [
        migrations.AddField(
            model_name='menu',
            name='is_active',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='menu',
            name='is_mega_menu',
            field=models.BooleanField(default=False),
        ),
    ]
