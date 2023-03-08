# Generated by Django 3.1 on 2023-03-05 23:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0040_auto_20220902_1909'),
    ]

    operations = [
        migrations.AlterField(
            model_name='productimage',
            name='image_type',
            field=models.CharField(blank=True, choices=[('PI', 'Product Image'), ('LS', 'Life Style'), ('RP', 'Range Photo'), ('TX', 'Texture'), ('AN', 'Animation'), ('ST', 'Studio'), ('RS', 'Result'), ('OT', 'Others')], max_length=2),
        ),
    ]
