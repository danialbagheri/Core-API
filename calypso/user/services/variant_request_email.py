import uuid

from django.contrib.sites.shortcuts import get_current_site
from django.core.files.base import ContentFile
from django.core.mail import send_mail


class VariantRequestEmailService:
    def __init__(self, variant_image_request, zip_buffer):
        self.variant_image_request = variant_image_request
        self.zip_buffer = zip_buffer

    def _save_zip_file(self):
        zip_file_name = f'{uuid.uuid4()}.zip'
        self.variant_image_request.zip_file.save(zip_file_name, ContentFile(self.zip_buffer.get_value()), save=False)
        self.variant_image_request.save()
        return f'{get_current_site(None).domain}{self.variant_image_request.zip_file.url}'

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
            recipient_list=[self.variant_image_request.email],
        )
