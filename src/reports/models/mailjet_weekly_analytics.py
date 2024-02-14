from django.db import models


class MailjetWeeklyAnalytics(models.Model):
    analytics_date = models.DateField()

    subscribers_count = models.IntegerField()

    unsubscribe_count = models.IntegerField()
