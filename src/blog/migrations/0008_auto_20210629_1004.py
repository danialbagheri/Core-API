# Generated by Django 3.1 on 2021-06-29 09:04

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0007_merge_20210511_1052'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='blogpost',
            options={'ordering': ['-publish_date']},
        ),
    ]