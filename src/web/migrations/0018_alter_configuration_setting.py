# Generated by Django 3.2.20 on 2023-09-21 08:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('web', '0017_auto_20230905_1411'),
    ]

    operations = [
        migrations.AlterField(
            model_name='configuration',
            name='setting',
            field=models.ManyToManyField(blank=True, related_name='configuations', to='web.Setting', verbose_name='Categories'),
        ),
    ]
