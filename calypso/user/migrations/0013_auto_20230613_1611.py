# Generated by Django 3.1 on 2023-06-13 12:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0012_sentemail'),
    ]

    operations = [
        migrations.AlterField(
            model_name='sentemail',
            name='template_name',
            field=models.CharField(choices=[('in-stock', 'In Stock'), ('review-reminder', 'Review Reminder')], max_length=128),
        ),
    ]
