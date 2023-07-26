from typing import Tuple

from common.services import BaseService


class InstagramImageThumbnailCreator(BaseService):
    def __init__(self, image_url, image_id):
        super().__init__(image_url=image_url, image_id=image_id)
        self.image_url = image_url
        self.image_id = image_id

    def get_image_path(self) -> str:
        raise NotImplementedError

    def image_exists(self, full_path: str) -> bool:
        raise NotImplementedError

    def upload_image(self, full_path: str) -> None:
        raise NotImplementedError

    def create_thumbnails(self, full_path) -> Tuple[str, str]:
        raise NotImplementedError

    def get_image_thumbnails(self) -> Tuple[str, str]:
        full_path = self.get_image_path()
        if not self.image_exists(full_path):
            self.upload_image(full_path)
        png_thumbnail_url, webp_thumbnail_url = self.create_thumbnails(full_path)
        return png_thumbnail_url, webp_thumbnail_url
