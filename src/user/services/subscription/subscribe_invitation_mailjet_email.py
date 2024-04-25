from typing import Dict, Any

from django.conf import settings

from common.services import TransactionalMailJetEmailService
from user.models import SentEmail


class SubscribeInvitationMailjetEmail(TransactionalMailJetEmailService):
    template_name = SentEmail.TEMPLATE_SUBSCRIBE_INVITATION
    template_config_key = 'subscribe-invitation-email-template-id'

    def _get_variables(self) -> Dict[str, Any]:
        email_images_settings = settings.MAILJET_EMAIL_IMAGES
        theme_settings = settings.MAILJET_EMAILS_THEME
        socials_settings = settings.SOCIAL_URLS
        return {
            'top_image_url': email_images_settings['subscribe_invitation_top'],
            'form_image_url': email_images_settings['subscribe_invitation_form'],

            'primary_background_color': theme_settings['primary_background_color'],
            'secondary_text_color': theme_settings['secondary_text_color'],

            'instagram_account_url': socials_settings['instagram'],
            'instagram_logo_url': email_images_settings['instagram_logo'],
            'facebook_account_url': socials_settings['facebook'],
            'facebook_logo_url': email_images_settings['facebook_logo'],
            'x_account_url': socials_settings['x'],
            'x_logo_url': email_images_settings['x_logo'],
            'youtube_account_url': socials_settings['youtube'],
            'youtube_logo_url': email_images_settings['youtube_logo'],

            'white_logo_url': email_images_settings['footer_logo'],
            'website_url': settings.WEBSITE_ADDRESS,
            'subscribe_page_url': f'{settings.WEBSITE_ADDRESS}/subscribe',
        }

    def _get_extra_data(self) -> str:
        return ''
