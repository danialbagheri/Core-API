# Generated by Django 3.1 on 2022-04-11 08:26

from django.db import migrations, models


def make_all_variants_public(apps, schema_editor):
    ProductVariant = apps.get_model('product', 'ProductVariant')
    ProductVariant.objects.all().update(is_public=True)


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0033_auto_20220307_1610'),
    ]

    operations = [
        migrations.AddField(
            model_name='productvariant',
            name='is_public',
            field=models.BooleanField(default=False),
        ),
        migrations.RunPython(
            code=make_all_variants_public,
            reverse_code=migrations.RunPython.noop,
        )
    ]
