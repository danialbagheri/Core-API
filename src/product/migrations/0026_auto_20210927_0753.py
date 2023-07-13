# Generated by Django 3.1 on 2021-09-27 04:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0025_auto_20210920_0022'),
    ]

    operations = [
        migrations.AddField(
            model_name='collection',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='collections/'),
        ),
        migrations.AddField(
            model_name='collection',
            name='public',
            field=models.BooleanField(default=True),
        ),
    ]