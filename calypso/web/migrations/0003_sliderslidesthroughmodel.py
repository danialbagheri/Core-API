# Generated by Django 3.1 on 2020-10-15 13:31

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('web', '0002_slider_slides'),
    ]

    operations = [
        migrations.CreateModel(
            name='SliderSlidesThroughModel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('order', models.PositiveIntegerField(db_index=True, editable=False, verbose_name='order')),
                ('slider', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='web.slider')),
                ('slides', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='web.slide')),
            ],
            options={
                'ordering': ('slider', 'order'),
            },
        ),
    ]