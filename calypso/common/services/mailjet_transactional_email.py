import logging
from typing import Any, Dict, List

from django.conf import settings
from mailjet_rest import Client
from requests import Response

from user.models import SentEmail

logger = logging.getLogger(__name__)


class TransactionalMailJetEmailService:
    template_name = None
    template_id = None

    def __init__(self, emails: List[str]) -> None:
        self.emails = emails
        self.mailjet = Client(
            auth=(settings.MAILJET_API_KEY, settings.MAILJET_SECRET_KEY),
            version='v3.1',
        )

    def _get_template_id(self):
        return self.template_id

    def _get_receiver_emails(self) -> List[str]:
        return self.emails

    def _get_variables(self) -> Dict[str, Any]:
        raise NotImplementedError

    def _get_extra_data(self) -> str:
        raise NotImplementedError

    def _send_email_api_request(self) -> Response:
        data = {
            'Messages': [
                {
                    'To': [
                        {
                            'Email': email
                        } for email in self._get_receiver_emails()
                    ],
                    'TemplateID': self._get_template_id(),
                    'TemplateLanguage': True,
                    'Variables': self._get_variables()
                }
            ],
            'SandboxMode': settings.DEBUG,
        }
        return self.mailjet.send.create(data=data)

    @staticmethod
    def _get_email_id(email_api_response: Response) -> str:
        email_id = None
        messages = email_api_response.json().get('Messages', [])
        if messages:
            email_id = messages[0]['To'][0]['MessageID']
        return email_id

    def _create_log(self, email_api_response: Response) -> None:
        email_id = self._get_email_id(email_api_response)
        for email in self.emails:
            SentEmail.objects.create(
                email=email,
                template_name=self.template_name,
                email_id=email_id,
                data=self._get_extra_data(),
            )

    def _log_error(self) -> None:
        logger.exception(
            msg=f'Failed to send {self.template_name} email to {self.emails}.',
        )

    def send_emails(self) -> None:
        if not self._get_template_id():
            logger.warning(f'Template ID is not set.')
            return
        logger.info(f'Sending email {self.template_name} to email {self.emails}')
        response = self._send_email_api_request()
        if response.ok:
            self._create_log(response)
        else:
            self._log_error()
