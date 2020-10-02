from django.core.mail import send_mail
from rest_framework.views import APIView
from .serializers import ContactFormSerializer, REASON_CHOICES
from rest_framework import authentication
from rest_framework.response import Response
from django.http import HttpResponse, JsonResponse

import pdb


class ContactForm(APIView):
    # authentication_classes = [authentication.TokenAuthentication]
    def post(self, request, *args, **kwargs):
        contact_serializer = ContactFormSerializer(
            data=request.data, context={"request": request})
        if contact_serializer.is_valid():
            data = contact_serializer.validated_data
            email_from = data.get('email')
            subject = data.get('reason')
            message = data.get('message')
            pdb.set_trace()
            try:
                if subject in REASON_CHOICES[:3]:
                    send_mail(subject, message, email_from, [
                              'pr@lincocare.com', 'info@calypsosun.com'],)
                else:
                    send_mail(subject, message, email_from,
                              ['info@calypsosun.com'],)
                return JsonResponse({"success": "Success"}, status=200)
            except Exception as e:
                return JsonResponse({"success": "Failed", "message": f"{e}"}, status=400)
        return JsonResponse(contact_serializer.errors, status=400)
