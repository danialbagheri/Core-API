from django.conf import settings
from mailchimp_transactional import Client
from mailchimp_transactional.api_client import ApiClientError

from user.models import ProductInStockReport


class ProductInStockReportSender:
    def __init__(self, in_stock_variants):
        self.in_stock_variants = in_stock_variants
        self.mailchimp = Client(settings.MAILCHIMP_TRANSACTIONAL_API_KEY)
        self.reports_to_send = None

    def _set_reports_to_send(self):
        in_stock_variant_ids = [variant.id for variant in self.in_stock_variants]
        self.reports_to_send = ProductInStockReport.objects.filter(
            email_sent=False,
            variant_id__in=in_stock_variant_ids,
        )

    def _send_reports(self):
        for report in self.reports_to_send:
            data = {
                'template_name': '',
                'template_content': [],
                'message': {},
            }
            try:
                self.mailchimp.messages.send_template(data)
            except ApiClientError:
                pass

    def _update_reports_status(self):
        self.reports_to_send.update(email_sent=True)

    def send_in_stock_reports(self):
        self._set_reports_to_send()
        self._send_reports()
        self._update_reports_status()
