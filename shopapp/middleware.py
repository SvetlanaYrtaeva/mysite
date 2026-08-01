from django.http import HttpResponse
import time


class ThrottlingMiddleware:
    """
    Middleware для ограничения частоты запросов от пользователя.
    Лимит: максимум 10 запросов в минуту от одного IP.
    """

    def __init__(self, get_response):
        self.get_response = get_response
        self.max_requests_per_minute = 10
        self.time_window = 60

        self.request_history = {}

    def __call__(self, request):
        ip_address = request.META.get('HTTP_X_FORWARDED_FOR', request.META.get('REMOTE_ADDR'))

        if ip_address and ',' in ip_address:
            ip_address = ip_address.split(',')[0].strip()

        if not ip_address:
            return self.get_response(request)

        current_time = time.time()

        if ip_address not in self.request_history:
            self.request_history[ip_address] = []

        self.request_history[ip_address] = [
            timestamp for timestamp in self.request_history[ip_address]
            if current_time - timestamp < self.time_window
        ]

        if len(self.request_history[ip_address]) >= self.max_requests_per_minute:
            return HttpResponse(
                '<h1>429 Too Many Requests</h1>'
                '<p>Вы превышили лимит запросов: {} запросов в минуту.</p>'
                '<p>Подождите немного и попробуйте снова.</p>'
                '<a href="/">← На главную</a>'
                .format(self.max_requests_per_minute),
                content_type='text/html',
                status=429
            )

        self.request_history[ip_address].append(current_time)

        return self.get_response(request)