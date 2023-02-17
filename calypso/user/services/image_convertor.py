import io

from PIL import Image


class ImageConvertor:
    def __init__(self, image_format):
        self.image_format = image_format

    def convert_image(self, file_path):
        image_bytes = io.BytesIO()
        image = Image.open(file_path)
        if self.image_format in ['JPG', 'JPEG']:
            image = image.convert('RGB')
        image.save(image_bytes, self.image_format)
        image_bytes.seek(0)
        return image_bytes
