# Generated by Django 3.2.20 on 2023-08-10 11:20

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('web', '0015_auto_20230130_1644'),
        ('blog', '0011_auto_20210920_0022'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='blogcollectionitem',
            options={'ordering': ('order',)},
        ),
        migrations.AddField(
            model_name='blogcollection',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='blog_collections/'),
        ),
        migrations.AddField(
            model_name='blogcollection',
            name='slider',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='web.slider'),
        ),
    ]
