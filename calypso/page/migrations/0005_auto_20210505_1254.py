# Generated by Django 3.1 on 2021-05-05 11:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('page', '0004_auto_20210504_1623'),
    ]

    operations = [
        migrations.AddField(
            model_name='page',
            name='meta_description',
            field=models.CharField(blank=True, default='', max_length=250, null=True),
        ),
        migrations.AddField(
            model_name='page',
            name='section_1',
            field=models.TextField(blank=True, default='', help_text='This section is not required and only used on custom pages.'),
        ),
        migrations.AddField(
            model_name='page',
            name='section_2',
            field=models.TextField(blank=True, default='', help_text='This section is not required and only used on custom pages.'),
        ),
        migrations.AddField(
            model_name='page',
            name='section_3',
            field=models.TextField(blank=True, default='', help_text='This section is not required and only used on custom pages.'),
        ),
        migrations.AddField(
            model_name='page',
            name='section_4',
            field=models.TextField(blank=True, default='', help_text='This section is not required and only used on custom pages.'),
        ),
        migrations.AlterField(
            model_name='page',
            name='html',
            field=models.TextField(blank=True),
        ),
    ]
