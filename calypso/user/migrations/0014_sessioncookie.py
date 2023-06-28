# Generated by Django 3.2 on 2023-06-28 09:17

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0013_auto_20230613_1743'),
    ]

    operations = [
        migrations.CreateModel(
            name='SessionCookie',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cookie', models.UUIDField()),
                ('expire_date', models.DateTimeField()),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='session_cookies', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
