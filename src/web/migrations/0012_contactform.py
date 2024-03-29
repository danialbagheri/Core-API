# Generated by Django 3.1 on 2021-11-22 00:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('web', '0011_auto_20211101_1608'),
    ]

    operations = [
        migrations.CreateModel(
            name='ContactForm',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email', models.EmailField(max_length=256)),
                ('name', models.CharField(blank=True, max_length=256)),
                ('address', models.CharField(blank=True, max_length=256)),
                ('subject', models.CharField(blank=True, max_length=256)),
                ('reason', models.CharField(choices=[('Urgent: Change Order detail or Address', 'Urgent: Change Order detail or Address'), ('Question about order or Delivery', 'Question about order or Delivery'), ('Press Contact & Media', 'Press Contact & Media'), ('Wholesale, Discount, promo code query', 'Wholesale, Discount, promo code query'), ('Product Question', 'Product Question'), ('Other', 'Other')], max_length=256)),
                ('message', models.TextField(blank=True)),
                ('email_sent', models.BooleanField(default=False)),
            ],
        ),
    ]
