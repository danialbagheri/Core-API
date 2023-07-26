import logging

logger = logging.getLogger(__name__)


class BaseService:
    service_name = None

    def __init__(self, **kwargs):
        self.log_info(
            message='Service started',
            data=kwargs,
        )

    def log_info(self, message, data=None):
        logger.info(msg=f'{self.service_name}: {message}. Data: {data}')

    def log_exception(self, message, data=None):
        logger.exception(msg=f'{self.service_name}: {message}. Data: {data}')
