from rest_framework.request import Request

from common.services import BaseService


class RequestIPRetriever(BaseService):
    def __init__(self, request: Request):
        super().__init__(request_meta=request.META)
        self.request = request

    def get_ip(self):
        x_forwarded_for = self.request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            return x_forwarded_for.split(',')[0]
        return self.request.META.get('REMOTE_ADDR')
