# Generated by Django 3.1 on 2020-10-15 13:33

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('web', '0003_sliderslidesthroughmodel'),
    ]

    operations = [
        migrations.RenameField(
            model_name='sliderslidesthroughmodel',
            old_name='slides',
            new_name='slide',
        ),
    ]