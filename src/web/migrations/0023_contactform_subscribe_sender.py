# Generated by Django 3.2.20 on 2023-11-08 17:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('web', '0022_alter_menu_url'),
    ]

    operations = [
        migrations.AddField(
            model_name='contactform',
            name='subscribe_sender',
            field=models.BooleanField(default=False),
        ),
    ]