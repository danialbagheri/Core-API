from datetime import timedelta

import requests
from django.conf import settings
from django.core.exceptions import ValidationError
from django.utils import timezone
from ipware import get_client_ip
from rest_framework import serializers

from user.models import ScheduledEmail
from user.services import SubscriptionVerifier
from web.models import ContactForm
from web.services import ContactUsEmailSender


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
        ContactUsEmailSender(contact_form).send_email()
        if contact_form.email_sent and SubscriptionVerifier(contact_form.email).is_subscribed():
            ScheduledEmail.objects.get_or_create(
                recipient_email=contact_form.email_sent,
                template_name=ScheduledEmail.TEMPLATE_SUBSCRIBE_INVITATION,
                defaults={
                    'send_time': timezone.now() + timedelta(weeks=2),
                },
            )
        return contact_form
