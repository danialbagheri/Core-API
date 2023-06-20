import logging
from smtplib import SMTPException

from django.core.mail import EmailMessage

from common.services import BaseService

logger = logging.getLogger(__name__)


class InternalEmailService(BaseService):
    subject = None
    message = None
    html_message = None

    def get_subject(self):
        variables = self.get_variables()
        return self.subject.format(**variables)

    def get_message(self):
        message = self.html_message or self.message
        variables = self.get_variables()
        return message.format(**variables)

    def get_variables(self):
        raise NotImplementedError

    def get_from_email(self):
        raise NotImplementedError

    def get_recipient_emails(self):
        raise NotImplementedError

    def get_reply_to_emails(self):
        raise NotImplementedError

    def log_template_error(self, **kwargs):
        logger.exception(
            msg=f'Template error in sending email {self.service_name}',
            extra={
                'service': self.service_name,
                **kwargs,
            }
        )

    def log_email_error(self, **kwargs):
        logger.exception(
            msg=f'Failed to send internal email {self.service_name}',
            extra={
                'service': self.service_name,
                **kwargs,
            },
        )

    def send_email(self):
        try:
            message = self.get_message()
        except KeyError:
            self.log_template_error()
            return

        try:
            email_message = EmailMessage(
                subject=self.get_subject(),
                body=message,
                from_email=self.get_from_email(),
                to=self.get_recipient_emails(),
                reply_to=self.get_reply_to_emails(),
            )
            if self.html_message:
                email_message.content_subtype = 'html'
            email_message.send()
        except SMTPException:
            self.log_email_error()
