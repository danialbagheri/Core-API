from django.conf import settings
from mailchimp_marketing import Client
from mailchimp_marketing.api_client import ApiClientError


class MarketingSubscriberService:
    def __init__(self):
        self.mailchimp = Client()
        self.mailchimp.set_config({
            'api_key': settings.MAILCHIMP_MARKETING_API_KEY,
            'server': settings.MAILCHIMP_SERVER_PREFIX,
        })

    def subscribe_email(self, email):
        try:
            self.mailchimp.lists.batch_list_members(
                list_id='c458361e44',
                body={
                    'members': [
                        {
                            'email_address': email,
                            'email_type': 'html',
                            'status': 'subscribed',
                        }
                    ],
                    'update_existing': True,
                }
            )
        except ApiClientError:
            pass
