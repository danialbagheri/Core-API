from common.services import AdminEmailService
from review.models import Review


class ReviewNotificationFailureEmail(AdminEmailService):
    service_name = 'Review Notification Failure Email'
    subject = 'New review email notification failed'
    message = '''
Failed to send review notification email to managers for review id {review_id}
Error: {error_type}
'''

    def __init__(self, review: Review, error_type: str):
        super().__init__(review=review, error_type=error_type)
        self.review = review
        self.error_type = error_type

    def get_variables(self):
        return {
            'review_id': self.review.id,
            'error_type': self.error_type,
        }
