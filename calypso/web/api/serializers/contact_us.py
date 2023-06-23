import requests
from django.conf import settings
from django.core.exceptions import ValidationError
from django.core.mail import send_mail
from ipware import get_client_ip
from rest_framework import serializers

from web.models import ContactForm, Configuration

REASON_CHOICES = [
    'Urgent: Change Order detail or Address',
    'Question about order or Delivery',
    'Press Contact & Media',
    'Wholesale, Discount, promo code query',
    'Product Question',
    'Other'
]


class ContactFormSerializer(serializers.ModelSerializer):

    class Meta:
        model = ContactForm
        fields = (
            'id',
            'email',
            'name',
            'address',
            'subject',
            'reason',
            'message',
        )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.recaptcha_value = None

    def to_internal_value(self, data):
        self.recaptcha_value = data.get('recaptcha')
        return super().to_internal_value(data)

    def validate(self, attrs):
        if not self.recaptcha_value:
            raise ValidationError('Recaptcha data not sent.')

        ip, _ = get_client_ip(self.context['request'])
        response = requests.post(
            url=f'https://www.google.com/recaptcha/api/siteverify?'
                f'secret={settings.DRF_RECAPTCHA_SECRET_KEY}&response={self.recaptcha_value}&remoteip={ip}',
        )
        if response.status_code != 200 or not response.json().get('success', False):
            raise ValidationError('Recaptcha validation failed.')
        return attrs

    def create(self, validated_data):
        contact_form = super().create(validated_data)
        email_from = "admin@calypsosun.com"
        message = f'''

        From: {contact_form.email}
        Address: {contact_form.address}
        Subject: {contact_form.reason}

        {contact_form.message}
        ________
        This email is sent via Calypsosun.com contact us page.

                    '''

        try:
            reason_config = Configuration.objects.filter(key=contact_form.reason).first()
            if reason_config:
                send_mail(contact_form.reason, message, email_from, reason_config.value.split(','))
                contact_form.email_sent = True
                contact_form.receivers_email = reason_config.value
                contact_form.save()
                return contact_form
            customer_service_emails, created = Configuration.objects.get_or_create(
                key='customer_service_emails',
                defaults={
                    'name': 'Customer Service Emails',
                    'value': settings.DEFAULT_CUSTOMER_SERVICE_EMAIL,
                },
            )
            marketing_emails, marketing_created = Configuration.objects.get_or_create(
                key='marketing_emails',
                defaults={
                    'name': 'Marketing Emails',
                    'value': settings.DEFAULT_MARKETING_EMAIL,
                },
            )

            if contact_form.reason in REASON_CHOICES[:3]:
                send_mail(contact_form.reason, message, email_from, marketing_emails.value.split(','), )
                contact_form.receivers_email = marketing_emails.value
            else:
                send_mail(
                    contact_form.reason, message, email_from, customer_service_emails.value.split(',')
                )
                contact_form.receivers_email = customer_service_emails.value
            contact_form.email_sent = True
            contact_form.save()
        except:
            pass
        return contact_form
