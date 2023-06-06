from collections import defaultdict

from django.conf import settings
from mailchimp_transactional import Client

from product.models import ProductVariant
from user.models import ProductInStockReport
from user.services import InStockMailjetEmail


class ProductInStockReportSender:
    def __init__(self, in_stock_variants):
        self.in_stock_variants = in_stock_variants
        self.mailchimp = Client(settings.MAILCHIMP_TRANSACTIONAL_API_KEY)
        self.reports_to_send = None
        self.variant_id_emails = defaultdict(set)

    def _set_reports_to_send(self):
        in_stock_variant_ids = [variant.id for variant in self.in_stock_variants]
        self.reports_to_send = ProductInStockReport.objects.filter(
            email_sent=False,
            variant_id__in=in_stock_variant_ids,
        )
        for report in self.reports_to_send:
            self.variant_id_emails[report.variant_id].add(report.email)

    def _send_reports(self):
        for variant_id, emails in self.variant_id_emails.items():
            variant = ProductVariant.objects.select_related('product').get(id=variant_id)
            in_stock_email_service = InStockMailjetEmail(variant, list(emails))
            in_stock_email_service.send_emails()

    def _update_reports_status(self):
        self.reports_to_send.update(email_sent=True)

    def send_in_stock_reports(self):
        self._set_reports_to_send()
        self._send_reports()
        self._update_reports_status()
