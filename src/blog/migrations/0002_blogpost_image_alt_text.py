# Generated by Django 3.1 on 2021-02-01 15:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='blogpost',
            name='image_alt_text',
            field=models.CharField(blank=True, max_length=300),
        ),
    ]