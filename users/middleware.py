import logging
import os
from datetime import datetime

from django.conf import settings

logger = logging.getLogger(__name__)

class RequestLoggerMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        self.log_request(request)
        response = self.get_response(request)
        self.log_response(request, response)
        return response

    def log_request(self, request):
        request_data = {
            'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'method': request.method,
            'path': request.path,
            'query_params': dict(request.GET),
            'body': request.body.decode('utf-8'),
            'user': str(request.user),
        }
        self.write_to_log('request.log', request_data)

    def log_response(self, request, response):
        response_data = {
            'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'status_code': response.status_code,
            'content': response.content.decode('utf-8'),
        }
        self.write_to_log('response.log', response_data)

    def write_to_log(self, filename, data):
        log_dir = os.path.join(settings.BASE_DIR, 'logs')
        os.makedirs(log_dir, exist_ok=True)
        log_file = os.path.join(log_dir, filename)
        with open(log_file, 'a') as f:
            f.write(str(data) + '\n')

    def process_exception(self, request, exception):
        error_data = {
            'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'path': request.path,
            'user': str(request.user),
            'exception': str(exception),
        }
        self.write_to_log('errors.log', error_data)
        logger.error(f'Exception occurred: {exception}')
        return None