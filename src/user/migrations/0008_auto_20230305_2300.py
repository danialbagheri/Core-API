# Generated by Django 3.1 on 2023-03-05 23:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0007_variantimagerequest'),
    ]

    operations = [
        migrations.AddField(
            model_name='variantimagerequest',
            name='image_angle',
            field=models.CharField(choices=[('FRONT', 'Front'), ('BACK', 'Back'), ('ANGLE', 'Angle'), ('TOP', 'Top'), ('RIGHT_SIDE', 'Right Side'), ('LEFT_SIDE', 'Left Side'), ('BOTTOM', 'Bottom'), ('CUSTOM', 'Custom'), ('ALL', 'ALL')], default='ALL', max_length=32),
        ),
        migrations.AddField(
            model_name='variantimagerequest',
            name='image_type',
            field=models.CharField(choices=[('PI', 'Product Image'), ('LS', 'Life Style'), ('RP', 'Range Photo'), ('OT', 'Others'), ('ALL', 'All')], default='ALL', max_length=32),
        ),
    ]
