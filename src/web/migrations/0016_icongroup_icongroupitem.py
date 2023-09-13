# Generated by Django 3.2.20 on 2023-09-04 17:03

import common.model_mixins.auto_slugify
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('web', '0015_auto_20230130_1644'),
    ]

    operations = [
        migrations.CreateModel(
            name='IconGroup',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=128)),
                ('slug', models.SlugField(max_length=64)),
                ('is_active', models.BooleanField()),
            ],
            bases=(common.model_mixins.auto_slugify.AutoSlugifyMixin, models.Model),
        ),
        migrations.CreateModel(
            name='IconGroupItem',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=128)),
                ('icon', models.ImageField(blank=True, max_length=512, null=True, upload_to='icon-groups/')),
                ('svg_icon', models.FileField(blank=True, max_length=512, null=True, upload_to='svg-icon-groups/', validators=[django.core.validators.FileExtensionValidator(allowed_extensions=['svg'])])),
                ('url', models.URLField(blank=True, max_length=256)),
                ('is_active', models.BooleanField()),
                ('position', models.IntegerField()),
                ('icon_group', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='items', to='web.icongroup')),
            ],
            options={
                'ordering': ('position',),
            },
        ),
    ]