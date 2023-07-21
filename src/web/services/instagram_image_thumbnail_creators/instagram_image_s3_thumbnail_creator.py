from io import BytesIO
from typing import Tuple
from urllib.parse import urljoin

import boto3
import requests
from botocore.exceptions import ClientError
from django.conf import settings
from sorl.thumbnail import get_thumbnail

from . import InstagramImageThumbnailCreator


class InstagramImageS3ThumbnailCreator(InstagramImageThumbnailCreator):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.image_content = None

    def get_image_path(self) -> str:
        media_url = settings.MEDIA_URL
        path = settings.INSTAGRAM_IMAGES_PATH
        return f'{urljoin(media_url, path)}{self.image_id}.jpg'

    def image_exists(self, full_path: str) -> bool:
        response = requests.get(self.image_url)
        if response.ok:
            self.image_content = response.content
        return response.ok

    def upload_image(self, full_path: str) -> None:
        image_bytes = BytesIO(self.image_content)
        path = f'{settings.INSTAGRAM_IMAGES_PATH}{self.image_id}.jpg'
        s3_client = boto3.client('s3')
        try:
            s3_client.upload_fileobj(
                image_bytes, settings.AWS_STORAGE_BUCKET_NAME, path,
                ExtraArgs={'ContentType': 'image/jpeg'}
            )
        except ClientError as e:
            self.log_exception('Error in S3 client', data={'exception': e})

    def create_thumbnails(self, full_path) -> Tuple[str, str]:
        png_url = get_thumbnail(full_path, '200x200', crop='center', quality=100, format='PNG').url
        webp_url = get_thumbnail(full_path, '200x200', crop='center', quality=100, format='WEBP').url
        return png_url, webp_url
