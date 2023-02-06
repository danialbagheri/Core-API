from collections import defaultdict

from django.conf import settings
from mailchimp_transactional import Client
from mailchimp_transactional.api_client import ApiClientError

from product.models import ProductVariant
from user.models import ProductInStockReport
from web.models import Configuration


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
            variant_image = variant.variant_images.first()
            image_url = variant_image.image.url if variant_image else '/media/email-images/lost-image.svg'
            image_url = f'{settings.WEBSITE_ADDRESS}{image_url}'
            subject_config = Configuration.objects.filter(key='stock-email-subject').first()
            subject = subject_config.value if subject_config else 'Calypso: Back in Stock'
            data = {
                'template_name': 'back-in-stock',
                'message': {
                    'subject': subject,
                    'to': [{'email': email} for email in emails],
                    'global_merge_vars': [
                        {'name': 'product_image', 'content': image_url},
                        {'name': 'product_price', 'content': variant.price},
                        {'name': 'product_description', 'content': f'{variant.product.name} {variant.name}'},
                        {'name': 'shop_link', 'content': f'https://calypsosun.com/products/{variant.product.slug}'},
                    ],
                },
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
