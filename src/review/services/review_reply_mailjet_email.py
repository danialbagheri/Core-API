from typing import Dict, Any

from common.services import TransactionalMailJetEmailService
from review.models import Review
from user.models import SentEmail
from web.models import Configuration


class ReviewReplyMailjetEmail(TransactionalMailJetEmailService):
    template_name = SentEmail.TEMPLATE_REVIEW_REPLY

    def _get_template_id(self):
        template_id_config = Configuration.objects.filter(key='review-reply-email-template-id').first()
        if not template_id_config:
            return None
        return int(template_id_config.value)

    def __init__(self, review: Review, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.review = review

    def _get_variables(self) -> Dict[str, Any]:
        return {
            'subject': '',
            'text': '',
        }

    def _get_extra_data(self) -> str:
        return f'Review ID: {self.review.id}'
