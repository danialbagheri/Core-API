from typing import Dict, Any

from django.conf import settings

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
            'subject': 'Response to Your Review on Our Website',
            'text': '''
Please see below our reply to your recent review:

{reply}
'''.format(reply=self.review.reply),
            'instagram_account_url': 'https://www.instagram.com/calypsosuncare/',
            'instagram_logo_url': 'https://calypso-static.s3.amazonaws.com/media/django-summernote/'
                                  '2023-08-18/f3559099-5f82-448a-b1ea-c2d7d0448547.png',
            'facebook_account_url': 'https://www.facebook.com/calypsosuncare/',
            'facebook_logo_url': 'https://calypso-static.s3.amazonaws.com/media/django-summernote/'
                                 '2023-08-18/2a31eeb4-4043-48ac-af19-e33c0055bd27.png',
            'x_account_url': 'https://x.com/calypsosuncare',
            'x_logo_url': 'https://calypso-static.s3.amazonaws.com/media/django-summernote/'
                          '2023-08-18/f9212e97-f7f7-4fe0-909f-a762a9072cb7.png',
            'youtube_account_url': 'https://www.youtube.com/channel/UCrZ14JcmZRDobPIVo8ptmrw',
            'youtube_logo_url': 'https://calypso-static.s3.amazonaws.com/media/django-summernote/'
                                '2023-08-18/a8f14c7a-23e5-4d43-b1db-901a9a60f36d.png',
            'white_logo_url': 'https://calypso-static.s3.eu-west-2.amazonaws.com/media/email-images/Calypso-white.png',
            'secondary_text_color': 'white',
            'website_url': settings.WEBSITE_ADDRESS,
        }

    def _get_extra_data(self) -> str:
        return f'{self.review.id}'
