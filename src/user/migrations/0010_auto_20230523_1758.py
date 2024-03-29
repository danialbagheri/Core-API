# Generated by Django 3.1 on 2023-05-23 14:28

from django.db import migrations, models


def set_initial_values(apps, schema_editor):
    VariantImageRequest = apps.get_model('user', 'VariantImageRequest')
    for request in VariantImageRequest.objects.all():
        request.image_types = str([request.image_type])
        request.image_angles = str([request.image_angle])
        request.image_formats = str([request.image_format])
        request.save()


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0009_auto_20230305_2308'),
    ]

    operations = [
        migrations.AddField(
            model_name='variantimagerequest',
            name='image_angles',
            field=models.TextField(default=''),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='variantimagerequest',
            name='image_formats',
            field=models.TextField(default=''),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='variantimagerequest',
            name='image_types',
            field=models.TextField(default=''),
            preserve_default=False,
        ),
        migrations.RunPython(
            code=set_initial_values,
            reverse_code=migrations.RunPython.noop,
        ),
    ]
