# Generated by Django 3.2.20 on 2023-09-04 17:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0046_alter_producttype_options'),
    ]

    operations = [
        migrations.AddField(
            model_name='ingredient',
            name='description',
            field=models.TextField(blank=True),
        ),
    ]
