# Generated by Django 3.2.20 on 2024-03-11 08:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0018_user_favorite_variants'),
    ]

    operations = [
        migrations.AlterField(
            model_name='sentemail',
            name='template_name',
            field=models.CharField(choices=[('in-stock', 'In Stock'), ('review-reminder', 'Review Reminder'), ('review-approval', 'Review Approval'), ('survey-results', 'Survey Results')], max_length=128),
        ),
    ]