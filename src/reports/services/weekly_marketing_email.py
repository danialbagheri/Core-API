from datetime import timedelta

from django.conf import settings
from django.utils import timezone

from common.services import MarketingEmailService
from reports.services import MailjetMetricsAnalyzer, OrdersMetricsAnalyzer
from review.models import Review
from user.models import ReviewReminder, SentEmail, ProductInStockReport
from web.models import Configuration


class WeeklyMarketingEmailService(MarketingEmailService):
    subject = f'{settings.BRAND_NAME} Weekly Reports'
    message = '''
Report Date: {start_date} - {end_date}
Total new mailjet subscribers count: {new_mailjet_subscribers_count}
Total mailjet unsubscribe count: {new_mailjet_unsubscribe_count}
Total number of orders: {total_number_of_orders}
Peak orders day: {peak_orders_day}
Most popular ordered product: {most_popular_ordered_product}
Most popular ordered variant: {most_popular_ordered_variant}
Reviews count: {reviews_count}
Review reminder emails count: {review_reminder_emails_count}
In-Stock requests count: {in_stock_requests_count}
In-Stock emails count: {in_stock_emails_count}
'''
    service_name = 'Weekly Marketing Email Service'

    def get_variables(self):
        mailjet_analyzer = MailjetMetricsAnalyzer()
        mailjet_analyzer.analyze_metrics()
        orders_analyzer = OrdersMetricsAnalyzer()
        orders_analyzer.analyze_metrics()

        now = timezone.now()
        reviews_count = Review.objects.filter(date_created__gt=now - timedelta(days=7)).count()
        review_reminder_emails_count = ReviewReminder.objects.filter(
            reminder_date__gt=now - timedelta(days=7),
            email_sent=True,
        ).count()

        marketing_emails = Configuration.objects.get(key='marketing_team').value.split(',')
        in_stock_emails_count = SentEmail.objects.filter(
            template_name=SentEmail.TEMPLATE_IN_STOCK,
            sent_date__gt=now - timedelta(days=7),
        ).exclude(
            email__in=marketing_emails,
        ).count()
        in_stock_requests_count = ProductInStockReport.objects.filter(
            created__gt=now - timedelta(days=7),
        ).exclude(
            email__in=marketing_emails,
        ).count()
        return {
            'new_mailjet_subscribers_count': mailjet_analyzer.new_subscribers_count,
            'new_mailjet_unsubscribe_count': mailjet_analyzer.new_unsubscribe_count,
            'total_number_of_orders': orders_analyzer.total_number_of_orders,
            'peak_orders_day': orders_analyzer.get_peak_orders_day(),
            'most_popular_ordered_product': orders_analyzer.get_most_popular_ordered_product(),
            'most_popular_ordered_variant': orders_analyzer.get_most_popular_ordered_variant(),
            'reviews_count': reviews_count,
            'review_reminder_emails_count': review_reminder_emails_count,
            'in_stock_requests_count': in_stock_requests_count,
            'in_stock_emails_count': in_stock_emails_count,
            'start_date': (now - timedelta(days=7)).date().strftime('%Y-%m-%d'),
            'end_date': now.date().strftime('%Y-%m-%d'),
        }
