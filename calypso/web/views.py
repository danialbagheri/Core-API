from django.shortcuts import render
from django.views.generic import TemplateView, DetailView, ListView
from product.models import ProductCategory
from .serializers import ContactFormSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
# Create your views here.


class HomePage(ListView):
    model = ProductCategory
    context_object_name = "product_categories"
    template_name = "pages/home.html"


class ContactFormView(APIView):
    def post(self, request, *args, **kwargs):
        contact_serializer = ContactFormSerializer(data=request.data)
        if contact_serializer.is_valid():
            data = contact_serializer.validated_data
            email_from = data.get('email')
            subject = data.get('subject')
            message = data.get('message')
            try:
                send_mail(subject, message, email_from, ['send to email'],)
                return Response({"success": "Sent"})
            except Exception as e:
                return Response({"success": "Failed", "message": f"{e}"})
