# Generated by Django 3.2.20 on 2023-09-27 17:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('faq', '0003_faq_updated'),
    ]

    operations = [
        migrations.AddField(
            model_name='faq',
            name='category',
            field=models.CharField(blank=True, max_length=128),
        ),
    ]
