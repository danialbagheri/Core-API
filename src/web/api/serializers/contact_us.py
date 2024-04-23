from datetime import timedelta

from django.core.exceptions import ValidationError
from django.utils import timezone
from rest_framework import serializers

from common.services import MailjetEmailManager
from common.services import RecaptchaValidator
from user.models import ScheduledEmail
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
            'subscribe_sender',
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
        RecaptchaValidator(self.recaptcha_value).validate(self.context['request'])
        return attrs

    def create(self, validated_data):
        contact_form = super().create(validated_data)
        ContactUsEmailSender(contact_form).send_email()
        if contact_form.email_sent:
            ScheduledEmail.objects.get_or_create(
                recipient_email=contact_form.email,
                template_name=ScheduledEmail.TEMPLATE_SUBSCRIBE_INVITATION,
                defaults={
                    'send_time': timezone.now() + timedelta(weeks=2),
                },
            )
        if contact_form.subscribe_sender and contact_form.email:
            MailjetEmailManager(contact_form.email).subscribe_email()
        return contact_form
