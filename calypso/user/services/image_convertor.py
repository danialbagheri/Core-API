import io

from PIL import Image


class ImageConvertor:
    def __init__(self, image_formats):
        self.image_formats = image_formats

    def convert_image(self, file_path):
        images = {}
        for image_format in self.image_formats:
            image_bytes = io.BytesIO()
            image = Image.open(file_path)
            if image_format in ['JPG', 'JPEG']:
                image = image.convert('RGB')
            image.save(image_bytes, image_format)
            image_bytes.seek(0)
            images[image_format] = image_bytes
        return images
