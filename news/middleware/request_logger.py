import logging
import time

from django.conf import settings


logger = logging.getLogger('django.request')


class RequestLoggingMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if not getattr(settings, 'REQUEST_LOGGING_ENABLED', True):
            return self.get_response(request)

        start_time = time.perf_counter()

        response = self.get_response(request)

        duration = time.perf_counter() - start_time

        ip_address = self.get_client_ip(request)
        url = request.get_full_path()

        logger.info(
            'IP: %s | URL: %s | Время выполнения: %.4f сек.',
            ip_address,
            url,
            duration,
        )

        return response

    def get_client_ip(self, request):
        return request.META.get('REMOTE_ADDR', 'Неизвестен')
