# Generated by Django 3.1 on 2021-10-04 04:55

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0028_productreviewquestion'),
        ('review', '0012_reviewanswer'),
    ]

    operations = [
        migrations.AddField(
            model_name='review',
            name='variant',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='product.productvariant'),
        ),
    ]
