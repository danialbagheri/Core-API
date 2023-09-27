from django.conf import settings
from django.core.mail import send_mail

from common.services import BaseService
from web.models import ContactForm, Configuration


class ContactUsEmailSender(BaseService):
    service_name = 'Contact Us Email Sender'
    REASON_CHOICES = [
        'Urgent: Change Order detail or Address',
        'Question about order or Delivery',
        'Press Contact & Media',
        'Wholesale, Discount, promo code query',
        'Product Question',
        'Other'
    ]

    def __init__(self, contact_form: ContactForm):
        super().__init__(reason=contact_form.reason, email=contact_form.email)
        self.contact_form = contact_form
        self.email_from = settings.SERVER_EMAIL

    def _get_email_message(self):
        return f'''
                From: {self.contact_form.email}
                Address: {self.contact_form.address}
                Subject: {self.contact_form.reason}

                {self.contact_form.message}
                ________
                This email is sent via {settings.SITE_NAME} contact us page.
'''

    def _send_to_reason_specific_emails(self, message, emails):
        send_mail(self.contact_form.reason, message, self.email_from, emails.split(','))
        self.contact_form.receivers_email = emails

    def _send_to_default_marketing_emails(self, message):
        marketing_emails, _ = Configuration.objects.get_or_create(
            key='marketing_emails',
            defaults={
                'name': 'Marketing Emails',
                'value': settings.DEFAULT_MARKETING_EMAIL,
            },
        )
        send_mail(self.contact_form.reason, message, self.email_from, marketing_emails.value.split(','), )
        self.contact_form.receivers_email = marketing_emails.value

    def _send_to_default_customer_service_emails(self, message):
        customer_service_emails, _ = Configuration.objects.get_or_create(
            key='customer_service_emails',
            defaults={
                'name': 'Customer Service Emails',
                'value': settings.DEFAULT_CUSTOMER_SERVICE_EMAIL,
            },
        )
        send_mail(self.contact_form.reason, message, self.email_from, customer_service_emails.value.split(','))
        self.contact_form.receivers_email = customer_service_emails.value

    def send_email(self):
        message = self._get_email_message()
        try:
            reason_config = Configuration.objects.filter(key=self.contact_form.reason).first()
            if reason_config:
                self._send_to_reason_specific_emails(message, reason_config.value)
            elif self.contact_form.reason in self.REASON_CHOICES[:3]:
                self._send_to_default_marketing_emails(message)
            else:
                self._send_to_default_customer_service_emails(message)
            self.contact_form.email_sent = True
            self.contact_form.save()
        except:
            pass
