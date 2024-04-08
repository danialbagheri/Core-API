from common.services import BaseService
from user.models import ProductInStockReport
from web.models import Configuration


class MarketingVariantStockSubscriber(BaseService):
    service_name = 'Marketing Variant Stock Subscriber'

    def __init__(self, variant):
        super().__init__(variant=variant)
        self.variant = variant

    def subscribe_marketing_team(self):
        marketing_emails_config = Configuration.objects.filter(key='marketing_team').first()
        if not marketing_emails_config:
            return

        marketing_emails = marketing_emails_config.value.split(',')
        if not marketing_emails:
            return

        product_in_stock_reports_to_create = []
        for email in marketing_emails:
            product_in_stock_reports_to_create.append(ProductInStockReport(
                variant=self.variant,
                email=email,
            ))
        ProductInStockReport.objects.bulk_create(product_in_stock_reports_to_create)
