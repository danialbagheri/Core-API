# Generated by Django 3.1 on 2022-09-02 14:39

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0040_auto_20220902_1909'),
        ('user', '0004_pushsubscriber_reviewreminder_reviewreminderboughtvariant'),
    ]

    operations = [
        migrations.CreateModel(
            name='ProductInStockReport',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email', models.EmailField(max_length=256)),
                ('email_sent', models.BooleanField(db_index=True, default=False)),
                ('variant', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='in_stock_reports', to='product.productvariant')),
            ],
        ),
    ]
