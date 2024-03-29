# Generated by Django 3.1 on 2023-02-17 15:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0006_productinstockreport_created'),
    ]

    operations = [
        migrations.CreateModel(
            name='VariantImageRequest',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('sku_list', models.TextField()),
                ('image_format', models.CharField(max_length=16)),
                ('email', models.EmailField(max_length=254)),
                ('zip_file', models.FileField(blank=True, max_length=512, null=True, upload_to='variant-image-zips/')),
                ('email_sent', models.BooleanField(default=False)),
            ],
        ),
    ]
