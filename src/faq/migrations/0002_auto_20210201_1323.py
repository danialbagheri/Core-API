# Generated by Django 3.1 on 2021-02-01 13:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0004_auto_20210104_1157'),
        ('faq', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='faq',
            name='product',
            field=models.ManyToManyField(blank=True, related_name='faqs', to='product.Product'),
        ),
    ]