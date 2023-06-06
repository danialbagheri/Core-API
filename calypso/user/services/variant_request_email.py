import uuid
from typing import Set

from django.contrib.sites.shortcuts import get_current_site
from django.core.files.base import ContentFile
from django.core.mail import send_mail


class VariantRequestEmailService:
    def __init__(self, variant_image_request, zip_buffer):
        self.variant_image_request = variant_image_request
        self.zip_buffer = zip_buffer

    def _save_zip_file(self):
        zip_file_name = f'{uuid.uuid4()}.zip'
        self.variant_image_request.zip_file.save(zip_file_name, ContentFile(self.zip_buffer.read()), save=False)
        self.variant_image_request.save()
        return f'{get_current_site(None).domain}{self.variant_image_request.zip_file.url}'

    @staticmethod
    def _get_message(zip_file_url: str, all_sku_without_image: Set[str]):
        return f'''
Your Images are now ready for you to view. Please follow the link below and download the zip file.

{zip_file_url}

Below given SKUs did not have any images the way you wanted:
{', '.join(all_sku_without_image) if all_sku_without_image else '-'}


For security purposes, always check the website URL and make sure the connection between you and our server is secure.
If you have not requested this email please ignore this email.
'''

    def send_email(self, all_sku_without_image: Set[str]):
        zip_file_url = self._save_zip_file()
        message = self._get_message(zip_file_url, all_sku_without_image)
        from_email = 'admin@calypsosun.com'
        send_mail(
            subject='Image Files',
            message=message,
            from_email=from_email,
            recipient_list=[self.variant_image_request.email],
        )
        self.variant_image_request.email_sent = True
        self.variant_image_request.save()
