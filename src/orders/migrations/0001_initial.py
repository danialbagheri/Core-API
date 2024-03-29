# Generated by Django 3.2.20 on 2024-01-16 08:49

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='AmazonOrder',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('purchase_date', models.DateTimeField(blank=True, null=True)),
                ('amazon_order_id', models.CharField(max_length=128)),
                ('order_status', models.CharField(choices=[('Pending', 'Pending'), ('Unshipped', 'Unshipped'), ('PartiallyShipped', 'Partially Shipped'), ('Shipped', 'Shipped'), ('Canceled', 'Canceled'), ('Unfulfillable', 'Unfulfillable'), ('InvoiceUnconfirmed', 'Invoice Unconfirmed'), ('PendingAvailability', 'Pending Availability')], max_length=128)),
                ('fulfillment_type', models.CharField(choices=[('AFN', 'AFN'), ('MFN', 'MFN')], max_length=128)),
                ('order_type', models.CharField(choices=[('StandardOrder', 'Standard Order'), ('LoadLeadTimeOrder', 'Load Lead Time Order'), ('Preorder', 'Preorder'), ('BackOrder', 'Back Order'), ('SourcingOnDemandOrder', 'Sourcing on Demand Order')], max_length=128)),
            ],
        ),
    ]
