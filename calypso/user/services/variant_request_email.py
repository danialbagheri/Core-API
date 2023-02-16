import uuid

from django.contrib.sites.shortcuts import get_current_site
from django.core.files.base import ContentFile
from django.core.mail import send_mail

from user.models import VariantImageRequest


class VariantRequestEmailService:
    def __init__(self, sku_list, email, zip_buffer):
        self.sku_list = sku_list
        self.email = email
        self.zip_buffer = zip_buffer

    def _save_zip_file(self):
        variant_image_request = VariantImageRequest.objects.create(
            sku_list=str(self.sku_list),
            email=self.email,
        )
        zip_file_name = f'{uuid.uuid4()}.zip'
        variant_image_request.zip_file.save(zip_file_name, ContentFile(self.zip_buffer.get_value()), save=False)
        variant_image_request.save()
        return f'{get_current_site(None).domain}{variant_image_request.zip_file.url}'

    @staticmethod
    def _get_message(zip_file_url):
        return f'''
Your Images are now ready for you to view. Please follow the link below and download the zip file.

{zip_file_url}

For security purposes, always check the website URL and make sure the connection between you and our server is secure.
If you have not requested this email please ignore this email.
'''

    def send_email(self):
        zip_file_url = self._save_zip_file()
        message = self._get_message(zip_file_url)
        from_email = 'admin@calypsosun.com'
        send_mail(
            subject='Image Files',
            message=message,
            from_email=from_email,
            recipient_list=[self.email],
        )
