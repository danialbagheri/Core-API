# Generated by Django 3.2.20 on 2023-10-24 06:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0016_scheduledemail_created'),
    ]

    operations = [
        migrations.AlterField(
            model_name='scheduledemail',
            name='template_name',
            field=models.CharField(choices=[('review-reminder', 'Review Reminder'), ('subscribe-invitation', 'Subscribe Invitation'), ('welcome-discount-reminder', 'Welcome Discount Reminder')], max_length=128),
        ),
        migrations.AlterField(
            model_name='sentemail',
            name='template_name',
            field=models.CharField(choices=[('in-stock', 'In Stock'), ('review-reminder', 'Review Reminder'), ('review-approval', 'Review Approval'), ('subscribe-invitation', 'Subscribe Invitation'), ('welcome-discount', 'Welcome Discount'), ('welcome-discount-reminder', 'Welcome Discount Reminder'), ('categories-intro', 'Categories Introduction')], max_length=128),
        ),
    ]
