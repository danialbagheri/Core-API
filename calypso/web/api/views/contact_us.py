from django.core.mail import send_mail
from django.http import JsonResponse
from rest_framework.views import APIView

from web.models import Configuration
from ..serializers import ContactFormSerializer
from ..serializers.contact_us import REASON_CHOICES


class ContactForm(APIView):

    def post(self, request, *args, **kwargs):
        contact_serializer = ContactFormSerializer(
            data=request.data, context={"request": request})
        if contact_serializer.is_valid(raise_exception=True):

            data = contact_serializer.validated_data
            email_from = "admin@calypsosun.com"
            customer_email = data.get('email')
            subject = data.get('reason')
            query = data.get('message')
            address = data.get('address')
            message = f'''

From: {customer_email}
Address: {address}
Subject: {subject}

{query}
________
This email is sent via Calypsosun.com contact us page.

            '''

            try:
                reason_config = Configuration.objects.filter(key=subject).first()
                if reason_config:
                    send_mail(subject, message, email_from, reason_config.value.split(','))
                    return JsonResponse({"success": "Success"}, status=200)
                customer_service_emails, created = Configuration.objects.get_or_create(key="customer_service_emails")
                if created:
                    customer_service_emails.name = "Customer Service emails"
                    customer_service_emails.value = "info@calypsosun.com"
                    customer_service_emails.save()
                marketing_emails, marketing_created = Configuration.objects.get_or_create(key="marketing_emails")
                if marketing_created:
                    marketing_emails.name = "Marketing Emails"
                    marketing_emails.value = "pr@lincocare.com"
                    marketing_emails.save()

                if subject in REASON_CHOICES[:3]:
                    send_mail(subject, message, email_from, marketing_emails.value.split(','),)
                else:
                    send_mail(subject, message, email_from,
                              customer_service_emails.value.split(','),)
                return JsonResponse({"success": "Success"}, status=200)
            except Exception as e:
                return JsonResponse({"success": "Failed", "message": f"{e}"}, status=400)
        return JsonResponse(contact_serializer.errors, status=400)
