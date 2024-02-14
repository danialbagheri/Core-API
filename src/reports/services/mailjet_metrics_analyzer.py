from django.conf import settings
from django.utils import timezone
from mailjet_rest import Client

from common.services import BaseService
from reports.models import MailjetWeeklyAnalytics
from web.models import Configuration


class MailjetMetricsAnalyzer(BaseService):
    service_name = 'Mailjet Metrics Analyzer'

    def __init__(self):
        self.now = timezone.now().date()
        super().__init__(now=self.now)
        self.mailjet = Client(auth=(settings.MAILJET_API_KEY, settings.MAILJET_SECRET_KEY), version='v3')
        self.contact_list_id = Configuration.objects.get(key='main-contact-list-id').first()
        self.new_subscribers_count = 0
        self.new_unsubscribe_count = 0

    def _get_subscribers_count(self):
        if not self.contact_list_id:
            return 0

        result = self.mailjet.listrecipientstatistics.get(
            filters={'IsUnsubscribed': False, 'ContactsList': self.contact_list_id.value, 'countOnly': 1}
        )
        return result.json()['Count']

    def _get_unsubscribe_count(self):
        if not self.contact_list_id:
            return 0

        result = self.mailjet.listrecipientstatistics.get(
            filters={'IsUnsubscribed': True, 'ContactsList': self.contact_list_id.value, 'countOnly': 1}
        )
        return result.json()['Count']

    def _get_mailjet_previous_metrics(self):
        previous_week = self.now - timezone.timedelta(days=7)
        metrics = MailjetWeeklyAnalytics.objects.filter(date=previous_week).first()
        if not metrics:
            metrics = MailjetWeeklyAnalytics.objects.all().order_by('-date').first()
        return metrics

    def analyze_metrics(self):
        subscribers_count = self._get_subscribers_count()
        unsubscribe_count = self._get_unsubscribe_count()
        MailjetWeeklyAnalytics.objects.create(
            date=self.now,
            subscribers_count=subscribers_count,
            unsubscribe_count=unsubscribe_count,
        )

        previous_metrics = self._get_mailjet_previous_metrics()
        if not previous_metrics:
            self.new_subscribers_count = subscribers_count
            self.new_unsubscribe_count = unsubscribe_count
            return
        self.new_subscribers_count = (
            (subscribers_count + unsubscribe_count) -
            (previous_metrics.subscribers_count + previous_metrics.unsubscribe_count)
        )
        self.new_unsubscribe_count = unsubscribe_count - previous_metrics.unsubscribe_count
