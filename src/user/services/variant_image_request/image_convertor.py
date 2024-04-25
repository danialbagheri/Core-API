import io

import requests
from PIL import Image


class ImageConvertor:
    def __init__(self, image_formats):
        self.image_formats = image_formats

    def convert_image(self, file_path):
        images = {}
        for image_format in self.image_formats:
            response = requests.get(file_path)
            image_data = response.content
            image_bytes = io.BytesIO()
            image = Image.open(io.BytesIO(image_data))
            if image_format in ['JPG', 'JPEG']:
                image = image.convert('RGB')
            image.save(image_bytes, image_format if image_format != 'JPG' else 'JPEG', quality=100)
            image_bytes.seek(0)
            images[image_format] = image_bytes
        return images
