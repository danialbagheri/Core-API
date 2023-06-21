from django.conf import settings

from common.services import ManagerEmailService
from review.models import Review
from review.services import ReviewNotificationFailureEmail


class ReviewNotificationEmail(ManagerEmailService):
    service_name = 'Review Notification Email'
    subject = 'A new review has been submitted on {review_source}'
    message = '''
Please check and approve the latest review by visiting {review_admin_url}
User IP: {user_ip_address}
User name: {user_name}
User email: {user_email}
Review score: {review_score}
Product: {product_title}
Subject: {review_title}
Review:
{review_message}
'''

    def __init__(self, review: Review):
        super().__init__(review=review)
        self.review = review

    def get_variables(self):
        return {
            'review_source': self.review.source,
            'review_admin_url': f'{settings.WEBSITE_ADDRESS}/admin/review/review/{self.review.id}/change/',
            'review_score': self.review.score,
            'review_title': self.review.title,
            'review_message': self.review.comment,
            'user_ip_address': self.review.ip_address,
            'user_name': self.review.customer_name,
            'user_email': self.review.email,
            'product_title': self.review.product.name,
        }

    def log_template_error(self, **kwargs):
        ReviewNotificationFailureEmail(self.review, 'Template Error').send_email()

    def log_email_error(self, **kwargs):
        ReviewNotificationFailureEmail(self.review, 'SMTP Error').send_email()
